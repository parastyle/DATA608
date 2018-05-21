# -*- coding: utf-8 -*-
"""
Created on Mon May 14 18:11:51 2018

@author: Exped
"""
from shapely.geometry import shape, Point
import pandas as pd
import numpy as np
import json
from collections import Counter
import plotly
from plotly.offline import plot
import plotly.plotly as py
import plotly.graph_objs as graph_objs

plotly.tools.set_credentials_file(username='', api_key='')
mapbox_access_token = ''

stations = pd.read_csv('https://raw.githubusercontent.com/parastyle/DATA608/master/DATA608/data/Stations.csv') 
stations['stop_id'] = stations['GTFS Stop ID']
liveData = pd.read_csv('https://raw.githubusercontent.com/parastyle/DATA608/master/DATA608/data/liveData.csv',index_col=0)
liveData['stop_id'] = liveData['stop_id'].astype(str).str[:-1]

##### Merge
allData = pd.merge(liveData,stations)


    

    
data = graph_objs.Data([
    graph_objs.Scattermapbox(
        lat=allData['GTFS Latitude'],
        lon=allData['GTFS Longitude'],
        text=allData['route_id'],
        hovertext=['route_id'],
        mode='markers',
        marker= dict(symbol='square',
                     opacity=1,
                     size=9)
    )
])
layout = graph_objs.Layout(
    height=700,
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        layers=[
            dict(
                sourcetype = 'geojson',
                source = 'https://raw.githubusercontent.com/parastyle/DATA608/master/DATA608/data/green_data.json',
                #source = 'https://raw.githubusercontent.com/plotly/datasets/master/florida-blue-data.json',
                type = 'fill',
                color = 'rgba(82, 182, 114,0.4)'
            ),
            dict(
                sourcetype = 'geojson',
                source = 'https://raw.githubusercontent.com/parastyle/DATA608/master/DATA608/data/red_data.json',
                #source = 'https://raw.githubusercontent.com/plotly/datasets/master/florida-blue-data.json',
                type = 'fill',
                color = 'rgba(190, 107, 23,0.4)'
            ),
            dict(
                sourcetype = 'geojson',
                source = 'https://raw.githubusercontent.com/parastyle/DATA608/master/DATA608/data/nyc_subway_line.geojson',
                #source = 'https://raw.githubusercontent.com/plotly/datasets/master/florida-red-data.json',
                type = 'line',
                color = 'rgba(62, 243, 21,1)'
            )
        ],
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=40,
            lon=-73
        ),
        pitch=0,
        zoom=9.2,
        style='light'
    ),
    
)
        
fig = dict(data=data, layout=layout)
py.iplot(fig, filename='county-level-choropleths-python')
        
'''
fig = dict(data=data, layout=layout)
plotly.offline.plot(fig, filename='county-level-choropleths-pythonTEHE')'''
