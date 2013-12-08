# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import re,os

# <codecell>

from bs4 import BeautifulSoup as bs
import urllib2

# <codecell>

searchurl = raw_input("Enter a website to extract the URL's from: ")
#searchurl = "http://www.yelp.com/berkeley"
f = urllib2.urlopen(searchurl)
html = f.read()
soup = bs(html)

desc = soup.findAll(attrs={"name":"description"}) 
#print desc[0]
mySoup = desc[0]['content']
print mySoup

# <codecell>

#for fish in soup.findAll('p'):
    #print fish.contents[0]

# <codecell>

str1 = "Hello world"
str2 = "world"
str3 = "hi"
str1.match(str1)

# <codecell>


