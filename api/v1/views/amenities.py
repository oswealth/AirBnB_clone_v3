#!/usr/bin/python3
""" Routes for handling Amenity objects and there operations """
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """
        Retrieves the list of all Amenity objects.
    :return: The json representation all amenities.
        If the amenity_id is not found raises a 400 error.
    """
    amenities = []
    amenity_objects = storage.all("Amenity")
    for obj in amenity_objects.values():
        amenities.append(obj.to_dict())

    return jsonify(amenities)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """
        Gets a specific Amenity object by its ID.
    :param amenity_id: the id of the amenity object
    :return: The json representation of an Amenity based on its id.
                 if id not found raises a 400 error.
    """
    amenity = storage.get('Amenity', str(amenity_id))
    if amenity is None:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
        Deletes an Amenity object by its id
    :param amenity_id: the id of the amenity object
    :return: An empty dict with 200 or 404 if not found
    """
    target_object = storage.get("Amenity", amenity_id)

    if target_object is None:
        abort(404)

    storage.delete(target_object)
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """
        Creates an Amenity route based on a amenity id.
    :return: a newly created Amenity object.
    """
    data = request.get_json(silent=True)
    # Check if request body is valid JSON
    if data is None:
        abort(400, "Not a JSON")

    # Check if key name exists
    if 'name' not in data:
        abort(400, "Missing name")

    # Create a new Amenity object
    new_amenity = Amenity(**data)
    new_amenity.save()
    response = jsonify(new_amenity.to_dict())
    response.status_code = 201
    return response


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id=None):
    """
        Updates a specific Amenity object based on its ID.
    :param amenity_id: the amenity object ID
    :return: amenity object and 200 on success, or 400 or 404 on failure.
    """
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')

    amenity_obj = storage.get("Amenity", str(amenity_id))
    if amenity_obj is None:
        abort(404)
    for key, val in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity_obj, key, val)
    amenity_obj.save()
    return jsonify(amenity_obj.to_dict())
