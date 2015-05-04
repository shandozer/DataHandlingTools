#!/usr/local/bin/python
"""
__author__ = 'Shannon Buckley', 8/17/14
"""

import os
from os import path
from BeautifulSoup import BeautifulSoup
import urllib2
from datetime import date

project_root = path.join(os.getcwd(), 'WeatherScrapeData')
os.makedirs(project_root)

file_out = path.join(project_root, 'weather-data.txt')

YEAR = 2009
AIRPORTCODE = 'KBUF'

AIRPORT_DESCRIPTIONS = {'KBUF': 'Buffalo, NY'}

f = open(file_out, 'w')

print 'getting Temperature data from %s... ' % AIRPORT_DESCRIPTIONS.get(AIRPORTCODE)

for m in range(1,13):
    for d in range(1,32):
        if m == 2 and d > 28:
            break
        elif m in [4,6,9,11] and d  > 30:
            break

        todaysdate = date(YEAR, m, d).isoformat()

        timestamp = str(YEAR) + str(m) + str(d)

        url = "http://www.wunderground.com/history/airport/%(airport_code)s/%(year)s/%(month)s/%(day)s/DailyHistory" \
              ".html" % {'airport_code' : AIRPORTCODE,
                         'year'         : str(YEAR),
                         'month'        : str(m),
                         'day'          : str(d)}

        page = urllib2.urlopen(url)

        soup = BeautifulSoup(page)

        dayTemp = soup.findAll(attrs={"class": "wx-data"})[2].span.string

        f.write(todaysdate + ',' + dayTemp + '\n')

        print '\tDate: %s \t Temp: %s' % (todaysdate, dayTemp)

    print 'closing file...'
    f.close()