#this is the dash_test.py file
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import random
app = dash.Dash(__name__)

app.layout = html.Div(html.Img(src=app.get_asset_url('meter.png')),style={'height':'10%'})


if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
