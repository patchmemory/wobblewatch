#this is the dash_test.py file
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import random
app = dash.Dash(__name__)
#app.layout = html.H1('hello dash')

#app.layout = html.Div(
#    [
#        html.Button('Generate random number', 
#            id='button1',
#            style={'display':'block', 'background-color':'#aabbcc'}
#        ),
#        html.Label('...', 
#            id='label1', 
#            style={'display':'inline-block', 'margin':'10'} 
#        )
#    ]
#)
#
#@app.callback(
#    Output(component_id='label1', component_property='children'),
#    [Input(component_id='button1', component_property='n_clicks')]
#)
#def update_output(input_value):
#    return random.random()
#
app.layout = html.Div(
    [
        html.Button('create random number', 
            id='button1',
            style={'display':'block', 'padding':'5', 'background-color':'#aabbcc'}),
        html.Label('…', 
            id='label1', 
            style={'display':'inline-block', 'margin':'10'} ),
        dcc.Graph(id='graph1') # this is the graph we add
    ]
)

@app.callback(
    Output(component_id='graph1', component_property='figure'),
    [Input(component_id='button1', component_property='n_clicks')]
)
def update_output(input_value):
    random_x = [i for i in range(5)]
    random_y = [random.random() for _ in range(5)]
    figure = {
        'data': [
            {'x':random_x, 'y':random_y, 'type':'bar', 'name': 'Series1'}
        ],
        'layout': {
            'title': 'Dash Data Visualization'
        }
    }
    return figure

if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
