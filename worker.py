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

    # ==== Get First Song =====
    first_song = soup.find('div', class_='chart-number-one__info')
    if first_song.select("div.chart-number-one__artist")[0].select('a'):
        first_song_artist = first_song.select("div.chart-number-one__artist")[0].select('a')[0].string.strip()
    else:
        first_song_artist = first_song.select("div.chart-number-one__artist")[0].string.strip()
    first_dic = {
        'rank': 1,
        'song_name': first_song.select("div.chart-number-one__title")[0].string.strip(),
        'artist': first_song_artist
    }
    dataRows.append(first_dic)

    # ==== Get Next 99 Songs =====
    list_of_songs = soup.find_all('div', class_='chart-list-item')
    print("{} items scraped".format(len(list_of_songs) + 1))
    for each_song in list_of_songs:
        rank = each_song.select("div.chart-list-item__rank")[0].string.strip()  # Rank
        song_name = each_song.select("span.chart-list-item__title-text")[0].string.strip()  # Song name
        if each_song.select("div.chart-list-item__artist")[0].select('a'):
            artist = each_song.select("div.chart-list-item__artist")[0].select('a')[0].string.strip()  # Artist name
        else:
            artist = each_song.select("div.chart-list-item__artist")[0].string.strip()
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
            # print "VideoID id added"
    print("\033[94m Video JSON is extracted \033[0m")

    with open('playlist.json', 'w') as outfile:
        json.dump(playlistid, outfile)

    del dataRows[0:len(dataRows)]
    s.enter(21600, 1, getchart, ())  # 86400 #43200 21600
    s.run()

if __name__ == "__main__":
    s = sched.scheduler(time.time, time.sleep)
    getchart()
