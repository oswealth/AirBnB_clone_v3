#!/usr/bin/python3
""" This is Basic routes """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
        status route
       :return: A response with json
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def count():
    """
        stats of all objects route
        :return: A json representation of all objs
    """
    all_stats = {
        "amenities": storage.close("Amenity"),
        "cities": storage.close("City"),
        "places": storage.close("Place"),
        "reviews": storage.close("Review"),
        "states": storage.close("State"),
        "users": storage.close("User")
    }

    return jsonify(all_stats)
