# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 20:28:08 2018

@author: Exped
"""

import requests
import pandas
import tempfile
import datetime
import gtfstk
import folium
import haversine
from functools import reduce
from multiprocessing import Pool

def url2gtfs(url):
    r = requests.get(url)
    with tempfile.NamedTemporaryFile(delete=False) as f:
      f.write(r._content)
      return gtfstk.read_gtfs(f.name, dist_units='mi')


def parseTime(time): # to deal with times after midnight
    if int(time.split(':')[0]) > 23:
        return datetime.datetime.strptime('2:' + str(int(time.split(':')[0]) - 24) + ':'
                                          + time.split(':')[1] + ':' + time.split(':')[2], '%d:%H:%M:%S')
    else:
        return datetime.datetime.strptime('1:' + time, '%d:%H:%M:%S')


def tripToSegments(trip_id):
    stop_times = gtfs.stop_times[gtfs.stop_times['trip_id'] == trip_id]
    segments = []
    for i in range(len(stop_times)-1):
        origin = gtfs.stops[gtfs.stops['stop_id'] == stop_times['stop_id'].iloc[i]]
        destination = gtfs.stops[gtfs.stops['stop_id'] == stop_times['stop_id'].iloc[i+1]]
        distance = haversine.haversine((origin['stop_lat'], origin['stop_lon']),
                         (destination['stop_lat'], destination['stop_lon']),
                         miles=True)
        startTime = parseTime(stop_times['departure_time'].iloc[i])
        stopTime = parseTime(stop_times['arrival_time'].iloc[i+1])
        duration = (stopTime - startTime).seconds
        if duration == 0:
            speed = 0 # when the laws of physics do not apply
        else:
            speed = distance / duration * 60 * 60
        segments.append({'origin_id': origin['stop_id'].iloc[0],
                         'destination_id': destination['stop_id'].iloc[0],
                         'distance': distance,
                         'duration': duration,
                         'speed': speed})
    return(segments)

def plotSegment(segment):
    origin = gtfs.stops[gtfs.stops['stop_id'] == segment.name[0]]
    destination = gtfs.stops[gtfs.stops['stop_id'] == segment.name[1]]
    folium.PolyLine(locations=[(origin.stop_lat.iloc[0], origin.stop_lon.iloc[0]),
                               (destination.stop_lat.iloc[0], destination.stop_lon.iloc[0])],
                    popup=str(segment.speed['min']),
                    weight=segment.speed['min']
                   ).add_to(foliumMap)
    
    
##########################################################################

url = 'https://gitlab.com/LACMTA/gtfs_rail/raw/master/gtfs_rail.zip' # Los Angeles County Metro
# url = 'http://github.com/transitland/gtfs-archives-not-hosted-elsewhere/raw/master/amtrak.zip' # Amtrak
gtfs = url2gtfs('http://web.mta.info/developers/data/nyct/subway/google_transit.zip')
'''
route_id = '1'
direction_id = 1.0

trip_ids = gtfs.trips[(gtfs.trips['route_id'] == route_id) & (gtfs.trips['direction_id'] == direction_id)]['trip_id']
p = Pool(8)
segments = reduce(lambda x, y: x + y, p.map(tripToSegments, trip_ids))
segmentsDF = pandas.DataFrame(segments).groupby(['origin_id', 'destination_id']).describe()'''

#40.7421571,-73.997239
