#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_restful import Resource, reqparse, Api
from flask import Flask, Response
from database import db_session as dbs
from models import Package, History, Location
from datetime import datetime

app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True
api = Api(app)


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

        latitude, longitude = args.shipper_loc.split(',')
        shipper_loc = Location.query.filter(
            Location.latitude == latitude,
            Location.longitude == longitude
        )
        dbs.add(Location(args.shipper_name, 'shipper', latitude, longitude))
        dbs.commit()

        latitude, longitude = args.reciever_loc.split(',')
        reciever_loc = Location.query.filter(
            Location.latitude == latitude,
            Location.longitude == longitude
        )
        if not reciever_loc:
            dbs.add(Location(args.reciever_name, 'reciever', latitude, longitude))
            dbs.commit()
         
        # Create sender and reciever locations
        # Create package
        # Create Initial History entry.
        return Location.query.all().first()


class Progress(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, required=True,
                            help='To check the progress of your package, please append the package id as an argument to the url.')
        # Return all history elements related to package and delivery bool
        return parser.parse_args()

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
