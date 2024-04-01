#!/usr/bin/python3
"""
New view for place objects that handles default Restful API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.place import Place
from models.city import City
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def getAllPlaces(city_id):
    """Retrieves all Place objects of City"""
    place_list = []
    all_places = storage.all('Place')

    get_city = storage.get("City", city_id)
    if get_city is None:
        abort(404)

    for item in all_places.values():
        if item.city_id == city_id:
            place_list.append(item.to_dict())

    return jsonify(place_list)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def getPlace(place_id):
    """return place object matching place_id """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['DELETE'])
def DEL_place(place_id):
    """delete a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    place.delete()
    storage.save()
    storage.close()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def POST_place(city_id):
    """adds a place"""
    post_content = request.get_json()

    if not request.is_json:
        abort(400, "Not a JSON")

    name = post_content.get('name')
    if not name:
        abort(400, "Missing name")

    user_id = post_content.get('user_id')
    if not user_id:
        abort(400, "Missing user_id")

    user = storage.get("User", user_id)
    if user is None:
        abort(404)

    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    new_place = Place(**post_content)
    new_place.city_id = city_id
    storage.new(new_place)
    new_place.save()
    storage.close()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def PUT_place(place_id):
    """updates place object"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    update_content = request.get_json()
    if not request.is_json:
        abort(400, "Not a JSON")

    ignore_keys = ["id", "city_id", "user_id",
                   "created_at", "updated_at"]

    for key, val in update_content.items():
        if key not in ignore_keys:
            setattr(place, key, val)
    place.save()
    storage.close()
    return jsonify(place.to_dict()), 200
