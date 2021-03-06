# -*- coding: utf-8 -*-

from flask import Flask, session, redirect, render_template, jsonify, request, Response, url_for, send_file
from functools import wraps
import json
import sys
import logging
import os
from mylib import graph, personal
import requests
import shutil

DEBUG = False
#DEBUG = True

app = Flask(__name__)
app.config['SECRET_KEY'] = 'XXXXXX'


@app.before_request
def before_request():
    if session.get('username') is not None:
        return
    if request.path == '/login':
        return
    if request.path[-4:] == ".css":
        return
    if request.path[-3:] == ".js":
        return
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and is_valid_user():
        session['username'] = request.form['workerId']
        return redirect(url_for('index'))
    return render_template('login.html')


def is_valid_user():
    if request.form.get('workerId') is None:
        return False
    return True


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


def get_request(payload):
    payload['acl:consumerKey'] = os.environ["FRAMEWORX_KEY"]
    return requests.get("https://api.frameworxopendata.jp/api/v3/datapoints", params=payload)


def write_data(data_type):
    payload = {'rdf:type': "frameworx:" + data_type}
    data = get_request(payload)
    with open(data_type + ".json", 'w') as f:
        json.dump(data.json(), f)


def write_map(filename, dirname=""):
    payload = {'acl:consumerKey': os.environ["FRAMEWORX_KEY"]}
    r = requests.get("https://api.frameworxopendata.jp/api/v3/files/" + filename, params=payload, stream=True)
    if r.status_code == 200:
        with open(os.path.join(dirname, filename), 'wb') as f:
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
        if DEBUG:
            auth = request.authorization
            if not auth or not check_auth(auth.username, auth.password):
                return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/_get_personal_log_data', methods=["POST"])
@requires_auth
def _get_personal_log_data():
    workerId = request.json[u'workerId']
    category = request.json[u'category']
    data = personal.get_log_data(workerId, category)
    return jsonify(data=json.dumps(data))


@app.route('/_get_personal_summary_data', methods=["POST"])
@requires_auth
def _get_personal_summary_data():
    workerId = int(request.json[u'workerId'])
    data = personal.get_summary_data(workerId)
    return jsonify(data=json.dumps(data))


@app.route('/_get_personal_map_data', methods=["POST"])
@requires_auth
def _get_personal_map_data():
    workerId = int(request.json[u'workerId'])
    data = personal.get_map_data(workerId)
    return jsonify(data=json.dumps(data))

@app.route('/image')
def image():
    dirname = "static/images/"
    filename = "warehouse_map_1.jpg"
    path = os.path.join(dirname, filename)
    if not os.path.exists(path):
        write_map(filename, dirname)
    return send_file(path, mimetype='image/jpg')

@app.route('/_step_graph', methods=["GET", "POST"])
@requires_auth
def _step_graph():
    return jsonify({"test": "aaa"})


@app.route('/_item_ranking', methods=["GET"])
@requires_auth
def _item_ranking():
    return jsonify(graph.getTotalItemNumData(os.environ["FRAMEWORX_KEY"]))


@app.route('/_cal_ranking', methods=["GET"])
@requires_auth
def _cal_ranking():
    return jsonify(graph.getVitalData(os.environ["FRAMEWORX_KEY"], "calorie"))


@app.route('/_distance_ranking', methods=["GET"])
@requires_auth
def _distance_ranking():
    return jsonify(graph.getMoveDistance(os.environ["FRAMEWORX_KEY"]))


@app.route('/_step_ranking', methods=["GET"])
@requires_auth
def _step_ranking():
    return jsonify(graph.getVitalData(os.environ["FRAMEWORX_KEY"], "step"))


@app.route('/_get_session', methods=["GET"])
@requires_auth
def _get_session():
    key = request.args['key']
    return session.get(key)


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


@app.route("/man.html")
@requires_auth
def man_page():
    return render_template("man.html")


if __name__ == "__main__":
    app.debug = True
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    if DEBUG:
        app.run(host="0.0.0.0", debug=True, threaded=True)
    else:
        app.run(threaded=True)
