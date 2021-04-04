#!/usr/bin/env python
# -*- coding: utf-8 -*-
# A simple helper class to make managing sqlalchemy connections
# simpler and assure no code replication.

import sqlalchemy
from os import environ as env
from sqlalchemy import create_engine, MetaData, schema
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class Database():

    def __init__(self):
        self.engine = create_engine(
            f'postgresql://{env.get("DBUSER")}:{env.get("POSTGRES_PASSWORD")}@{env.get("HOST")}/{env.get("DBUSER")}',
            client_encoding='utf8',
            echo=False
        )
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.conn = self.engine.connect()


    def execute(self, data, table_name=None, schema=None):
        if table_name:
            table = sqlalchemy.Table(
                table_name,
                sqlalchemy.schema.MetaData(
                    bind=self.engine,
                    schema=schema or "public"
                ),
                autoload=True
            ) 
            self.conn.execute(table.insert(), data)
        else:
            self.conn.execute(data)


    def commit(self):
        self.session.commit()


    def close(self):
        self.session.close()
        self.conn.close()
