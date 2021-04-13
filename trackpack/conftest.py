#!/usr/bin/python3
# -*- coding: utf-8 -*-

from os import environ as env
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from trackpack.models import Location, Package, History
from datetime import datetime, timedelta
import pytest
# from pytest import set_trace as st


@pytest.fixture(scope='session')
def engine():
    return create_engine(
        f'postgresql://{env.get("DBUSER")}:{env.get("POSTGRES_PASSWORD")}@{env.get("HOST")}/{env.get("DBNAME")}',
        client_encoding='utf8',
        echo=False
    )


@pytest.fixture(scope='session')
def tables(engine):
    BaseModel = declarative_base()
    BaseModel.metadata.create_all(engine)
    yield
    BaseModel.metadata.drop_all(engine)


@pytest.fixture(scope='session')
def dbsession(engine, tables):
    '''Returns sqlalchemy session, and after the test tears down everything properly'''
    connection = engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    session = Session(bind=connection)

    yield session

    session.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()


@pytest.fixture(scope='module')
def new_shipper(dbsession):
    shipper = Location('Pytest shipper', latitude=45.12345, longitude=54.54321)
    dbsession.add(shipper)
    dbsession.commit()
    return shipper


@pytest.fixture(scope='module')
def new_reciever(dbsession):
    reciever = Location('Pytest reciever', latitude=45.54321, longitude=54.12345)
    dbsession.add(reciever)
    dbsession.commit()
    return reciever


@pytest.fixture(scope='module')
def new_package(dbsession, new_shipper, new_reciever):
    package = Package(
        shipper=[new_shipper],
        reciever=[new_reciever],
        eta=(datetime.now() + timedelta(days=5)))
    dbsession.add(package)
    dbsession.commit()
    return package


@pytest.fixture(scope='module')
def new_history(dbsession, new_package, new_reciever):
    history = History(package=new_package.id, location=new_reciever.id)
    dbsession.add(history)
    dbsession.commit()
    return history
