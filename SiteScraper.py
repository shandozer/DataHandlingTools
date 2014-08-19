#!/usr/local/bin/python
"""
__author__ = 'Shannon Buckley', 8/17/14
"""

import os
from os import path
import urllib2
from BeautifulSoup import BeautifulSoup

page = urllib2.urlopen("http://www.wunderground.com/history/airport/KBUF/2009/1/1/DailyHistory.html")

soup = BeautifulSoup(page)

images = soup.findAll('img')

first_img = images[0]

src = first_img['src']

try:
    wx_data = soup.findAll(attrs={"class":"wx-data"})
    print 'found wx data, giving 2nd element / Avg Daily Temp: %s' % wx_data[1]
except Exception:
    print 'Could not find any wx-data pieces... Make sure date is more recent?'

# the Mean Temp is the 2nd element of the wx-data... nobr must be deprecated
dayTemp = wx_data[1].span.string

print 'The Average Daily Temp for KBUF airport on 1/1/2009 was: %s' % dayTemp

