#!/usr/bin/python3
# -*- coding: utf-8 -*-
#from pytest import set_trace as st


def test_create_new_location(new_shipper):
    assert new_shipper.id is not None


def test_create_new_package(new_package):
    assert new_package.id is not None


def test_create_new_history(new_history):
    assert new_history is not None
