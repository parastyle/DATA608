# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime as dt
import pandas as pd

raw_data = pd.read_csv('https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/master/module4/Data/riverkeeper_data_2013.csv')
raw_data['Date'] = pd.to_datetime(raw_data['Date'])
raw_data['EnteroCount'] = raw_data['EnteroCount'].map(lambda x: x.lstrip('><'))\
                                     .astype(int)

def grouper(input_data,raw_data):
    the_month = int(input_data[5:7])
    the_year = int(input_data[0:4])
    the_data = raw_data[(raw_data['Date'].dt.month==the_month) & (raw_data['Date'].dt.year==the_year)]
    group_it = the_data.groupby(['Site'])[['EnteroCount']].mean().round(1)
    group_it = group_it.sort_values(by=['EnteroCount'],ascending=True)
    return group_it
                  
app = dash.Dash()

app.layout = html.Div([
        
    dcc.DatePickerSingle(
    id='input',
    date=dt(2007, 5, 10)
    ),
    html.Div(id='output-decision'),
    html.Div(id='output-graph')
])

@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='date')]
)
def update_value_a(input_data):
    group_it = grouper(input_data,raw_data)
    
    wc =  dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': group_it.index, 'y': group_it.EnteroCount, 'type': 'line', 'name': 'Places to Launch'},
            ],
            'layout': {
                'title': 'Monthly water contamination levels'
            }
        }
    )
    return wc

@app.callback(
    Output(component_id='output-decision', component_property='children'),
    [Input(component_id='input', component_property='date')]
)
def update_value_b(input_data):
    group_it = grouper(input_data,raw_data)
    return 'Launch site ' + group_it.index[0]+ ' selected for lowest contamination levels'



if __name__ == '__main__':
    app.run_server(debug=True,port=8000, host='127.0.0.1')
    
