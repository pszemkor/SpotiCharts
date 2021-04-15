from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import os
import pandas as pd
from datetime import datetime

from modules.db.model import Base, Top200, Viral50


def fix_date(d):
    date_string = d['date']
    parsed_date = datetime.strptime(date_string, '%Y-%m-%d').date()
    d['date'] = parsed_date
    return d


engine = create_engine('sqlite:///spoticharts.db', echo=True)
conn = engine.connect()
session = Session(bind=engine)
Base.metadata.create_all(engine)
path = r'../../../data_merged'
expected_dirs = {'top200': lambda item: Top200(**item), 'viral': lambda item: Viral50(**item)}
print("Reading data from:", path)
for dir in expected_dirs:
    print("Reading from:", dir)
    dir_path = os.path.join(path, dir)
    dir_df = None
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        print(file_path)
        df = pd.read_csv(file_path)
        df = df.rename({'track name': 'track_name'}, axis=1)
        values = df.T.to_dict().values()
        objects = list(map(lambda item: expected_dirs[dir](fix_date(item)), values))
        rows_count = len(objects)
        session.bulk_save_objects(objects)
        session.commit()
        print("{} rows from file: '{}' saved successfully".format(rows_count, file_name))
