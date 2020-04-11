import dash                             # Para instanciar la app
import dash_html_components as html     # Componentes de HTML
import dash_core_components as dcc      # Conecta la app con el backend (plots) y hace cosas de Js (interactividad)
                                        # Combina cosas de React.js
import dash_auth
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from sklearn import datasets            # para importar bases de datos
from dash.dependencies import Input, Output # para tomar datos y producir resultados en base a acciones (reactive)

def load_df():
    '''
    Retorna un df de el iris dataset
    '''
    data = datasets.load_iris().data            # Colectar los datos del iris
    cols = datasets.load_iris().feature_names   # Colect los nombres de las columnas
    df = pd.DataFrame(data=data, columns=cols)  # Crear df con los datos y las columnas del iris
    df['target'] = datasets.load_iris().target  # Añade la categoría de target al df con los valores de load_iris().target
    return df

df = load_df()                  # Instancia del DataFrame
app = dash.Dash()               # Instancia de la app
VALID_USERNAME_PASSWORD_PAIRS = [['User','Psw']]
auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)

app.layout = html.Div([                 # Lo que se va a mostrar: elementos html cuyos hijos son listas desplegables usando dcc
    html.H1('Iris Visualization'),
    html.Div([
          dcc.Dropdown(                 # Lista desplegable
               id='dropdown1',
               # options: recibe lista de diccionarios que tienen 'label' y 'value'
               # 'label' es lo que el usuario ve
               # Las opciones serán las primeras 4 columnas del df
               options=[{'label':i,'value':i} for i in df.columns[:4]],
               value=df.columns[0]      # Valor por defecto a mostrar en la app
          )
    ], style={'width':'50%', 'display':'inline-block'}),     # display: inline-block para que lo siguiente siga ocupando la misma caja
    html.Div([
          dcc.Dropdown(                 # Lista desplegable
               id='dropdown2',
               # options: recibe lista de diccionarios que tienen 'label' y 'value'
               # 'label' es lo que el usuario ve
               # Las opciones serán las primeras 4 columnas del df
               options=[{'label':i,'value':i} for i in df.columns[:4]],
               value=df.columns[1]      # Valor por defecto a mostrar en la app
          )
    ],style={'width':'50%','float':'right'}),
    dcc.Graph(id='main-plot',
              config={'displayModeBar': False}  # Quitar barra de herramientas superior
    )
], style={'width':'80%', 'margin-left':'auto', 'margin-right':'auto'})

'''
¿Cómo puedo hacer que mi aplicación lea/escuche/reciba un feedback reactivo y
cambie según las diferentes entradas?
Debe tomar los valores de los menús desplegables, seleccionar las columnas deseadas
del df del pandas, aplicar acciones a los datos y luego retornar el plot al layout-Graph
La forma de hacerlo es con callbacks: wrapper "cápsulas o envolturas" de funciones (¿decoradores?)
'''

@app.callback(                  # Decorador
    # Cada que se hacen cambios en los dropdown, hay Input, el decorador llama la función y saca el Output
    # Hace un monitoreo de datos de entrada
    Output('main-plot','figure'),    # ID del retorno y el tipo de retorno (plotly figure)
    # # plotly figure: bar chart, line graph, mapa de coropletas, etc...
    # # Tiene 2 componentes: data y layout para que se vean bonitos los datos
    # # Ese el plotly figure lo que lo hace reactive
    [Input('dropdown1','value'),    # el objeto que escuchas y lo que quieres escuchar de él
                                    # el valor del menú desplegable cambia cada que clickeas en él un valor diferente
    Input('dropdown2','value')]
    )
def plotly_maker(col1,col2):
#     '''
#     Returns plotly figure for desire columns: ergo, data + layout
#     '''
    data = []                   # Lista de traces.
    # Se hará una traza que sostiene la data que quiero mostrar en el plotly Graph
    # trace is a plotly object
    colors = ['blueviolet','darkcyan','darkseagreen']
    # Vamos a poner los nombres de las trazas respectivas usando la info de load_iris()
    names = datasets.load_iris().target_names
    for target in range(3):
        trace = go.Scatter(
            # Pasar una máscara (arreglo de True-False) al df de pandas para que sólo seleccione 0, 1, 2
            # Luego extrae la col1 asociada
            x = df[df['target']==target][col1],
            y = df[df['target']==target][col2],
            # Nombres de las trazas
            name = names[target],
            # Para que se vean los puntos, no las líneas
            mode='markers',
            marker={'size':16,
                    'opacity':0.8,
                    'line':{'color': 'black'},
                    'color':colors[target]
            }
        )
        data.append(trace)

    layout = go.Layout(
        xaxis={'title':col1},
        yaxis={'title':col2},
        margin={'l':120, 'b':0, 't':50, 'r':0},
        # Al pasar el cursos sobre las marcas de datos, se verán lo que valen
        # en x e y
        # Por defecto, muestra el dato más cercano a la línea media
        # para todas las gráficas con puntos sobre la misma vertical
        hovermode='closest'
     )
    return {'data': data, 'layout': layout}


if __name__ == '__main__':
    # Debug=True: para mostrar cambios de la app en el browser, se guardan automáticamente
    # port=8052: se "almacena" o direcciona la app en ese puerto. El browser busca la app que esté en el puerto dado
    app.run_server(debug=True, port=8052)
