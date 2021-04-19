import datetime
import sys


from .log_config import logger
from .exceptions import FyChartsException


def defaultListOfDates(isWeekly, isViral):
    viralWeeklyStart = "2017-01-05"
    topWeeklyStart = "2016-12-22"
    allDailyStart = "2017-01-01"

    if(isWeekly):
        if(isViral):
            start = datetime.datetime.strptime(viralWeeklyStart, "%Y-%m-%d")
        else:
            start = datetime.datetime.strptime(topWeeklyStart, "%Y-%m-%d")
    else:
        start = datetime.datetime.strptime(allDailyStart, "%Y-%m-%d")

    end = datetime.datetime.now()

    dates = []
    if(isWeekly):
        if(isViral):
            gen = [start + datetime.timedelta(weeks = x) for x in range(0, (end-start).days + 1)]
            for date in gen:
                if(date < end):
                    dt = date + datetime.timedelta(days = 0)
                    dates.append(dt.strftime("%Y-%m-%d"))
        else:
            gen = [start + datetime.timedelta(weeks = x) for x in range(0, (end-start).days + 1)]
            for date in gen:
                if(date<end):
                    dt = date + datetime.timedelta(days=1)
                    dates.append(dt.strftime("%Y-%m-%d"))

    else:
        gen = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days+1)]
        for date in gen:
            if(date<=end):
                dates.append(date.strftime("%Y-%m-%d"))

    return dates


def returnDatesAndRegions(start=None, end=None, theRegs=None, isWeekly=False, isViral=False):
    """Return list of dates and regions based on query
    start - String start of range. Can be None i.e. range is from the beginning of data
    end - String end of range. Can be None i.e. range is till today
    isWeekly - Frequency is weekly or daily. Default is False i.e. Frequency is daily
    isViral - Top 200 or Viral 50. Default is False i.e. Return Top 200
    region - Region of chart. Default is None i.e. Get for all regions
    """
    # Default values
    regions = ["global", "ad", "ar", "at", "au", "be", "bg", "bo", "br", "ca", "ch", "cl", "co", "cr", "cy", "cz", "de", "dk", "do", "ec", "ee", "es", "fi", "fr", "gb", "gr", "gt", "hk", "hn", "hu", "id", "ie", "il", "is", "it", "jp", "lt", "lu", "lv", "mc", "mt", "mx","my", "ni", "nl", "no", "nz", "pa", "pe", "ph", "pl", "pt", "py", "ro", "se", "sg", "sk", "sv", "th", "tr", "tw", "us", "uy", "vn", "za"]
    viralWeeklyStart = "2017-01-05"
    topWeeklyStart = "2016-12-22"
    allDailyStart = "2017-01-01"

    #Required since dates taken are very specific
    defaultList = defaultListOfDates(isWeekly, isViral)
    #--------------------------------------------

    # Helper for Exception handling
    if(isWeekly and isViral):
        func = "viral50Weekly"
    elif(isWeekly and not isViral):
        func = "top200Weekly"
    elif(not isWeekly and isViral):
        func = "viral50Daily"
    elif(not isWeekly and not isViral):
        func = "top200Daily"
    #

    # Start dates
    if(start is None): #From the beginning
        if(isWeekly):
            if(isViral):
                start = datetime.datetime.strptime(viralWeeklyStart, "%Y-%m-%d")
            else:
                start = datetime.datetime.strptime(topWeeklyStart, "%Y-%m-%d")
        else:
            start = datetime.datetime.strptime(allDailyStart, "%Y-%m-%d")
    else:
        if(start in defaultList):
            start = datetime.datetime.strptime(start, "%Y-%m-%d")
        else:
            orderedList = sorted(defaultList, key=lambda x: datetime.datetime.strptime(x, "%Y-%m-%d") - datetime.datetime.strptime(start, "%Y-%m-%d"))
            closest = [d for d in orderedList if d >= start]
            suggest = closest[0:5]
            logger.info(f"The start date {start} provided for {func} is invalid. Wanna give one these a try? {suggest}")
            choice = input("Enter (1) to use the first suggestion, or (2) to quit and set yourself: ")
            if(int(choice) == 1):
                start = datetime.datetime.strptime(suggest[0], "%Y-%m-%d")
            elif(int(choice) == 2):
                sys.exit()
            else:
                raise FyChartsException("Invalid Choice.")


    # End dates
    if(end is None): #Up to now
        end = datetime.datetime.now()
    else:
        end = datetime.datetime.strptime(end, "%Y-%m-%d")
        

    # Region
    region = []
    if(theRegs is None):
        region = regions
    else:
        if(type(theRegs) is not list):
            regs = []
            regs.append(theRegs)
            theRegs = regs
            
        for aReg in theRegs:
            region.append(aReg)

    #Generate list of dates
    dates = []
    if(isWeekly):
        if(isViral):
            gen = [start + datetime.timedelta(weeks=x) for x in range(0, (end-start).days+1)]
            for date in gen:
                if(date<end):
                    dt = date + datetime.timedelta(days=0)
                    dates.append(dt.strftime("%Y-%m-%d"))
        else:
            gen = [start + datetime.timedelta(weeks=x) for x in range(0, (end-start).days+1)]
            for date in gen:
                if(date<end):
                    dt = date + datetime.timedelta(days=0)
                    dates.append(dt.strftime("%Y-%m-%d"))

    else:
        gen = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days+1)]
        for date in gen:
            if(date<=end):
                dates.append(date.strftime("%Y-%m-%d"))

    dates.reverse()
    var = {"dates": dates, "region": region}
    return var

def whatDates(start, end, desired):
    
    if(desired == "top200Daily"):
        isWeekly = False
        isViral = False
    elif(desired == "top200Weekly"):
        isWeekly = True
        isViral = False
    elif(desired == "viral50Daily"):
        isWeekly = False
        isViral = True
    elif(desired == "viral50Weekly"):
        isWeekly = True
        isViral = True

    allValids = defaultListOfDates(isWeekly, isViral)

    fin = [date for date in allValids if date <= end and date >= start]
    
    return fin
