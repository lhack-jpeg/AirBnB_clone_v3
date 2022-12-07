#!/usr/bin/python3
'''
This module contains the view for the restful API for the
state obj.
'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    '''Returns the json object of all states in storage.'''
    state_list = []
    all_states = storage.all('State')
    for _state in all_states.values():
        state_list.append(_state.to_dict())

    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_one_state(state_id):
    '''Returns the one state in json or else the 404 page.'''
    result = storage.get(State, state_id)
    if result is None:
        abort(404)

    single_state_dict = result.to_dict()
    return jsonify(single_state_dict)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_one_state(state_id):
    '''Checks to see if state exists before deleting from db'''
    result = storage.get(State, state_id)
    if result is None:
        abort(404)

    storage.delete(result)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'])
def create_state():
    '''Creates a new state from the http body'''
    new_obj = request.get_json()
    '''If not json abort to 400 code'''
    if new_obj is None:
        abort(400, 'Not a JSON')

    '''If obj doesn't have key of name, abort 400'''
    if new_obj.get('name') is None:
        abort(400, 'Missing name')

    '''Create new obj, save to storage and return json obj.'''
    new_state = State(**new_obj)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    '''
    Updates state by id. Checks to make sure if it exists.
    Sends either 404 if states doesn't exists.
    Sends 400 if json in http body is bad.
    Ignores keys id, updated_at, created_at.
    '''
    new_attributes = request.get_json()
    if new_attributes is None:
        abort(400, 'Not a JSON')

    one_state = storage.get(State, state_id)
    if one_state is None:
        abort(404)

    skip_keys = ['id', 'created_at', 'updated_at']
    for key, value in new_attributes.items():
        if key in skip_keys:
            pass
        else:
            setattr(one_state, key, value)
    storage.save()
    return jsonify(one_state.to_dict()), 200
