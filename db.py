import requests
import sqlite3
import datetime
import pytz
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

engine = create_engine('sqlite:///monitors.db', echo=True)
Base = declarative_base()


class Monitors(Base):
    __tablename__ = 'monitors'

    def __init__(self, label, cost, frequency, diagonal, model):
        self.label = label
        self.cost = cost
        self.frequency = frequency
        self.diagonal = diagonal
        self.model = model

    id = Column(Integer, primary_key=True)
    label = Column(String)
    frequency = Column(Integer)
    cost = Column(Integer)
    diagonal = Column(Integer)
    model = Column(String)


def find_int(type, value, sign='=='):

    if eval('session.query(exists().where(Monitors.{} {} {})).scalar()'.format(type, sign, value)):
        return eval('session.query(Monitors).filter(Monitors.{} {} {}).all()'.format(type, sign, value))


def find_str(type, value, sign='=='):
    if eval('session.query(exists().where(Monitors.{} == "{}")).scalar()'.format(type, value)):
        return eval('session.query(Monitors).filter(Monitors.{} == "{}").all()'.format(type, value))


def create(label, cost, frequency, model, diagonal):
    session.add(Monitors(label=label, cost=cost, frequency=frequency, model=model, diagonal=diagonal))
    session.commit()


def get_all():
    return session.query(Monitors).all()


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
