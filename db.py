from sqlalchemy import Column, Integer, Float, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database
from geoalchemy2 import Geometry
import pandas as pd
from shapely import wkb

import config


base = declarative_base()


class Station(base):
    __tablename__ = 'stations'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    longitude = Column(Float)
    latitude = Column(Float)
    geodata_center = Column(Geometry('POINT'))


class Apartment(base):
    __tablename__ = 'apartments'

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    geodata_center = Column(Geometry('POINT'))


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
    delete_tables()
    base.metadata.create_all(engine)
    data_apartments = pd.read_excel('apartments.xlsx')
    data_stations = pd.read_excel('stations.xlsx')
    mas_stations = data_stations.reset_index().values.tolist()
    for i in range(len(mas_stations)):
        mas_stations[i].append('POINT(' + str(mas_stations[i][2]) + ' ' + str(mas_stations[i][3]) + ')')
        session.add(Station(name=mas_stations[i][1],
                            longitude=mas_stations[i][2],
                            latitude=mas_stations[i][3],
                            geodata_center=mas_stations[i][4]))
        session.commit()

    mas_apartments = data_apartments.reset_index().values.tolist()
    for i in range(len(mas_apartments)):
        session.add(Apartment(name=mas_apartments[i][1],
                              geodata_center=mas_apartments[i][2]))
        session.commit()


def delete_tables():
    session.commit()
    Station.__table__.drop(engine, checkfirst=True)
    Apartment.__table__.drop(engine, checkfirst=True)


def get_dict_apartments() -> dict:
    response = session.query(Apartment.name, Apartment.geodata_center).all()
    dct = {}
    for row in response:
        point = wkb.loads(bytes(row.geodata_center.data))
        dct[row.name] = [point.x, point.y]
    return dct


def get_dict_stations() -> dict:
    response = session.query(Station.name, Station.geodata_center).all()
    dct = {}
    for row in response:
        point = wkb.loads(bytes(row.geodata_center.data))
        dct[row.name] = [point.x, point.y]
    session.commit()
    return dct
