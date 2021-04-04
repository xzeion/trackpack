#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_restful import Resource, reqparse, Api
from flask import Flask, Response
#from db import Database
import pdb

app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True
api = Api(app)
#db = Database()


class Create(Resource):

    def get(self):
        return "Hello Flask World!"


    def post(self):
        pass

class Progress(Resource):


    def get(self):
        pass


    def post(self):
        pass


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
