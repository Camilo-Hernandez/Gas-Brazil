import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ipywidgets import widgets, interactive_output
from tabulate import tabulate
from tqdm import tqdm
from time import time

app = dash.Dash(__name__)

encabezado= html.Div([html.H1(['Precios de la gasolina en Brasil']),
						], className = "encabezado")

banner = html.Div([
				html.Img(id='img-udea',src = "/assets/Logo_UdeA.png"),
				html.Img(id='img-semillero',src = "/assets/failed_logo_semillero.png"),
				encabezado,
                html.Div(className='clear')
        ], className = "banner")

row_1 = html.Div([
                html.Div(html.H2(['Estados']),className='style_estados'),
                html.Div(html.H2(['Productos']),className='style_productos'),
                html.Div(html.H2(['Indicador 3']),className='style_grafica'),
                html.Div(html.H2(['Indicador 3']),className='style_grafica_2'),
                html.Div(html.H2(['Indicador 2']),className='style_grafica'),
                html.Div(html.H2(['Indicador 4']),className='style_grafica_2'),
                html.Div(className='clear')
        ],className = 'style_row_1')
row_2 = html.Div([
                html.Div(html.H2(['Texto']),className='style_E'),
                html.Div(html.H2(['Regiones']),className='style_F'),
                html.Div(html.H2(['Indicador 3']),id='style_H'),
                html.Div(className='clear')
        ],className = 'style_row_2')

container = html.Div([
					row_1,
					row_2
			])

app.layout = html.Div([banner,row_1,row_2],className = "main")


if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
