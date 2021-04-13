#!/usr/bin/python3
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint, Table
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from dataclasses import dataclass
from trackpack.database import Base
import uuid

dt_format='%Y-%m-%dT%H:%M:%S.%f'

shipper_association = Table( 'shipper_association', Base.metadata,
    Column('location', UUID(as_uuid=True), ForeignKey('location.id')),
    Column('package', UUID(as_uuid=True), ForeignKey('package.id'))
                    
)
reciever_association = Table( 'reciever_association', Base.metadata,
    Column('location', UUID(as_uuid=True), ForeignKey('location.id')),
    Column('package', UUID(as_uuid=True), ForeignKey('package.id'))
                    
)

class Location(Base):
    __tablename__ = 'location'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(length=64), nullable=False)
    latitude = Column(Float(decimal_return_scale=5), nullable=False)
    longitude = Column(Float(decimal_return_scale=5), nullable=False)
    __table_args__ = (UniqueConstraint('name', 'latitude', 'longitude', name='_location_uc'),)

    def __init__(self, name=None, latitude=None, longitude=None):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f'<Location {self.name}>'


class Package (Base):
    __tablename__ = 'package'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    delivered = Column(Boolean, nullable=False, default=False)
    eta = Column(DateTime, nullable=True)
    shipper = relationship(
        'Location',
        backref='shipper',
        secondary=shipper_association,
        lazy='dynamic')
    reciever = relationship(
        'Location',
        backref='reciever',
        secondary=reciever_association,
        lazy='dynamic')
    history = relationship('History', backref='package_history', uselist=False)

    def __init__(self, id=None, shipper=None, reciever=None, eta=None):
        self.id = id
        self.shipper = shipper
        self.reciever = reciever
        self.eta = eta

    def __repr__(self):
        return f'<Packages {self.id}>'


class History(Base):
    __tablename__ = 'history'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    arrival = Column(DateTime, nullable=False, default=datetime.utcnow)
    package = Column(UUID(as_uuid=True), ForeignKey('package.id'), nullable=False)
    location = Column(UUID(as_uuid=True), ForeignKey('location.id'), nullable=True)


    def __init__(self, id=None, package=None, arrival=None, location=None):
        self.id = id
        self.package = package
        self.arrival = arrival
        self.location = location

    def __repr__(self):
        return f'<History {self.id} :: {self.package}>'


class LocationSchema(SQLAlchemySchema):
    class Meta:
        model = Location
        load_instance = True

    id = auto_field()
    name = auto_field()
    latitude = auto_field()
    longitude = auto_field()


class HistorySchema(SQLAlchemySchema):
    class Meta:
        model = History
        load_instance = True

    arrival = auto_field()
    location = auto_field()

class PackageSchema(SQLAlchemySchema):
    class Meta:
        model = Package
        include_relationships = True
        load_instance = True

    created_at = auto_field()
    updated_at = auto_field()
    delivered = auto_field()
    eta = auto_field()
