import requests, sched, time
from bs4 import BeautifulSoup

# Google API Key #
DEVELOPER_KEY = "AIzaSyB-kggO5cg8psVRpAJ2Yv73AJDlTwyCoSo"

def youtube_search(options):
  payload = {'part':'snippet', 'q':options["q"], 'maxResults':options["maxResults"], 'key':DEVELOPER_KEY}
  r = requests.get("https://www.googleapis.com/youtube/v3/search", params=payload)
  
  videos = []
  channels = []
  playlists = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in r.json().get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
    	return search_result
    	"""
    	## Returing only certain results ##
    	return {"title":search_result["snippet"]["title"], 
    			"videoID":search_result["id"]["videoId"], 
    			"albumArt":search_result["snippet"]["thumbnails"]["medium"]["url"], 
    			"channel":search_result["snippet"]["channelTitle"]
    			}
		"""

global dataRows
def getchart():
	page1 = BeautifulSoup('http://www.billboard.com/charts/hot-100')
	page2 = BeautifulSoup('http://www.billboard.com/charts/hot-100?page=1')
	page3 = BeautifulSoup('http://www.billboard.com/charts/hot-100?page=2')
	page4 = BeautifulSoup('http://www.billboard.com/charts/hot-100?page=3')
	page5 = BeautifulSoup('http://www.billboard.com/charts/hot-100?page=4')
	page6 = BeautifulSoup('http://www.billboard.com/charts/hot-100?page=5')
	page7 = BeautifulSoup('http://www.billboard.com/charts/hot-100?page=6')
	page8 = BeautifulSoup('http://www.billboard.com/charts/hot-100?page=7')
	page9 = BeautifulSoup('http://www.billboard.com/charts/hot-100?page=8')
	page10 = BeautifulSoup('http://www.billboard.com/charts/hot-100?page=9')
	
	print page1.article

	dataRows

	"""
			"rank" : 1,
			"album": "Trigga [Clean]", 
            "song_name": "Foreign", 
            "artist": "Trey Songz"
	"""
	with open('data.json', 'w') as outfile:
  		json.dump(dataRows, outfile)
  	print "data.JSON file is extracted"
  	
	playlistid=[]
	for item in dataRows:	
		query = youtube_search({"q":"%s %s" %(item["song_name"],item["artist"]),"maxResults":"1"})
		if query:
			playlistid.append(query)
			# print "VideoID id added"
	print "video id is done"

	with open('playlist.json', 'w') as outfile:
  		json.dump(playlistid, outfile)

  	del dataRows[0:len(dataRows)]
  	s.enter(21600, 1, getchart, ()) #86400 #43200 21600
  	s.run()

if __name__ == "__main__":
	s = sched.scheduler(time.time, time.sleep)
	getchart()