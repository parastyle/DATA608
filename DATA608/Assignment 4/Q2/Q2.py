# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 20:34:43 2018

@author: Exped
"""

# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

raw_data = pd.read_csv('https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/master/module4/Data/riverkeeper_data_2013.csv')
raw_data['Date'] = pd.to_datetime(raw_data['Date'])
raw_data['EnteroCount'] = raw_data['EnteroCount'].map(lambda x: x.lstrip('><'))\
                                     .astype(int)
sites = raw_data['Site'].unique()
dictList = []
for k in sites:
    dictList.append({'label': k, 'value' : k})

def plot_it(input_data,raw_data):
    group_it = raw_data[raw_data['Site'].isin(input_data)]
    plotted = []
    for i in group_it.Site.unique():
        df_by_site = group_it[group_it['Site']==i]
        plotted.append(go.Scatter(
                x=df_by_site['FourDayRainTotal'],
                y=df_by_site['EnteroCount'],
                text=df_by_site['SampleCount'],
                mode='markers',
                opacity=.65,
                marker={
                        'size':10,
                        'line': {'width':.4,'color':'white'}
                        },
                name=i
                ))
    return {
        'data': plotted,
        'layout': go.Layout(
            xaxis={'type': '-', 'title': 'Water quality'},
            yaxis={'title': 'Rain'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }
                  
app = dash.Dash()

app.layout = html.Div([
        
     dcc.Dropdown(
        id='dropdown',
        options=dictList,
        value=['MTL', 'SF'],
        multi=True
    ),
    html.Div(id='output-decision'),
    dcc.Graph(id='output-graph')
])

@app.callback(
    dash.dependencies.Output('output-graph', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_figure(input_data):
    print(input_data)
    return plot_it(input_data,raw_data)




if __name__ == '__main__':
    app.run_server(debug=True,port=8000, host='127.0.0.1')
    
#FourDayRainTotal
#EnteroCount
#SampleCount
#Date
#Site