from flask import Flask
from flask import render_template

#some random imports
import logging, json, importio, latch

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
	app.run(debug=True)