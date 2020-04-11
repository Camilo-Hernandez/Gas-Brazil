import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)

row_1 = html.Div([
                html.Div(html.H2(['A']),className='style_A'),
                html.Div(html.H2(['B']),className='style_B'),
        ])
row_2 = html.Div([])
row_3 = html.Div([])

app.layout = html.Div([row_1,row_2,row_3],className = "main")


if __name__ == "__main__":
    app.run_server(debug=True)
