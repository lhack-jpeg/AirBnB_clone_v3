#!/usr/bin/python3
'''
This module contains the view for the restful API for the
state obj.
'''

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State


@app_views.route('/states', method='GET')
def get_all_states():
    '''Returns the json object of all states in storage.'''
    state_list = []
    all_states = storage.all('State')
    for _state in all_states.values():
        state_list.append(_state.to_dict())

    return jsonify(state_list)


@app_views.route('/states/<state_id>', method='GET')
def get_one_state(state_id):
    '''Returns the one state in json or else the 404 page.'''
    result = storage.get(State, state_id)
    print(result)

    return jsonify({'status': 200})
