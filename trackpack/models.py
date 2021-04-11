#!/usr/bin/python3
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint, Table
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from dataclasses import dataclass
from database import Base
import uuid

dt_format='%Y-%m-%dT%H:%M:%S.%f'

association = Table( 'association', Base.metadata,
    Column('location', UUID(as_uuid=True), ForeignKey('location.id')),
    Column('package', UUID(as_uuid=True), ForeignKey('package.id'))
                    
)

class Location(Base):
    __tablename__ = 'location'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(length=64), nullable=False)
    type = Column(String(length=7), nullable=False)
    latitude = Column(Numeric(7,5), nullable=False)
    longitude = Column(Numeric(7,5), nullable=False)
    __table_args__ = (UniqueConstraint('latitude', 'longitude', 'type', name='_location_uc'),)

    def __init__(self, name=None, type=None, latitude=None, longitude=None):
        self.name = name
        self.type = type
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f'<Location {self.name},{self.type},{self.latitude},{self.longitude}>'


class Package (Base):
    __tablename__ = 'package'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    delivered = Column(Boolean, nullable=False, default=False)
    eta = Column(DateTime, nullable=True)
    shipper = relationship(
        'Location',
        backref='package_shipper',
        overlaps='reciever, package',
        #primaryjoin="and_(Package.shipper == Location.id)",
        secondary=association,
        lazy='dynamic')
    reciever = relationship(
        'Location',
        backref='package_recipiant',
        overlaps='shipper, package',
        #primaryjoin="and_(Package.reciever == Location.id)",
        secondary=association,
        lazy='dynamic')
    history = relationship('History', backref='package_history', uselist=False)

    def __init__(self, shipper=None, reciever=None, eta=None):
        self.shipper = shipper
        self.reciever = reciever
        self.eta = eta

    def __repr__(self):
        return f'<Packages {self.shipper},{self.reciever},{self.eta}>'


class History(Base):
    __tablename__ = 'history'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    arrival = Column(DateTime, nullable=False, default=datetime.utcnow)
    package = Column(UUID(as_uuid=True), ForeignKey('package.id'), nullable=False)
    location = Column(UUID(as_uuid=True), ForeignKey('location.id'), nullable=True)


    def __init__(self, package=None, arrival=None, location=None):
        self.package = package
        self.arrival = arrival
        self.location = location

    def __repr__(self):
        return f'<History {self.package},{self.arrival},{self.location}>'

