from flask import Flask, render_template, jsonify, request, Response, url_for
from functools import wraps
import requests
import json
import sys
import logging
import os


#DEBUG = False
DEBUG = True

app = Flask(__name__)


def get_request(data_type):
    payload = {'rdf:type': "frameworx:" + data_type,
               'acl:consumerKey': os.environ["FRAMEWORX_KEY"]}
    return requests.get("https://api.frameworxopendata.jp/api/v3/datapoints", params=payload)


def write_data(data_type):
    data = get_request(data_type)
    with open(data_type + ".json", 'w') as f:
        json.dump(data.json(), f)


def check_auth(username, password):
    return username == os.environ["APP_USER"] and password == os.environ["APP_PASS"]


def authenticate():
    return Response(
        'Could not verify your access level for that URL.\n',
        401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/_step_graph', methods=["GET", "POST"])
@requires_auth
def _step_graph():
    return jsonify({"test": "aaa"})


@app.route('/_get_key', methods=["GET"])
@requires_auth
def _get_key():
    return jsonify({"key": os.environ["FRAMEWORX_KEY"]})


@app.route("/")
@requires_auth
def index():
    return render_template("index.html")


if __name__ == "__main__":
    for data_type in ["WarehouseVital", "WarehouseActivity"]:
        write_data(data_type)

    app.debug = True
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    if DEBUG:
        app.run(host="0.0.0.0", debug=True)
    else:
        app.run(debug=True)

