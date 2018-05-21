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
import plotly.graph_objs as go

plotly.tools.set_credentials_file(username='Parastyle', api_key='bVEKNTpHflu2IpcnetwH')
mapbox_access_token = 'pk.eyJ1IjoicGFyYXN0eWxlIiwiYSI6ImNqaDZ2MTlzcjAxYjEzM3BjNzUxNnVkZnAifQ.ekMqXJjfWyUj8PQJQ-hdlg'

stations = pd.read_csv('https://raw.githubusercontent.com/parastyle/DATA608/master/DATA608/data/Stations.csv') 
stations['stop_id'] = stations['GTFS Stop ID']
liveData = pd.read_csv('https://raw.githubusercontent.com/parastyle/DATA608/master/DATA608/data/liveData.csv',index_col=0)
liveData['stop_id'] = liveData['stop_id'].astype(str).str[:-1]

##### Merge
allData = pd.merge(liveData,stations)
allData['Frequency'] = allData.groupby('Station ID')['Station ID'].transform('count')

DFtable = pd.DataFrame({'Station':allData['Stop Name'],'Frequency':allData['Frequency']}).drop_duplicates()
DFtable = DFtable.sort_values(by='Frequency',ascending=False)
    

    
trace = go.Table(
    header=dict(values=['Neighborhood', 'Current # of trains'],
                line = dict(color='#7D7F80'),
                fill = dict(color='#a1c3d1'),
                align = ['left'] * 5),
    cells=dict(values=[list(DFtable['Station']),
                       list(DFtable['Frequency'])],
               line = dict(color='#7D7F80'),
               fill = dict(color='#EDFAFF'),
               align = ['left'] * 5))

layout = dict(width=500, height=400)
data = [trace]
        
fig = dict(data=data, layout=layout)
py.iplot(fig, filename='live_table')
        
'''
fig = dict(data=data, layout=layout)
plotly.offline.plot(fig, filename='county-level-choropleths-pythonTEHE')'''