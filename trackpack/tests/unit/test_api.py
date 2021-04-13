#!/usr/bin/python3
# -*- coding: utf-8 -*-
#from pytest import set_trace as st

import requests
import json
import pytest

pytest.BASE_URL = 'http://127.0.0.1:5000'
pytest.pid = None

def test_package_creation():
    resp = requests.post(
        f'{pytest.BASE_URL}/api/v1/create',
        data={
            "shipper_name": "Delivery Dans Custom T's",
            "shipper_loc": "45.12345,54.54321",
            "reciever_name": "Brian Gratton",
            "reciever_loc": "43.34212,-83.88431"
        }
    )
    pytest.pid = resp.json()['PID']
    assert resp.status_code == 200

def test_adding_stop_to_package():
    resp = requests.post(
        f'{pytest.BASE_URL}/api/v1/progress',
        data={
            "name": "Delivery Daves",
            "location": "45.12345,54.54321",
            "id": pytest.pid
        }
    )
    # make sure package id matches
    assert pytest.pid == resp.json()['package_id']
    # make sure package is not yet delivered
    assert resp.json()['delivered'] == False
    assert resp.status_code == 200


def test_delivering_package_to_destination():
    resp = requests.post(
        f'{pytest.BASE_URL}/api/v1/progress',
        data={
            "name": "Brian Gratton",
            "location": "43.34212,-83.88431",
            "id": pytest.pid
        }
    )
    # Check the package moved to delivered when locations match
    assert resp.json()['delivered'] == True
    assert resp.status_code == 200

    
def test_get_package_history():
    resp = requests.get(f'{pytest.BASE_URL}/api/v1/progress?id={pytest.pid}')
    assert resp.status_code == 200
    data = resp.json()
    # Make sure the package id returned is the one we requested
    assert data['package_id'] == pytest.pid
    # Check that the final location in the history is the recievers location
    assert data['history'][-1]['location'] == data['reciever']['id']


def test_cant_add_stop_after_delivery():
    resp = requests.post(
        f'{pytest.BASE_URL}/api/v1/progress',
        data={
            "name": "Delivery Daves",
            "location": "45.12345,54.54321",
            "id": pytest.pid
        }
    )
    # Make sure we cant add another stop after a package has been delivered
    assert resp.json().get('ERROR') is not None
