#!/usr/bin/python3
"""
users route module
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def getAllUsers():
    """Retrieves the list of all User objects"""
    retval = []
    all_users = storage.all('User')
    for item in all_users.values():
        retval.append(item.to_dict())
    return jsonify(retval)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def GET_user(user_id):
    """GET User object, else raise 404"""

    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=['DELETE'])
def DEL_user(user_id):
    """ delete a user object """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)

    user.delete()
    storage.save()
    storage.close()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def POST_user():
    """adds user, raise 400 if not valid json"""
    post_content = request.get_json()

    if not request.is_json:
        abort(400, "Not a JSON")

    email = post_content.get('email')
    if not email:
        abort(400, "Missing email")

    password = post_content.get('password')
    if not password:
        abort(400, "Missing password")

    new_user = User(**post_content)
    storage.new(new_user)

    new_user.save()
    storage.close()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def PUT_user(user_id):
    """Update user, raise 404 if none, raise 400 if not json"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)

    ignore_keys = ["id", "created_at", "updated_at", "email"]

    content = request.get_json()

    if not request.is_json:
        abort(400, "Not a JSON")

    for key, val in content.items():
        if key not in ignore_keys:
            setattr(user, key, val)

    user.save()
    storage.close()

    return jsonify(user.to_dict()), 200
