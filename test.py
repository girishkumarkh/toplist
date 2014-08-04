# Test
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

r = requests.get("http://www.billboard.com/charts/hot-100")
p = r.text
page1 = BeautifulSoup(p)
tag.name = "a id='rank_1'"
print tag