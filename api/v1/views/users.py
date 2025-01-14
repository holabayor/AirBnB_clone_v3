#!/usr/bin/python3
""" view for users objects """

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """Retrieves a list of all User objects"""
    all_users = storage.all(User)
    users = []
    for user in all_users.values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if user:
        user.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User object"""
    try:
        data = request.get_json()
        if data.get("email") is None:
            return make_response(jsonify({"error": "Missing email"}), 400)
        if data.get("password") is None:
            return make_response(jsonify({"error": "Missing password"}), 400)
        user = User(**data)
        user.save()
        response = jsonify(user.to_dict())
        return make_response(response, 201)
    except Exception:
        return make_response(jsonify({"error": "Not a JSON"}), 400)


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    try:
        data = request.get_json()
        user = storage.get(User, user_id)
        for key, value in data.items():
            if key in ['id', 'email', 'created_at', 'updated_at']:
                continue
            setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict())
    except KeyError:
        abort(404)
    except Exception:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
