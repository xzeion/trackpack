#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_restful import Resource, reqparse, Api
from flask import Flask, Response
from db import Database
import pdb

app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True
api = Api(app)
db = Database()


class Create(Resource):

    def get(self):
        return "put endpoint instructions here"


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('shipper_name', type=str, required=True, help='')
        parser.add_argument('reciever_name', type=str, required=True, help='')
        parser.add_argument('shipper_address', type=str, required=True, help='')
        parser.add_argument('reciever_address', type=str, required=True, help='')
        print(parser.parse_args())

class Progress(Resource):


    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'id', type=str, required=True, 
            help='To check the progress of your package, please append the package id as an argument to the url.'
        )
        return parser.parse_args()


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'id', type=str, required=True, 
            help='To check the progress of your package, please append the package id as an argument to the url.'
        )
        #TODO: Allow the user to pass a standard address and use an external service to look up and store the lat long.
        parser.add_argument('lat', type=int, required=True, help='Latitude of location recieving the package')
        parser.add_argument('long', type=int, required=True, help='Longitude of location recieving the package')
        parser.add_argument('arrival', type=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f'),
                            help='When the package arrived if its not when the record is created. (0001-01-01T01:01:01.0)')
        return parser.parse_args()


class Update(Resource):


    def get(self):
        pass


    def post(self):
        pass


class Delivered(Resource):


    def get(self):
        pass


    def post(self):
        pass


api.add_resource(Create, '/api/v1/create')
api.add_resource(Progress, '/api/v1/progress')
api.add_resource(Update, '/api/v1/update')
api.add_resource(Delivered, '/api/v1/mark')

if __name__=="__main__":
    app.run(host='0.0.0.0', threaded=True, debug=True)
