from flask import Flask
from flask import render_template
import subprocess
#some random imports
import json
app = Flask(__name__)
global dataRows

@app.route("/")
def home():
	with open("data.txt") as json_file:
		json_data = json.load(json_file)
	return render_template('home.html', data=json_data)  

@app.route("/songlist")
def songlist():
	with open("data.txt") as json_file:
		json_data = json.load(json_file)
	return render_template('songlist.html', data=json_data) 


if __name__ == "__main__":
	subprocess.call(["python worker.py"], shell=True)
	app.run(debug=True)
