from sqlalchemy import Column, Integer, Float, Date, Boolean, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy_utils import database_exists, create_database
from geoalchemy2 import Geometry
import pandas as pd

import config


base = declarative_base()


class Station(base):
    __tablename__ = 'stations'
    id = Column(Integer, primary_key=True)
    id_station = Column(Integer)
    name = Column(String(100))
    longitude = Column(Float)
    latitude = Column(Float)
    Street = Column(String(100))
    adm_area = Column(String(100))
    district = Column(String(100))
    route_numbers = Column(String(100))
    station_name = Column(String(100))
    pavilion = Column(Boolean)
    operating_org_name = Column(String(100))
    entry_state = Column(String(100))
    global_id = Column(Integer)
    geodata_center = Column(Geometry('POINT'))

    '''def __init__(self, name, begin_date, end_date):
        self.name = name
        self.begin_date = begin_date
        self.end_date = end_date

    def __repr__(self):
        return f"<Stocks(name={self.name}, " \
               f"begin_date={self.begin_date}," \
               f" end_date={self.end_date})>" '''


class Apartment(base):
    __tablename__ = 'apartments'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    geodata_center = Column(Geometry('POINT'))

    '''def __init__(self, name, all_period, from_date, till_date):
        self.name = name
        self.all_period = all_period
        self.from_date = from_date
        self.till_date = till_date

    def __repr_(self):
        return f"Database(name={self.name}, " \
               f"all_period={self.all_period}" \
               f"from_date={self.from_date}, " \
               f"till_date={self.till_date})" '''


username = config.username
password = config.password
database = config.database
host = config.host
port = config.port


connection_string = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}'
engine = create_engine(connection_string, echo=False)

if database_exists(connection_string):
    print(f'Database exists: {database_exists(engine.url)}')
else:
    create_database(engine.url)
    print(f'Database created: {database_exists(engine.url)}')

session = Session(bind=engine, autoflush=False)


def create_db():
    base.metadata.create_all(engine)


data_stations = pd.read_excel('stations.xlsx')
data_stations.to_sql("stations", )

