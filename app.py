# -*- coding: utf-8 -*-
"""
Created on Sat May 26 17:58:32 2018

@author: Szymon S
"""

import pandas as pd
import numpy as np
import psycopg2

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import json


conn_params = dict(host='85.194.245.31',
                   port='5432',
                   database='locit_sample',
                   user='sample_user',
                   password='!TajemniczaTajemnica7'
                   )


app = dash.Dash(__name__)

app.css.append_css({'external_url': 'https://github.com/sapkos/hackathon_app/blob/master/hackathon_app.css'})
app.css.append_css({'external_url': 'https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css'})

app.config.supress_callback_exceptions=True
categories = dict(Cat_1=['Restauracje','FastFood'], Cat_2=['uslugi_medyczne','Sklep'], Cat_3=['Przedszkola','Hazard'])

n_clicks = [0,0,0]
colors = ['#ff5454', '#ffff54', '#eeff00', '#8fff54', '#00ff19']

app.layout = html.Div([
      
         html.Div([
               html.H2("Twój biznes!")     
         ], className='banner'),
         
         html.Div([
               dcc.Markdown("""
  #### Witaj na stronie Twoj Biznes!
  Pomożemy Ci otworzyc Twój biznes,
  wybierz kategorie swojego biznesu
                            """)
         ], className='banner'),

         html.Div([
               html.Button('Gastronomia',
                           id='Cat_1',
                           n_clicks=0,
                           style={'width': '33%',
                                  'background-color': 'powderblue'}),
               html.Button('Handel',
                           id='Cat_2',
                           n_clicks=0,
                           style={'width': '33%',
                                  'background-color': 'powderblue'}),
               html.Button('Usługi',
                           id='Cat_3',
                           n_clicks=0,
                           style={'width': '33%',
                                  'background-color': 'powderblue'})
         ]),
         html.Br(),
         html.Div(id='subcat-dropdown', style={'width':'50%'}),
         dcc.Graph(
               id = "mapbox",
               figure={},
               style = {"height": "100vh"}
         )
         
   ], style={'padding': '0px 10px 15px 10px',
             'marginLeft': 'auto', 'marginRight': 'auto', "width": "900px",
             'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'})

@app.callback(Output('subcat-dropdown', 'children'),
              [dash.dependencies.Input('Cat_{}'.format(i),'n_clicks') for i in range(1, 4)])
def update_output(cat1, cat2, cat3):
   clicked = None
   if cat1 != n_clicks[0]:
      n_clicks[0]+=1
      clicked = 'Cat_1'
   elif cat2 != n_clicks[1]:
      n_clicks[1]+=1
      clicked = 'Cat_2'
   elif cat3 != n_clicks[2]:
      n_clicks[2]+=1
      clicked = 'Cat_3'
   else:
      return None
   return dcc.Dropdown(id='subcat-dropdown-dropdown', 
                       options=[{'label': j, 'value': j} for j in categories[clicked]])

   
@app.callback(Output('mapbox', 'figure'),
              [Input('subcat-dropdown-dropdown', 'value')])
def update_graph(category):
   pred = pd.read_csv(category+'_xy.csv')
   figure = {
                 "data": [go.Scattermapbox(
                 lat=pred[pred['digits']==i]['grid_y'].values,
                 lon=pred[pred['digits']==i]['grid_x'].values,
                 mode='markers',
                 marker=dict(
                     size=30,
                     opacity=i/(3*pred['digits'].max()),
                     color=colors[i]
                 ),
                 text='Grupa_{}'.format(i)  
                 ) for i in range(0, 5)],
                 "layout": dict(
                     autosize = True,
                     hovermode = "closest",
                     margin = dict(l = 0, r = 0, t = 0, b = 0),
                     mapbox = dict(
                         accesstoken = 'pk.eyJ1Ijoic3p5bWVrazk1IiwiYSI6ImNqZ3BqcHN6ZjJ0dngycW84OGZnaHdoaGMifQ.xVWsCrwXz-6qYX5MYJjmoQ',
                         bearing = 0,
                         pitch = 0,
                         zoom=12,
                         center=dict(
                               lat=50.062204,
                               lon=19.938160
                               )
                     )
                 )
            }
   return figure 

if __name__ == '__main__':
   app.run_server()