import os
from flask import Flask
from flask import render_template, jsonify
# import subprocess
#some random imports
import json

app = Flask(__name__)

@app.route("/")
def home():
	with open("playlist.json") as json_file:
		json_data = json.load(json_file)
	first = json_data.pop(0)
	rest = (',').join(json_data)
	return render_template('home.html', first=first, data=rest)  

@app.route("/songlist")
def songlist():
	with open("data.json") as json_file:
		json_data = json.load(json_file)
	return render_template('songlist.html', data=json_data)

@app.route("/api/toplist")
def api():
	with open("playlist.json") as json_file:
		json_data = json.load(json_file)
	return jsonify(data=json_data)


if __name__ == "__main__":
	# subprocess.call(["python worker.py"], shell=True)
	port = int(os.environ.get("PORT",5000))
	app.run(host='0.0.0.0', port=port, debug=True)