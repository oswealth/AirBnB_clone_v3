#!/usr/bin/python3
""" This is the main app """
from flask import Flask, jsonify
<<<<<<< HEAD
from api.v1.views import app_views
from os import getenv
=======
>>>>>>> 7c5727d93da252d385ecb5af6ef5646a5a9879a7
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask('__name__')
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exception=None):
    """
        This is a teardown function
    """
    storage.close()


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
