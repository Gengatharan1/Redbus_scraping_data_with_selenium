from sqlalchemy import (
    create_engine, Column, Integer, String, DateTime, Date, Float,
    MetaData, BigInteger
    )
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
username = os.environ.get('sql_db_usr') 
password = os.environ.get('sql_db_pwd')
hostname = 'localhost'
port = os.environ.get('sql_db_endpoint') 
database = os.environ.get('sql_db_dbname')


# postgresql
db_url = f'postgresql+psycopg2://{username}:{password}@{hostname}:{port}/{database}'


# Create engine
engine = create_engine(db_url)


# Create a base class for your ORM models
Base = declarative_base()


# Define ORM model
class States(Base):
    __tablename__ = 'states'

    state = Column(String, primary_key=True)
    state_link = Column(String)


class Routes(Base):
    __tablename__ = 'routes'

    route_name = Column(String, primary_key=True)
    state = Column(String)
    route_link = Column(String)


class Buses(Base):
    __tablename__ = 'buses'

    bus_id = Column(String, primary_key=True)
    bus_name = Column(String)
    bus_type = Column(String)
    dur = Column(String)
    date_dep = Column(Date)
    date_arrival = Column(Date)
    time_dep = Column(DateTime)
    time_arrival = Column(DateTime)
    star_rate = Column(Float)
    price = Column(Integer)
    seat_available = Column(Integer)
    route_name = Column(String)
    loc_dep = Column(String)
    loc_arrival = Column(String)
    operator = Column(String)


def sql():
    print(db_url)
    
    # Create the tables in the database
    Base.metadata.create_all(engine)

    # Create a session maker
    Session = sessionmaker(bind=engine)
    session = Session()
    return session, engine

if __name__ == '__main__':
    pass