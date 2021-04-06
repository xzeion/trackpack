#!/usr/bin/python3
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from database import Base
import uuid


class Package (Base):
    __tablename__ = 'package'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    delivered = Column(Boolean, nullable=False, default=True)
    eta = Column(DateTime, nullable=True)
    shipper = Column(UUID(as_uuid=True), ForeignKey('location.id'), nullable=False)
    reciever = Column(UUID(as_uuid=True), ForeignKey('location.id'), nullable=False)

    def __init__(self, shipper=None, reciever=None, eta=None):
        self.shipper = shipper
        self.reciever = reciever
        self.eta = eta

    def __repr(self):
        return f'<Packages {self.shipper},{self.reciever},{eta}>'


class History(Base):
    __tablename__ = 'history'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    #package = relationship("Package", foreign_keys="Packages.id")
    package = Column(UUID(as_uuid=True), ForeignKey('package.id'), nullable=False)
    arrival = Column(DateTime, nullable=False, default=datetime.utcnow)
    latitude = Column(Float(precision=5), nullable=False)
    longitude = Column(Float(precision=5), nullable=False)

    def __init__(self, package=None, arrival=None, latitude=None, longitude=None):
        self.package = package
        self.arrival = arrival
        self.latitude = latitude
        self.longitude = longitude

    def __repr(self):
        return f'<History {self.package},{self.arrival},{self.latitude},{self.logitude}>'


class Location(Base):
    __tablename__ = 'location'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(length=50), nullable=False)
    type = Column(String(length=7), nullable=False)
    latitude = Column(Float(precision=5), nullable=False)
    longitude = Column(Float(precision=5), nullable=False)
    #package = relationship("Package", back_populates="location")

    def __init__(self, name=None, type=None, latitude=None, longitude=None):
        self.name = name
        self.type = type
        self.latitude = latitude
        self.longitude = longitude

    def __repr(self):
        return f'<Location {self.name},{self.type},{self.latitude},{self.longitude}>'

