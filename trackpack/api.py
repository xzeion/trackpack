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


class Orm:

    @classmethod
    def location(self, name, type, loc):
        lat, lon = [float(x) for x in loc.split(',')]
        loc = Location(
            name=name,
            type=type,
            latitude=lat,
            longitude=lon)
        try:
            dbs.add(loc)
            dbs.commit()
        except Exception:
            dbs.rollback()

        # NOTE: Because sqlalchemy can not return the record uuid
        # before creation, we commit and then query for the record.
        return Location.query.filter(
            Location.latitude == lat,
            Location.longitude == lon
        ).first().id

    @classmethod
    def package(self, sid, rid):
        pac = Package(shipper=sid, reciever=rid)
        dbs.add(pac)
        dbs.commit()

        return Package.query.filter(
            Package.shipper == sid,
            Package.reciever == rid
        ).first().id

    @classmethod
    def history(self, pid, sid):
        his = History(package=pid, location=sid)
        dbs.add(his)
        dbs.commit()

        return History.query.filter(
            History.package == pid
            #History.location == sid
        ).first().id


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

        shipper_id = Orm.location(args.shipper_name, 'ship', args.shipper_loc)
        reciever_id = Orm.location(args.reciever_name, 'recieve', args.reciever_loc)

        pid = Orm.package(shipper_id, reciever_id)
        history = Orm.history(pid, reciever_id)

        # Create sender and reciever locations
        # Create package
        # Create Initial History entry.
        return {'Success': f'Created new package to database {history}'}


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
