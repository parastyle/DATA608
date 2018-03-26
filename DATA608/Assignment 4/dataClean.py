# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 14:52:23 2018

@author: Exped
"""
import geocoder as gc
import numpy as np
import pandas as pd
import time
import random

raw_data = pd.read_csv('https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/master/module4/Data/riverkeeper_data_2013.csv')
raw_data['Date'] = pd.to_datetime(raw_data['Date'])
raw_data['EnteroCount'] = raw_data['EnteroCount'].map(lambda x: x.lstrip('><'))\
                                     .astype(int)

def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))

locations_key = raw_data['Site'].unique()
locations_value = {}

the_month = 5
the_year = 2007

the_data = raw_data[(raw_data['Date'].dt.month==the_month) & (raw_data['Date'].dt.year==the_year)]
group_it = the_data.groupby(['Site'])[['EnteroCount']].mean()
group_it = group_it.sort_values(by=['EnteroCount'],ascending=False)

'''while len(locations_key) > 0:
    for pos,x in enumerate(locations_key):
        g = gc.google(x+', NY')
        if g.latlng == None:
            print('Query LIMIT : Waiting 10 seconds')
            time.sleep(10)
            g = gc.google(x+', NY')
        if g.latlng != None:
            locations_value[x] = g.latlng
            locations_key = np.delete(locations_key,pos)
            print('LatLong for ' + x + ' is ' +str(g.latlng))
            time.sleep(random.randint(10,15))
        print(len(locations_key))'''