#!/usr/bin/python3
'''
This module contains the view for the restful API for the
state obj.
'''

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State


@app_views.route('/states')
def get_all_states():
    '''Returns the json object of all states in storage.'''
    all_states = storage.all(State)
    for state in all_states:
        state = state.to_dict()
    return jsonify(all_states)
