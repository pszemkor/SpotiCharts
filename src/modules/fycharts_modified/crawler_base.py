import sys
import io

import itertools
import logging
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import re

from .log_config import logger


def emptyDf(size, region, date):
	"""Returns a df full of NA i.e empty df
	size - 200 or 50 i.e. viral 50 or top 200
	region - Region of interest
	date - Date of interest
	"""
	if(size == 50):
		isViral = True
	else:
		isViral = False

	pos = list(itertools.repeat("NA", size))
	track = list(itertools.repeat("NA", size))
	art = list(itertools.repeat("NA", size))
	stre = list(itertools.repeat("NA", size))
	reg = list(itertools.repeat(region, size))
	dat = list(itertools.repeat(date, size))
	i = list(itertools.repeat("NA", size))

	if(isViral):
		empty = pd.DataFrame.from_dict({"position": pos, "track name":track, "artist":art, "region": reg, "date":dat, "spotify_id":i})
	else:
		empty = pd.DataFrame.from_dict({"position": pos, "track name":track, "artist":art, "streams":stre, "region": reg, "date":dat, "spotify_id":i})

	return empty


class SpotifyChartsBase(object):
	def __init__(self):
		""" Set up necessary things
		"""
		self.logger = logger


	def __regex(self, url):
		"""Extract Track ID from URL
		url - Spotify track URL
		"""
		if(type(url) == str):
			sr = re.search(r"https://open.spotify.com/track/(.*)" ,url, re.I|re.M)
			trackId = sr.group(1)
		else:
			trackId = "N/A"
		
		return trackId

	def __makeRequests(self, url, date, region, isSkip, size):
			"""Make the HTTP request, clean data, and return as df
			url - The URL to make request
			isSkip - Whether or not to skip first row of CSV file
			"""
			headers = {"Host":"spotifycharts.com", "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36"}

			retries = Retry(total = 2, backoff_factor = 2, status_forcelist = [500, 502, 503, 504, 404])

			try:
				s = requests.Session()
				s.mount("https://", HTTPAdapter(max_retries = retries))
				res = s.get(url, headers = headers, timeout = 3)

				if(res.status_code == 200):
					if(res.headers["Content-Type"] == "text/html; charset=UTF-8"):
						self.logger.error("***** Data not found. Generating empty dataframe *****")

						df = emptyDf(size, region, date)

					else:
						data = res.content
						if(isSkip):
							df = pd.read_csv(io.StringIO(data.decode("utf-8")), skiprows=1)
						else:
							df = pd.read_csv(io.StringIO(data.decode("utf-8")))

						df["date"] = date
						df["region"] = region
						df["spotify_id"] =  df["URL"].apply(lambda x: self.__regex(x))
						df.drop(["URL"], axis=1, inplace=True)


				else:
					self.logger.error("***** Data not found. Generating empty dataframe *****")
					df = emptyDf(size, region, date)

				return df
			except Exception as e:
				self.logger.error(f"*****Data not found with error <<{e}>>. Generating empty dataframe *****")

				df = emptyDf(size, region, date)
				
				return df


	def helperTop200Weekly(self, date, region):
		"""Base method to return df of top 200 weekly
		date: Date to extract df
		region: Region of interest
		"""
		self.logger.info("Extracting top 200 weekly for {} - {}".format(date, region))
		url = "https://spotifycharts.com/regional/{}/weekly/{}/download".format(region, date)
		data = self.__makeRequests(url, date, region, True, 200)

		return data

	
	def helperTop200Daily(self, date, region):
		"""Base method to return df of top 200 daily
		date: Date to extract df
		region: Region of interest
		"""
		self.logger.info("Extracting top 200 daily for {} - {}".format(date, region))
		url = "https://spotifycharts.com/regional/{}/daily/{}/download".format(region, date)
		data = self.__makeRequests(url, date, region, True, 200)

		return data


	def helperViral50Weekly(self, date, region):
		"""Base method to return df of viral 50 weekly
		date: Date to extract df
		region: Region of interest
		"""
		self.logger.info("Extracting viral 50 weekly for {} - {}".format(date, region))
		url = "https://spotifycharts.com/viral/{}/weekly/{}/download".format(region, date)
		data = self.__makeRequests(url, date, region, False, 50)

		return data


	def helperViral50Daily(self, date, region):
		"""Base method to return df of viral 50 daily
		date: Date to extract df
		region: Region of interest
		"""
		self.logger.info("Extracting viral 50 daily for {} - {}".format(date, region))
		url = "https://spotifycharts.com/viral/{}/daily/{}/download".format(region, date)
		data = self.__makeRequests(url, date, region, False, 50)

		return data

		
