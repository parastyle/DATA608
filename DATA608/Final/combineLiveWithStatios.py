# -*- coding: utf-8 -*-
"""
Created on Sat May 19 22:31:08 2018

@author: Exped
"""
from shapely.geometry import shape, Point
import pandas as pd
import numpy as np
import json
from collections import Counter
import plotly

plotly.tools.set_credentials_file(username='', api_key='')
mapbox_access_token = ''

stations = pd.read_csv('https://raw.githubusercontent.com/parastyle/DATA608/master/DATA608/data/Stations.csv') 
stations['stop_id'] = stations['GTFS Stop ID']
liveData = pd.read_csv('https://raw.githubusercontent.com/parastyle/DATA608/master/DATA608/data/liveData.csv',index_col=0)
liveData['stop_id'] = liveData['stop_id'].astype(str).str[:-1]

##### Merge
allData = pd.merge(liveData,stations)


#####Do some neighborhood math

#load neighborhoods
with open('NYneighorhoods.json') as f:
    js = json.load(f)

allNames = pd.DataFrame(js['features'][k]['properties']['Name'] for k in range(len(js['features'])))
allNames.columns = ['Name']


neighborhood = []
indvF = []
for index, row in allData.iterrows():
    point = Point(row['GTFS Longitude'],row['GTFS Latitude'])
    for feature in js['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            neighborhood.append(feature['properties']['Name'])
neighborhood.sort()
df = pd.DataFrame.from_dict(Counter(neighborhood), orient='index').reset_index()
df.columns = ['Name','Frequency']
df.assign(D=np.nan)
df = df.merge(allNames, how='right')
df = df.fillna(value=0)

#Levels of density
l1,l2 = [],[]


for index, row in df.iterrows():
    if row['Frequency'] <= 3:
        for e, feature in enumerate(js['features']):
            if feature.get('properties').get('Name') == row['Name']:
                l1.append(js['features'][e])
    else:
        for e, feature in enumerate(js['features']):
            if feature.get('properties').get('Name') == row['Name']:
                l2.append(js['features'][e])

green_data = {"type": "FeatureCollection"}
green_data['features'] = l1

red_data = {"type": "FeatureCollection"}
red_data['features'] = l2


with open('red_data.json', 'w') as f:
    f.write(json.dumps(red_data))
with open('green_data.json', 'w') as f:
    f.write(json.dumps(green_data))

