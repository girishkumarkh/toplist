from flask import Flask
from flask import render_template
from threading import Thread

#some random imports
import logging, json, importio, latch
import sched, time

app = Flask(__name__)
global dataRows

s = sched.scheduler(time.time, time.sleep)

def getchart():
	# To use an API key for authentication, use the following code:
	client = importio.importio(user_id="877a94b9-5a3d-4868-bcf7-85bd0e150f96", api_key="4Sj5laBSBEiPLJCJl3aFxnezKVy3/8UOJoOMJuhx+gU2iYe5GhYRgWTDXtL/WN3dyB80xynC0WmDvJO5v5KKeQ==", host="https://query.import.io")

	# Once we have started the client and authenticated, we need to connect it to the server:
	client.connect()

	# Because import.io queries are asynchronous, for this simple script we will use a "latch"
	# to stop the script from exiting before all of our queries are returned
	# For more information on the latch class, see the latch.py file included in this client library
	queryLatch = latch.latch(10)

	# Define here a global variable that we can put all our results in to when they come back from
	# the server, so we can use the data later on in the script
	dataRows = []

	# In order to receive the data from the queries we issue, we need to define a callback method
	# This method will receive each message that comes back from the queries, and we can take that
	# data and store it for use in our app
	def callback(query, message):
	  

	  # Disconnect messages happen if we disconnect the client library while a query is in progress
	  if message["type"] == "DISCONNECT":
		print "Query in progress when library disconnected"
		#print json.dumps(message["data"], indent = 4)

	  # Check the message we receive actually has some data in it
	  if message["type"] == "MESSAGE":
		if "errorType" in message["data"]:
		  # In this case, we received a message, but it was an error from the external service
		  print "Got an error!" 
		  print json.dumps(message["data"], indent = 4)
		else:
		  # We got a message and it was not an error, so we can process the data
		  print "Got data!"
		  #print json.dumps(message["data"], indent = 4)
		  # Save the data we got in our dataRows variable for later
		  dataRows.extend(message["data"]["results"])

	  # When the query is finished, countdown the latch so the program can continue when everything is done
	  if query.finished(): queryLatch.countdown()

	# Issue queries to your data sources and with your inputs
	# You can modify the inputs and connectorGuids so as to query your own sources
	# Query for tile Billboard top 100 charts
	client.query({
	  "connectorGuids": [
		"58099e34-6688-4c3e-bc44-779a09010e8f"
	  ],
	  "input": {
		"webpage/url": "http://www.billboard.com/charts/hot-100"
	  }
	}, callback)

	# Query for tile Billboard top 100 charts
	client.query({
	  "connectorGuids": [
		"58099e34-6688-4c3e-bc44-779a09010e8f"
	  ],
	  "input": {
		"webpage/url": "http://www.billboard.com/charts/hot-100?page=1"
	  }
	}, callback)

	# Query for tile Billboard top 100 charts
	client.query({
	  "connectorGuids": [
		"58099e34-6688-4c3e-bc44-779a09010e8f"
	  ],
	  "input": {
		"webpage/url": "http://www.billboard.com/charts/hot-100?page=2"
	  }
	}, callback)

	# Query for tile Billboard top 100 charts
	client.query({
	  "connectorGuids": [
		"58099e34-6688-4c3e-bc44-779a09010e8f"
	  ],
	  "input": {
		"webpage/url": "http://www.billboard.com/charts/hot-100?page=3"
	  }
	}, callback)

	# Query for tile Billboard top 100 charts
	client.query({
	  "connectorGuids": [
		"58099e34-6688-4c3e-bc44-779a09010e8f"
	  ],
	  "input": {
		"webpage/url": "http://www.billboard.com/charts/hot-100?page=4"
	  }
	}, callback)

	# Query for tile Billboard top 100 charts
	client.query({
	  "connectorGuids": [
		"58099e34-6688-4c3e-bc44-779a09010e8f"
	  ],
	  "input": {
		"webpage/url": "http://www.billboard.com/charts/hot-100?page=5"
	  }
	}, callback)

	# Query for tile Billboard top 100 charts
	client.query({
	  "connectorGuids": [
		"58099e34-6688-4c3e-bc44-779a09010e8f"
	  ],
	  "input": {
		"webpage/url": "http://www.billboard.com/charts/hot-100?page=6"
	  }
	}, callback)

	# Query for tile Billboard top 100 charts
	client.query({
	  "connectorGuids": [
		"58099e34-6688-4c3e-bc44-779a09010e8f"
	  ],
	  "input": {
		"webpage/url": "http://www.billboard.com/charts/hot-100?page=7"
	  }
	}, callback)

	# Query for tile Billboard top 100 charts
	client.query({
	  "connectorGuids": [
		"58099e34-6688-4c3e-bc44-779a09010e8f"
	  ],
	  "input": {
		"webpage/url": "http://www.billboard.com/charts/hot-100?page=8"
	  }
	}, callback)

	# Query for tile Billboard top 100 charts
	client.query({
	  "connectorGuids": [
		"58099e34-6688-4c3e-bc44-779a09010e8f"
	  ],
	  "input": {
		"webpage/url": "http://www.billboard.com/charts/hot-100?page=9"
	  }
	}, callback)

	print "Queries dispatched, now waiting for results"

	# Now we have issued all of the queries, we can "await" on the latch so that we know when it is all done
	queryLatch.await()

	print "Latch has completed, all results returned"

	# It is best practice to disconnect when you are finished sending queries and getting data - it allows us to
	# clean up resources on the client and the server
	client.disconnect()

	# Now we can print out the data we got
	print "All data received and saved into json file"
	#print json.dumps(dataRows, indent = 4)
	with open('data.txt', 'w') as outfile:
  		json.dump(dataRows, outfile)
  	s.enter(5, 1, getchart, ())
  	s.run()


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
	#thr = Thread(target=getchart)
	#thr.start()
	getchart()
	app.run(debug=True)
    #s.run()