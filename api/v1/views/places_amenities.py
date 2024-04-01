#!/usr/bin/python3
"""Route for place_amenities objects"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def view_place_amenities(place_id):
    """Returns a list containing all Amenity objects from a particular place"""
    for place in storage.all(Place).values():
        if place.id == place_id:
            return jsonify([amenity.to_dict() for amenity in place.amenities])
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'],
                 strict_slashes=False)
def view_place_amenitie(place_id, amenity_id):
    """Deletes a Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if not place:
        raise abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        raise abort(404)

    if request.method == 'DELETE':
        if amenity not in place.amenities:
            raise abort(404)

        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200

    if request.method == 'POST':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200

        place.amenities.append(amenity)
        return jsonify(amenity.to_dict()), 201
