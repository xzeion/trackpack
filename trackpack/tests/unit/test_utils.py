#!/usr/bin/python3
# -*- coding: utf-8 -*-
# from pytest import set_trace as st

from trackpack.utils import get_or_create, get_or_create_package, location, valid_uuid, error_resp
from trackpack.models import Location


def test_get_or_create_locations_and_package():
    shipper = get_or_create(
        Location,
        name='Shipper',
        latitude=12.34567,
        longitude=76.54321)
    assert shipper.id is not None

    reciever = get_or_create(
        Location,
        name='Reciever',
        latitude=23.45678,
        longitude=87.76543)
    assert reciever.id is not None

    package = get_or_create_package(
        shipper=shipper,
        reciever=reciever
    )
    assert package.id is not None


def test_lat_lon_parser():
    resp = location('12.12345,-53.14253')
    assert type(resp[0]) is float and type(resp[1]) is float
    assert len(resp) == 2


def test_uuid_validity_check():
    invalid = valid_uuid('12345')
    valid = valid_uuid('12f7becd-96ca-4051-bd42-2873ea0f6aac')
    assert invalid is False
    assert valid is True


def test_error_resp_message_genarator():
    resp = error_resp('Your simple error message here')
    assert resp.status_code == 400
