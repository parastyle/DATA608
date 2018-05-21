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


plotly.tools.set_credentials_file(username='Parastyle', api_key='bVEKNTpHflu2IpcnetwH')
mapbox_access_token = 'pk.eyJ1IjoicGFyYXN0eWxlIiwiYSI6ImNqaDZ2MTlzcjAxYjEzM3BjNzUxNnVkZnAifQ.ekMqXJjfWyUj8PQJQ-hdlg'

stations = pd.read_csv('https://raw.githubusercontent.com/parastyle/DATA608/master/DATA608/data/Stations.csv') 
stations['stop_id'] = stations['GTFS Stop ID']
stations['hood'] = 0
stations2 = stations


#####Do some neighborhood math

#load neighborhoods
with open('NYneighorhoods.json') as f:
    js = json.load(f)

allNames = pd.DataFrame(js['features'][k]['properties']['Name'] for k in range(len(js['features'])))
allNames.columns = ['Name']

for index, row in stations2.iterrows():
    point = Point(row['GTFS Longitude'],row['GTFS Latitude'])
    for feature in js['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            stations['hood'][index] =feature['properties']['Name']

stations['Frequency'] = stations.groupby('hood')['hood'].transform('count')

df = stations
#Levels of density
l1,l2,l3,l4 = [],[],[], []


for index, row in df.iterrows():
    if row['Frequency'] <= 5:
        for e, feature in enumerate(js['features']):
            if feature.get('properties').get('Name') == row['hood']:
                l1.append(js['features'][e])
    elif row['Frequency'] <= 9:
        for e, feature in enumerate(js['features']):
            if feature.get('properties').get('Name') == row['hood']:
                l2.append(js['features'][e])
    else:
        for e, feature in enumerate(js['features']):
            if feature.get('properties').get('Name') == row['hood']:
                l3.append(js['features'][e])
                
for index, row in allNames.iterrows():
    if row['Name'] not in df['hood'].unique():
        for e, feature in enumerate(js['features']):
            if feature.get('properties').get('Name') == row['Name']:
                l4.append(js['features'][e])
                

low_data = {"type": "FeatureCollection"}
low_data['features'] = l1

med_data = {"type": "FeatureCollection"}
med_data['features'] = l2

high_data = {"type": "FeatureCollection"}
high_data['features'] = l3

void_data = {"type": "FeatureCollection"}
void_data['features'] = l4

with open('low_data.json', 'w') as f:
    f.write(json.dumps(low_data))
with open('med_data.json', 'w') as f:
    f.write(json.dumps(med_data))
with open('high_data.json', 'w') as f:
    f.write(json.dumps(high_data))
with open('void_data.json', 'w') as f:
    f.write(json.dumps(void_data))


