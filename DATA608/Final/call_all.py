# -*- coding: utf-8 -*-
"""
Created on Sat May 19 17:02:49 2018

@author: Exped
"""

from google.transit import gtfs_realtime_pb2
import time 
import random
import requests
import pandas as pd
import re
import time # imports module for Epoch/GMT time conversion
import os # imports package for dotenv
from dotenv import load_dotenv, find_dotenv # imports module for dotenv
load_dotenv(find_dotenv()) # loads .env from root directory
from protobuf_to_dict import protobuf_to_dict
# The root directory requires a .env file with API_KEY assigned/defined within
# and dotenv installed from pypi. Get API key from http://datamine.mta.info/user

def updates(dictionary):
    emptyTable = []
    for id_vehicle in dictionary:
        row = []
        for k,v in id_vehicle.items():
            count = 0
            if k == 'trip_update':
                for n,m in v.items():
                    if n == 'stop_time_update':
                        m = m[0]
                        if count== 0:
                            for z,x in m.items():
                                if len(str(x)) > 10:
                                    row.append(int(re.findall('\d+', str(x) )[0]))
                                else:
                                    row.append(x)
                            count += 1
                        else:
                            continue
                    if n == 'trip':
                        for g,h in m.items():
                            row.append(h)
        if len(row) > 1:
            emptyTable.append(row)
    frame = pd.DataFrame(emptyTable)
    frame.columns = ['id','Date','route_id','arrival','departure','stop_id','schedule_relationship']
    return(frame)

api_key = '8f06b8cf93a06466cc325406e73b7faf'



# Requests subway status data feed from City of New York MTA API
feed = gtfs_realtime_pb2.FeedMessage()
feeds = ['http://datamine.mta.info/mta_esi.php?key={}&feed_id=1',
         'http://datamine.mta.info/mta_esi.php?key={}&feed_id=26',
         'http://datamine.mta.info/mta_esi.php?key={}&feed_id=16',
         'http://datamine.mta.info/mta_esi.php?key={}&feed_id=21',
         'http://datamine.mta.info/mta_esi.php?key={}&feed_id=2',
         'http://datamine.mta.info/mta_esi.php?key={}&feed_id=11',
         'http://datamine.mta.info/mta_esi.php?key={}&feed_id=31',
         'http://datamine.mta.info/mta_esi.php?key={}&feed_id=36',
         'http://datamine.mta.info/mta_esi.php?key={}&feed_id=51',
         ]
responses = []
for feeder in feeds:
    response = requests.get(feeder.format(api_key))
    feed.ParseFromString(response.content)
    subway_feed = protobuf_to_dict(feed) # subway_feed is a dictionary
    time.sleep(random.randint(15,30))
    while True:
        try:
            responses.append(subway_feed['entity']) # train_data is a list
            print('Success')
        except:
            print('Trying again')
            time.sleep(random.randint(20,40))
            continue
        break
        



primeData = []

'''
for x in responses[1:]:
    primeData.append(updates(x))
    
liveData = pd.concat(primeData)'''


response = requests.get('http://datamine.mta.info/mta_esi.php?key={}&feed_id=1'.format(api_key))
feed.ParseFromString(response.content)
subway_feed = protobuf_to_dict(feed) # subway_feed is a dictionary
realtime_data = subway_feed['entity'] # train_data is a list










