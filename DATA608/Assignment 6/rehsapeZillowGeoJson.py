# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 22:30:52 2018

@author: Exped
"""
import folium
import winsound
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 10  # Set Duration To 1000 ms == 1 second


import shapefile
shape = shapefile.Reader('NYBoundaries/ZillowNeighborhoods-NY.shp')
#first feature of the shapefile
feature = shape.shapeRecords()[0]
first = feature.shape.__geo_interface__ 




boroughList = ['Queens','Kings','New York','Bronx']
   # read the shapefile
reader = shapefile.Reader('NYBoundaries/ZillowNeighborhoods-NY.shp')
fields = reader.fields[1:]
field_names = [field[0] for field in fields]
buffer = []
for sr in reader.shapeRecords():
    atr = dict(zip(field_names, sr.record))
    print(atr['Name'])
    if atr['County'] in boroughList:
        geom = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature", \
                           geometry=geom, properties=atr)) 
   
   # write the GeoJSON file
from json import dumps
geojson = open("NYneighorhoods.json", "w")
geojson.write(dumps({"type": "FeatureCollection",\
                     "features": buffer}, indent=2) + "\n")
geojson.close()



m = folium.Map([40.78,-73.97], zoom_start=15)

m.choropleth(
    geo_data=open('NYneighorhoods.json').read(),
    #data=unemployment,
    #columns=['State', 'Unemployment'],
    #key_on='feature.id',
    #fill_color='YlGn',
    )