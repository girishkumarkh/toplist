# -*- coding: utf-8 -*-
import os
import requests
import sched
import time
import json
from bs4 import BeautifulSoup

# Google API Key #
DEVELOPER_KEY = os.environ['G_DEV_KEY']


def youtube_search(options):
    payload = {'part': 'snippet', 'q': options["q"], 'maxResults': options["maxResults"], 'key': DEVELOPER_KEY}
    r = requests.get("https://www.googleapis.com/youtube/v3/search", params=payload)
    for search_result in r.json().get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            return search_result


def getchart():
    dataRows = []
    r = requests.get("http://www.billboard.com/charts/hot-100")
    html = r.text
    soup = BeautifulSoup(html, "html.parser")

    # ==== Get 100 Songs =====
    list_of_songs = soup.find_all('li', {"class": "chart-list__element"})
    print(list_of_songs)
    print("{} items scraped".format(len(list_of_songs)))
    for each_song in list_of_songs:
        rank = each_song.select("span.chart-element__rank__number")[0].string.strip()  # Rank
        song_name = each_song.select("span.chart-element__information__song")[0].string.strip()  # Song name
        artist = each_song.select("span.chart-element__information__artist")[0].string.strip()  # Artist name

        dic = {
            'rank': rank,
            'song_name': song_name,
            'artist': artist
            # 'album' : album
        }
        print(dic)
        dataRows.append(dic)

    with open('data.json', 'w') as outfile:
        json.dump(dataRows, outfile)
    print("\033[95m Data JSON is extracted \033[0m")

    playlistid = []
    for item in dataRows:
        query = youtube_search({"q": "%s %s" % (item["song_name"], item["artist"]), "maxResults": "1"})
        print(query)
        if query:
            playlistid.append(query)
    print("\033[94m Video JSON is extracted \033[0m")

    with open('playlist.json', 'w') as outfile:
        json.dump(playlistid, outfile)

    del dataRows[0:len(dataRows)]
    s.enter(21600, 1, getchart, ())  # 86400 #43200 21600
    s.run()


if __name__ == "__main__":
    s = sched.scheduler(time.time, time.sleep)
    getchart()
