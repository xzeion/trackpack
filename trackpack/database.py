#!/usr/bin/python3
# -*- coding: utf-8 -*-

from os import environ as env
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
#from flask.ext.jsontools import JsonSerializableBase

engine = create_engine(
    f'postgresql://{env.get("DBUSER")}:{env.get("POSTGRES_PASSWORD")}@{env.get("HOST")}/{env.get("DBNAME")}',
    client_encoding='utf8',
    echo=False
)

db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)

#Base = declarative_base(cls=(JsonSerializableBase,))
Base = declarative_base()

Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)
