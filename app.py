# -*- coding: utf-8 -*-
"""
Created on Sat May 26 17:58:32 2018

@author: Szymon S
"""

import pandas as pd
import numpy as np


import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go


app = dash.Dash(__name__)

app.css.append_css('hackathon_app.css')

app.layout = html.Div([
      
      
      
      ])




if __name__ == '__main__':
   app.run_server()