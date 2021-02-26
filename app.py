 
 # ABOUT:

 # We're using Dash for making the dashboard.
 # Developed as an open-source library by Plotly, 
 # the Python framework Dash is built on top of Flask, Plotly.js, and React.js. 
 # Dash allows the building of interactive web applications in pure Python 
 # and is particularly suited for sharing insights gained from data.


 # Create virtual environment -> pip install pandas, pip install dash

import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output

# Load data
df = pd.read_csv('data/data.csv', index_col=0, parse_dates=True)
df.index = pd.to_datetime(df['datetime'])

# Initialize the app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

server = app.server

def get_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})

    return dict_list


app.layout = html.Div(
    children=[
        html.Div(className='row',
                 children=[
                    html.Div(className='four columns div-user-controls',
                             children=[
                                 html.H2('Stappaot - Online Attendance Capturing Tool'),
                                 html.P('Dashboard of overall Attendance of the class'),
                                 html.P('Pick one or more Class from the dropdown below.'),
                                 html.Div(
                                     className='div-for-dropdown',
                                     children=[
                                         dcc.Dropdown(id='attendance', options=get_options(df['classID'].unique()),
                                                      multi=True, value=[df['classID'].sort_values()[0]],
                                                      style={'backgroundColor': '#1E1E1E'},
                                                      className='stockselector'
                                                      ),
                                     ],
                                     style={'color': '#1E1E1E'})
                                ]
                             ),
                    html.Div(className='eight columns div-for-charts bg-grey',
                             children=[
                                 dcc.Graph(id='timeseries', config={'displayModeBar': False}, animate=True)
                             ])
                              ])
        ]

)


# Callback for timeseries attendance
@app.callback(Output('timeseries', 'figure'),
              [Input('attendance', 'value')])
def update_graph(selected_dropdown_value):
    trace1 = []
    df_sub = df
    for stock in selected_dropdown_value:
        trace1.append(go.Scatter(x=df_sub[df_sub['classID'] == stock].index,
                                 y=df_sub[df_sub['classID'] == stock]['value'],
                                 mode='lines',
                                 opacity=0.7,
                                 name=stock,
                                 textposition='bottom center'))
    traces = [trace1]
    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 15},
                  hovermode='x',
                  autosize=True,
                  title={'text': 'Attendance Graph', 'font': {'color': 'white'}, 'x': 0.5},
                  xaxis={'range': [df_sub.index.min(), df_sub.index.max()]},
              ),

              }

    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
