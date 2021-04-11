#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, Api
from flask import Flask, Response, jsonify
from database import db_session as dbs
from models import Package, History, Location
from datetime import datetime
import logging 

app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True
api = Api(app)

logging.basicConfig(
    level=logging.DEBUG,
    format = f'%(levelname)s: %(message)s')
log = app.logger.debug

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


def location(l):
    # returns lat lon in a list as floats
    return [float(x) for x in l.split(',')]


class Create(Resource):

    def get(self):
        raise Exception
        return "put endpoint instructions here"

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('shipper_name', type=str, required=True, help='Name of the shipper')
        parser.add_argument('reciever_name', type=str, required=True, help='Name of the reciever')
        parser.add_argument('shipper_loc', type=str, required=True,
                            help='Five decimal place lat/long location as a comma seperated string "45.12345,45.54321"')
        parser.add_argument('reciever_loc', type=str, required=True,
                            help='Five decimal place lat/long location as a comma seperated string "45.12345,45.54321"')
        args = parser.parse_args()
        log('Args Parsed')

        lat, lon = location(args.shipper_loc)
        shipper = get_or_create(
            Location,
            name=args.shipper_name,
            type='ship',
            latitude=lat,
            longitude=lon )
        log(f'Shipper Id: {shipper.id}')

        lat, lon = location(args.reciever_loc)
        reciever = get_or_create(
            Location,
            name = args.reciever_name,
            type='recieve',
            latitude=lat,
            longitude=lon )
        log(f'Reciever Id: {reciever.id}')

        package = get_or_create_package(
            shipper=shipper,
            reciever=reciever
        )
        log(f'Package Id: {package.id}')

        history = get_or_create(
            History,
            package=package.id,
            location=shipper.id )
        log(f'History Id: {history.id}')

        return {'Success': f'New Package Added, PID: {package.id}'}


class Progress(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, required=True,
                            help='To check the progress of your package, please append the package id as an argument to the url.')
        args = parser.parse_args()
        history = History.query.filter(History.package == args.id)
        return jsonify(history)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, required=True,
                            help='To check the progress of your package, please append the package id as an argument to the url.')
        parser.add_argument('lat', type=int, required=True, help='Latitude of location recieving the package')
        parser.add_argument('long', type=int, required=True, help='Longitude of location recieving the package')
        parser.add_argument('arrival', type=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f'),
                            help='When the package arrived if its not when the record is created. (0001-01-01T01:01:01.0)')

        # Get or create sender/reciver location
        # Create new history element for package
        # if package current location matches reciever mark package as delivered.
        return parser.parse_args()

        Response()


api.add_resource(Create, '/api/v1/create')
api.add_resource(Progress, '/api/v1/progress')

if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True, debug=True)
