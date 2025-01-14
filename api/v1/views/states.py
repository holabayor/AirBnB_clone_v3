#!/usr/bin/python3
""" view for states objects """

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Retrieves the list of all State objects"""
    all_states = storage.all(State)
    states = []
    for state in all_states.values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """Retrieves a State objects"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State objects"""
    state = storage.get(State, state_id)
    if state:
        state.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State objects"""
    try:
        data = request.get_json()
        if data.get("name") is None:
            return make_response(jsonify({"error": "Missing name"}), 400)
        state = State(**data)
        state.save()
        response = jsonify(state.to_dict())
        response.status_code = 201
        return response
    except Exception:
        return make_response(jsonify({"error": "Not a JSON"}), 400)


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """Updates a State objects"""
    try:
        data = request.get_json()
        state = storage.get(State, state_id)
        for key, value in data.items():
            if key in ['id', 'created_at', 'updated_at']:
                continue
            setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict())
    except KeyError:
        abort(404)
    except Exception:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
