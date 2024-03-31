#!/usr/bin/python3
""" Routes for handling City objects and there operations """
from api.v1.views import app_views
from models import storage
from models.state import City
from flask import jsonify, abort, request


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def get_cities(state_id):
    """
        Retrieves the list of all City objects of a State.
    :return: The json representation a all cities based on
    the state id. If the state_id is not found raises a 400 error.
    """
    state = storage.get('State', str(state_id))
    if state is None:
        abort(404)

    cities = []
    all_cities = storage.all("City")
    for city in all_cities.values():
        if city.to_dict()['state_id'] == state_id:
            cities.append(city.to_dict())

    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """
        Gets a specific City object by its ID.
    :param city_id: the id of a state object
    :return: The json representation a City based on its id.
                 if id not found raises a 400 error.
    """
    city = storage.get('City', str(city_id))
    if city is None:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """
        Deletes a State by its id
    :param city_id: the id of a state object
    :return: An empty dict with 200 or 404 if not found
    """
    target_object = storage.get("City", city_id)

    if target_object is None:
        abort(404)

    storage.delete(target_object)
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """
        Creates a City route based on a state id.
    :return: a newly created City object.
    """
    # Check If the state_id is not linked to any State object
    state = storage.get('State', str(state_id))
    if state is None:
        abort(404)

    data = request.get_json(silent=True)
    # Check if request body is valid JSON
    if data is None:
        abort(400, "Not a JSON")

    # Check if key name exists
    if 'name' not in data:
        abort(400, "Missing name")

    # Create a new City object
    data['state_id'] = state_id
    new_city = City(**data)
    new_city.save()
    response = jsonify(new_city.to_dict())
    response.status_code = 201
    return response


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
        Updates a specific City object based on its ID.
    :param city_id: the state object ID
    :return: City object and 200 on success, or 400 or 404 on failure.
    """
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')

    city_obj = storage.get("City", str(city_id))
    if city_obj is None:
        abort(404)
    for key, val in data.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city_obj, key, val)
    city_obj.save()
    return jsonify(city_obj.to_dict())
