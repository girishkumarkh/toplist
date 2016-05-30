import os
from flask import Flask
from flask import render_template, jsonify
# import subprocess
# some random imports
import json
from datetime import timedelta
from flask import make_response, request, current_app, abort, request
from functools import update_wrapper

app = Flask(__name__)


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


ALLOW_HOSTS = ['*.paperlist.co', 'www.paperlist.co']


@app.before_request
def limit_remote_addr():
    print str(request.remote_addr)
    print ALLOW_HOSTS
    print str(request.remote_addr) not in ALLOW_HOSTS
    if str(request.remote_addr) not in ALLOW_HOSTS:
        abort(403)  # Forbidden


@app.route("/")
def home():
    with open("playlist.json") as json_file:
        json_data = json.load(json_file)
    first = json_data.pop(0)["id"]["videoId"]
    othervideo = [item["id"]["videoId"] for item in json_data]
    rest = (',').join(othervideo)
    return render_template('home.html', first=first, data=rest)


@app.route("/songlist")
def songlist():
    with open("data.json") as json_file:
        json_data = json.load(json_file)
    return render_template('songlist.html', data=json_data)


@app.route("/api/toplist")
@crossdomain(origin='*')
def api():
    with open("playlist.json") as json_file:
        json_data = json.load(json_file)
    return jsonify(data=json_data)


if __name__ == "__main__":
    host = os.environ.get('HOST', 'localhost')
    port = int(os.environ.get('PORT', 8000))
    app.run(host=host, port=port, debug=True)
