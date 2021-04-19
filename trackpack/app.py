#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, Response
from flask_restful import Resource, reqparse, Api
from trackpack.database import db_session as dbs
from trackpack.models import Package, History, Location, PackageSchema, HistorySchema, LocationSchema
from trackpack.utils import get_or_create, get_or_create_package, location, valid_uuid, error_resp
from datetime import datetime
import logging 
import json

app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True
api = Api(app)

logging.basicConfig(
    level=logging.DEBUG,
    format = f'%(levelname)s: %(message)s')
log = app.logger.debug


class Create(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('shipper_name', type=str, required=True, help='Name of the shipper')
        parser.add_argument('reciever_name', type=str, required=True, help='Name of the reciever')
        parser.add_argument('shipper_loc', type=str, required=True,
                            help='Five decimal place lat/long location as a comma seperated string "45.12345,45.54321"')
        parser.add_argument('reciever_loc', type=str, required=True,
                            help='Five decimal place lat/long location as a comma seperated string "45.12345,45.54321"')
        parser.add_argument('eta', type=str, required=False,
                            help='A datetime representing the estimated time of arrival formatted as "YYYY-MM-DDTHH:MM:SS.00000"')
        args = parser.parse_args()
        log('Args Parsed')

        lat, lon = location(args.shipper_loc)
        shipper = get_or_create(
            Location,
            name=args.shipper_name,
            latitude=lat,
            longitude=lon )
        log(f'Shipper Id: {shipper.id}')

        lat, lon = location(args.reciever_loc)
        reciever = get_or_create(
            Location,
            name = args.reciever_name,
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

        return Response(json.dumps({
            'Success': 'New Package Added',
            'PID': str(package.id)
        }), status=200)


class Progress(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, required=True,
            help='To check the progress of your package, please append the package id as an argument to the url.')
        args = parser.parse_args()

        if not valid_uuid(args.id):
            return error_resp('Invalid UUID')
        pack = Package.query.get(args.id)
        if not pack:
            return error_resp('There is no package with that id')

        history = History.query.filter(History.package == args.id)
        return Response(json.dumps({
            'package_id': args.id,
            'package': PackageSchema().dump(pack),
            'shipper': LocationSchema().dump(pack.shipper.one()),
            'reciever': LocationSchema().dump(pack.reciever.one()),
            'history': HistorySchema(many=True).dump(history)
        }), status=200)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, required=True,
                            help='Id of package you are checking in.')
        parser.add_argument('name', type=str, required=True, help='Name of the facility recieving the package')
        parser.add_argument('location', type=str, required=True,
                            help='Five decimal place lat/long location as a comma seperated string "45.12345,45.54321"')
        parser.add_argument('arrival', type=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f'),
                            help='When the package arrived if different than current time. "YYYY-MM-DDTHH:MM:SS.00000"')
        args = parser.parse_args()

        if not valid_uuid(args.id):
            return error_resp('Invalid UUID')
        pack =  Package.query.get(args.id)
        if not pack:
            return error_resp('There is no package with that id')
        if pack.delivered:
            return error_resp('You can\'t add a stop to a package that has been delivered')

        lat, lon = location(args.location)
        loc = get_or_create(
            Location,
            name=args.name,
            latitude=lat,
            longitude=lon )

        history = get_or_create(
            History,
            package=args.id,
            location=loc.id )

        if pack.reciever.one().id == loc.id:
            pack.delivered = True
            pack.eta = history.arrival
            dbs.add(pack)
            dbs.commit()

        return Response(json.dumps({
            'check_in': 'successful',
            'package_id': args.id,
            'delivered': pack.delivered,
            **HistorySchema().dump(history)
        }), status=200)


api.add_resource(Create, '/api/v1/create')
api.add_resource(Progress, '/api/v1/progress')


if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True, debug=True)
