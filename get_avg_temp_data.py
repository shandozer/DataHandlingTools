#!/usr/local/bin/python
"""
__author__ = 'Shannon Buckley', 8/17/14
"""

import os
from os import path
from BeautifulSoup import BeautifulSoup
import urllib2

root = '/Users/st_buckls/PycharmProjects/DataHandlingTools/'
file_out = path.join(root, 'weather-data.txt')

YEAR = 2009
AIRPORT = 'KBUF'

f = open(file_out, 'w')

for m in range(1,13):
    for d in range(1,32):
        if (m == 2 and d > 28):
            break
        elif (m in [4,6,9,11] and d  > 30):
            break

        timestamp = str(YEAR) + str(m) + str(d)
        # do some formatting to timestamp

        if len(str(m)) < 2:
            mStamp = '0' +str(m)
        else:
            mStamp = str(m)

        if len(str(d)) < 2:
            dStamp = '0' + str(d)
        else:
            dStamp = str(d)

        timestamp = str(YEAR) + mStamp + dStamp

        print "Getting data for " + timestamp

        url = "http://www.wunderground.com/history/airport/%(airport_code)s/%(year)s/%(month)s/%(day)s/DailyHistory" \
              ".html" % {'airport_code' : AIRPORT,
                         'year'         : str(YEAR),
                         'month'        : str(m),
                         'day'          : str(d)}

        page = urllib2.urlopen(url)

        soup = BeautifulSoup(page)

        print 'getting Temperature data'
        dayTemp = soup.findAll(attrs={"class": "wx-data"})[2].span.string



        f.write(timestamp + ',' + dayTemp +'\n')

    print 'closing file...'
    f.close()