# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify, request, Response, url_for
from functools import wraps
import json
import sys
import logging
import os
import graph
import personal
import requests
import shutil

# DEBUG = False
DEBUG = True

app = Flask(__name__)


def get_request(payload):
    payload['acl:consumerKey'] = os.environ["FRAMEWORX_KEY"]
    return requests.get("https://api.frameworxopendata.jp/api/v3/datapoints", params=payload)


def write_data(data_type):
    payload = {'rdf:type': "frameworx:" + data_type}
    data = get_request(payload)
    with open(data_type + ".json", 'w') as f:
        json.dump(data.json(), f)


def write_map(map_name):
    payload = {'acl:consumerKey': os.environ["FRAMEWORX_KEY"]}
    r = requests.get("https://api.frameworxopendata.jp/api/v3/files/" + map_name, params=payload, stream=True)
    if r.status_code == 200:
        with open(map_name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)


def read_data(data_type):
    with open(data_type + ".json", 'r') as f:
        data = json.load(f)
    return data




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


@app.route('/_get_personal_data', methods=["POST"])
@requires_auth
def _get_personal_data():
    workerId = int(request.json[u'workerId'])
    category = request.json[u'category']
    data = personal.get_data(workerId, category)
    return jsonify(data=json.dumps(data))


@app.route('/_step_graph', methods=["GET", "POST"])
@requires_auth
def _step_graph():
    return jsonify({"test": "aaa"})

@app.route('/_item_ranking', methods=["GET"])
@requires_auth
def _item_ranking():
    return jsonify(graph.getLogData(os.environ["FRAMEWORX_KEY"]))

@app.route('/_cal_ranking', methods=["GET"])
@requires_auth
def _cal_ranking():
    return jsonify(graph.getVitalData(os.environ["FRAMEWORX_KEY"], "calorie"))

@app.route('/_step_ranking', methods=["GET"])
@requires_auth
def _step_ranking():
    return jsonify(graph.getVitalData(os.environ["FRAMEWORX_KEY"]), "step")

@app.route('/_get_key', methods=["GET"])
@requires_auth
def _get_key():
    return jsonify({"key": os.environ["FRAMEWORX_KEY"]})


@app.route("/")
@requires_auth
def index():
    return render_template("index.html")


@app.route("/index.html")
@requires_auth
def index_2():
    return render_template("index.html")


@app.route("/log.html")
@requires_auth
def log_page():
    return render_template("log.html")


@app.route("/ranking.html")
@requires_auth
def ranking_page():
    return render_template("ranking.html")


if __name__ == "__main__":
    for data_type in ["WarehouseVital", "WarehouseActivity"]:
        if not os.path.exists(data_type + ".json"):
            write_data(data_type)

    for map_name in ["warehouse_map_1.jpg", "warehouse_map_2.jpg"]:
        if not os.path.exists(map_name):
            write_map(map_name)

    app.debug = True
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    if DEBUG:
        app.run(host="0.0.0.0", debug=True)
    else:
        app.run(debug=True)

