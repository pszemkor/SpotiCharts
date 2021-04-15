from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///modules/db/spoticharts.db', echo=False)
conn = engine.connect()
Session = sessionmaker(bind=engine)