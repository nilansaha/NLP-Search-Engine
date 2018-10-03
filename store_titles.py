# -*- coding: utf-8 -*-
from google_result import search
from bs4 import BeautifulSoup
import urllib2
import pandas as pd

webpages = search("How to learn python", 4)

titles = []

for result in webpages:
    try:
        titles.append(result[0].encode('ascii','ignore').replace("  "," "))
    except:
        print "Error"

df = pd.DataFrame()
df['Titles'] = titles
df.to_csv('titles.csv', index=False)
