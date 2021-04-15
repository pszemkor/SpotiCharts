from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine('sqlite:///spoticharts.db', echo=True)
conn = engine.connect()
session = Session(bind=engine)