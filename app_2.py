descripcion='''
    Esta API muestra gráficas de diferentes precios
    de 6 diferentes combustibles en los Estados y Regiones de Brasil
    entre los años 2004 y 2019.
'''

# %% Importar Módulos
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output,Input,State
import pandas as pd
import os
import numpy as np
import plotly.graph_objects as go
# from ipywidgets import widgets, interactive_output
# from plotly.subplots import make_subplots
from tabulate import tabulate
# from tqdm import tqdm
# from time import time

# %% Configuración inicial del DataFrame
df = pd.read_csv('./2004-2019.tsv',sep = '\t',index_col = 0)
df.columns = ['fecha_inicial',
    'fecha_final',
    'region',
    'estado',
    'producto',
    'num_postes_revisados',
    'unidad_medida',
    'precio_medio_reventa',
    'desviacion_estandar_reventa',
    'precio_min_reventa',
    'precio_max_reventa',
    'margen_medio_reventa',
    'coef_variacion_reventa',
    'precio_medio_distribucion',
    'desvia_estand_distribucion',
    'precio_min_distribucion',
    'precio_max_distribucion',
    'coef_variacion_distribucion',
    'mes','ano']
df_ano = list(df.ano.unique())
df_mes = list(df.mes.unique())

# %% Arquitectura HTML
app = dash.Dash(__name__)
# Banner
encabezado = html.Div(html.H2(['Precios de la gasolina en Brasil']), className = "encabezado")
banner = html.Div([
                html.Img(id='img-fondo',src = "/assets/fondo1.png"),
                html.Img(id='img-gasolina',src = "/assets/gas.png"),
				encabezado,
                html.Img(id='img-udea',src = "/assets/Logo_UdeA.png"),
                html.Img(id='img-semillero',src = "/assets/failed_logo_semillero.png"),
                html.Div(className='clear')
        ], className = "banner")
# Lado izquierdo
col_1 = html.Div([
                html.Div(dcc.Dropdown(
                        options=[{'label':i,'value':i} for i in df.estado.unique()],
                        value = df.estado.unique()[0],
                        id ='estado',
                    ),className='style_estados'),
                html.Div(dcc.Dropdown(
                        options=[{'label':i,'value':i} for i in df.producto.unique()],
                        value = df.producto.unique()[0],
                        id = 'producto',
                    ),className='style_productos'),
                html.Div(dcc.Dropdown(
                        options=[{'label':i,'value':i} for i in df.ano.unique()],
                        value = df.ano.unique()[0],
                        id ='ano',
                    ),className='style_ano'),
                html.Div([dcc.Graph(className = 'style_grafica',id = 'figura1')]),
                html.Div([dcc.Graph(className = 'style_grafica',id = 'figura3')]),
                html.Div([dcc.Graph(className = 'style_grafica',id = 'figura2')]),
                html.Div([dcc.Graph(className = 'style_grafica',id = 'figura4')]),
                html.Div(className='clear')
        ],className = 'style_row_1')
# Lado derecho
col_2 = html.Div([
                html.Div(html.H3(descripcion),className='style_E'),
                html.Div(dcc.Dropdown(
                        options=[{'label':i,'value':i} for i in df.region.unique()],
                        value = df.region.unique()[0],
                        id = 'region',
                    ),className='style_F'),
                html.Div([dcc.Graph(id = 'figura5')]),
                html.Div(className='clear')
        ],className = 'style_row_2')

container = html.Div([col_1, col_2])
app.layout = html.Div([banner, col_1, col_2], className = "main")
# %%

# %% Interactividad: de los Dropdown a los Graphs
@app.callback([
    Output(component_id ='figura1', component_property ='figure'),
    Output(component_id ='figura2', component_property ='figure'),
    Output(component_id ='figura3', component_property ='figure'),
    Output(component_id ='figura4', component_property ='figure')
    ],

    [
    Input(component_id='estado', component_property='value'),
    Input(component_id='producto',component_property='value'),
    Input(component_id='ano', component_property='value'),
    ])

def grafica(estado,producto,ano):
    '''
    Retorna una tupla con las 3 gráficas del lado izquierdo:
        1. Precios de Reventa vs Año
        2. Precios de Distribución vs Año
        3. Número de estaciones revisadas
    Las gráficas de precios muestran Mínimos, Medios y Máximos.
    Primero crea los datos (trazas tipo Scatter)
    Luego crea 3 instancias de tipo go.Figure() con data igual a sus respectivos traces
    Luego le añade un layout las 3 figuras para que los datos o trazas se puedan mostrar.
    '''
    # GOAL: Hacer un ciclo que cree las 3 traces

    names = ('Min','Medio','Max')   # Tupla de identificaciones de precios y nombres de las gráficas
    traces=[[],[],[],[]]              # Lista de 2 listas: traces figura 1 y 2
    for trc in range(len(traces)):   # trc = 0, 1, 2       # Vamos a crear las 2 figuras basadas en precios vs año
        if trc<=1:
            for p in range(len(names)):      # Almacenar las 3 trazas en las 2 sublistas
                traces[trc].append(go.Scatter(
                    x=df_ano,
                    y=list(df[(df.producto == producto) & (df.estado == estado)]
                        .groupby(['ano','estado'])[f'precio_{names[p].lower()}_'+('reventa' if trc==0 else 'distribucion')]
                        .agg('sum')), name=names[p]) )
        if trc>=2:
            traces[trc].append(go.Bar(
                x=df_ano,
                y=list(df[(df.producto == producto) & (df.estado == estado) & ((df.ano == ano) if trc==3 else True)]
                    .groupby([('mes' if trc==3 else 'ano'),'estado'])['num_postes_revisados']
                    .agg('sum')), name='Postes revisados por '+('mes' if trc==3 else 'año')) )

        # traces = go.Bar(x=df_mes,
        #         y=list(df[(df.producto == 'GLP') & (df.estado == 'SAO PAULO') & ((df.ano == 2009) if trc==3 else True)]
        #             .groupby([('mes' if trc==3 else 'ano'),'estado'])['num_postes_revisados']
        #             .agg('sum')),name='Postes revisados por '+('mes' if trc==3 else 'año'))
    traces4 = go.Bar(x=df_mes,
                     y=list(df[(df.producto == producto) & (df.estado == estado) & (df.ano == ano)]
                            .groupby(['mes','estado'])['num_postes_revisados']
                            .agg('sum')),name='Postes revisados')

    # Instancias de las 4 figure del lado izquierdo
    fig1 = go.Figure(data = traces[0])
    fig2 = go.Figure(data = traces[1])
    fig3 = go.Figure(data = traces[2])
    fig4 = go.Figure(data = traces[3])
    figs = [fig1, fig2, fig3]
    titles = ['Precio Reventa','Precio Distribucion','# de est revisadas al año',"# de est revisadas al mes"]
    meses = ["mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre","enero","febrero","marzo","abril"]
    # Seting de datos y layout de las primeras 3 figuras
    for fig,title in zip(figs,titles):
        fig.update_layout(
            margin = {'l':0,'r':0,'t':0,'b':0},
            xaxis=dict(
                title_text="Año",
                ticktext=df_ano,
                tickvals=df_ano
            ),
            yaxis=dict(
                title_text=title,
            ),)
        fig.update_traces(opacity=0.7)
    # Seting de datos y layout de la 4ta figura
    fig4.update_layout(
        margin = {'l':0,'r':0,'t':0,'b':0},
        xaxis=dict(
            title_text="Mes",
            ticktext=meses,
            tickvals=df_mes
        ),
        yaxis=dict(
            title_text=titles[3]
        )
    )
    fig4.update_traces(opacity=0.7)
    figs.append(fig4)
    return figs
# %% Crear la gráfica del lado derecho: precios de los 6
@app.callback(
            # [
                Output(component_id = 'figura5', component_property = 'figure'),
            # ],
            [
                Input(component_id = 'region', component_property = 'value'),
            ])

def grafica2(region):
    df_temp = df[df.region == region]['estado'].unique()
    productos =['ETANOL HIDRATADO','GASOLINA COMUM','GLP','GNV','ÓLEO DIESEL','ÓLEO DIESEL S10']
    data =[go.Bar(name= prod, x=df_temp, y=df[df.producto == prod].groupby(['ano','estado','producto']).precio_medio_reventa.sum()) for prod in productos]
    fig = go.Figure(data = data)
    fig.update_layout(
        margin = {'l':0,'r':0,'t':0,'b':0},
        xaxis=dict(
            title_text="Estados de " + region,
            ticktext=df_temp,
            tickvals=df_temp
        ),
        yaxis=dict(
            title_text="Precio medio de reventa",
        ))

    return(fig)

# %% Ejecución del programa
if __name__ == "__main__":
    app.run_server(debug=True, port=8051)
