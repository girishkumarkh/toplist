# -*- coding: utf-8 -*-
import requests, json
from bs4 import BeautifulSoup

dataRows = []
for page in range(0,10):
	if (page == 0):
		r = requests.get("http://www.billboard.com/charts/hot-100")
	else:
		payload = {'page': page}
		r = requests.get("http://www.billboard.com/charts/hot-100", params=payload)
	html = r.text
	soup = BeautifulSoup(html)
	list_of_songs = soup.find_all('article')
	for song in range(0,10):
		rank = list_of_songs[song].span.string #Rank
		song_name = list_of_songs[song].h1.string.strip() # Song name
		if (list_of_songs[song].p.a):
			artist = list_of_songs[song].p.a.string # Artist name
		else:
			artist = list_of_songs[song].p.string # Artist name
		album = list_of_songs[song].p.br.string.strip() # Album name
		dic = {'rank': rank, 'song_name': song_name,'artist': artist,'album': album}
		dataRows.append(dic)

with open('data.json', 'w') as outfile:
	json.dump(dataRows, outfile)
print "data.JSON file is extracted"
