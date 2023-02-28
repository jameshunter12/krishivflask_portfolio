from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.activitypick import activities

activity_api = Blueprint('activity_api', __name__,
                   url_prefix='/api/activities')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(activity_api)

class activityAPI:        
    class _Create(Resource):
        def rents(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 210
            # validate uid
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 210
            # look for password and dob
            address = body.get('address')
            if address is None or len(address) < 0:
                return {'message': f'address is missing, or is less than 2 characters'}, 210
            coordinates = body.get('coordinates')
            if coordinates is None or len(coordinates) < 1:
                return {'message': f'coordinates is missing, or is less than 2 characters'}, 210
            fun = body.get('fun')
            if fun is None or len(fun) < 1:
                return {'message': f'fun is missing, or is less than 2 characters'}, 210
            
    

            ''' #1: Key code block, setup USER OBJECT '''
            uo = activities(name=name, 
                      uid=uid)
            
            ''' Additional garbage error checking '''
            # set password if provided
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            activity = uo.create()
            # success returns json of user
            if activity:
                return jsonify(activity.read())
            # failure returns error
            return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 210

    class _Read(Resource):
        def get(self):
            activities = activities.query.all()    # read/extract all users from database
            json_ready = [activities.read() for users in activities]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    class _Security(Resource):

        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Get Data '''
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            address = body.get('address')

            ''' Find user '''
            user = activities.query.filter_by(_uid=uid).first()
            if user is None or not user.is_address(address):
                return {'message': f"Invalid user id or password"}, 400
            
            ''' authenticated user '''
            return jsonify(user.read())

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
    # api.add_resource(_Security, '/authenticate')
