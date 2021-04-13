#!/usr/bin/python3
# -*- coding: utf-8 -*-
# from pytest import set_trace as st


def test_create_new_location(new_shipper):
    '''
    GIVEN a set of locations
    CREATE a new package
    '''
    assert new_shipper.id


def test_create_new_package(new_package):
    '''
    GIVEN a set of locations
    CREATE a new package
    '''
    assert new_package


def test_create_new_history(new_history):
    '''
    GIVEN a set of locations
    CREATE a new package
    '''
    assert new_history
