from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
# Imports the methods needed to abstract classes into tables
# Allow us to declare column types

Base=declarative_base()

class Events(Base):
    __tablename__='events'
    id=Column(Integer, primary_key=True, autoincrement=True)
    event_id=Column(String)
    time=Column(Float)
    headline=Column(String)
    event_type=Column(String)
    severity=Column(String)
    lat=Column(Float)
    lon=Column(Float)

    def __repr__(self):
      return f'<event_id> {self.event_id}' 