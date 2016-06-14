from flask import Flask, render_template, jsonify, request, Response, url_for
from functools import wraps
import requests
import json
import sys
import logging
import os
import dateutil.parser


#DEBUG = False
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
    worker_id = int(request.json['workerId'])
    data_item = request.json['item']
    data_type = "WarehouseVital"
    times = [""]
    values = []

    for d in read_data(data_type):
        if d['frameworx:workerId'] == worker_id:
            date = dateutil.parser.parse(d['dc:date'])
            time = str(date.hour).zfill(2) + ":" + str((date.minute//10)*10).zfill(2)
            if time != times[-1]:
                times.append(time)
                values.append(d["frameworx:" + data_item])

    del times[0]

    data = {'label': data_item,
            'labels': times,
            'data': values}

    return jsonify(json.dumps(data))


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
        if not os.path.exists(data_type + ".json"):
            write_data(data_type)

    app.debug = True
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    if DEBUG:
        app.run(host="0.0.0.0", debug=True)
    else:
        app.run(debug=True)

