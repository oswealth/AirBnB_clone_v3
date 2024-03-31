#!/usr/bin/python3
""" Routes for handling State objects and there operations """
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def all_states():
    """
        retrieves all State objects.
    :return: The json representation of states.
    """
    states = []
    state_objects = storage.all("State")
    for obj in state_objects.values():
        states.append(obj.to_dict())

    return jsonify(states)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """
        Gets a specific State object by its ID.
    :return: The json representation a states based on its id.
             if id not found raises a 400 error.
    """
    state = storage.get('State', str(state_id))
    if state is None:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
        Deletes a State by its id
    :param state_id: the id of a state object
    :return: An empty dict with 200 or 404 if not found
    """
    target_object = storage.get("State", state_id)

    if target_object is None:
        abort(404)

    storage.delete(target_object)
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
        Creates a state route
    :return: a newly created state object.
    """
    data = request.get_json(silent=True)
    # Check if request body is valid JSON
    if data is None:
        abort(400, "Not a JSON")

    # Check if key name exists
    if 'name' not in data:
        abort(400, "Missing name")

    # Create a new State object
    new_state = State(**data)
    new_state.save()
    response = jsonify(new_state.to_dict())
    response.status_code = 201
    return response


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id=None):
    """
        Updates a specific State object based on its ID.
    :param state_id: the state object ID
    :return: state object and 200 on success, or 400 or 404 on failure.
    """
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')
    state_obj = storage.get("State", str(state_id))
    if state_obj is None:
        abort(404)
    for key, val in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state_obj, key, val)
    state_obj.save()
    return jsonify(state_obj.to_dict())
