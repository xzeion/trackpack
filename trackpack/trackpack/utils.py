from flask import Response
from trackpack.database import db_session as dbs
from models import Package
import uuid
import json


def get_or_create(model, defaults=None, **k):
    instance = dbs.query(model).filter_by(**k).one_or_none()
    if instance:
        return instance
    else:
        k |= defaults or {}
        instance = model(**k)
        try:
            dbs.add(instance)
            dbs.commit()
        except Exception:
            dbs.rollback()
            instance = dbs.query(model).filter_by(**k).one()
            return instance
        else:
            return instance


def get_or_create_package(package_id=None, shipper=None, reciever=None):
    if package_id:
        return dbs.query(Package).filter(id == id).one_or_none()
    package = Package(
        shipper=[shipper],
        reciever=[reciever])
    dbs.add(package)
    dbs.commit()
    return package


def location(loc):
    # returns lat lon in a list as floats
    return [float(x) for x in loc.split(',')]


def valid_uuid(id):
    try:
        uuid.UUID(id)
        return True
    except ValueError:
        return False


def error_resp(message):
    return Response(
        json.dumps({'ERROR': message}),
        status=400, mimetype='application/json')
