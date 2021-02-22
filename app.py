 
 # ABOUT:

 # We're using Dash for making the dashboard.
 # Developed as an open-source library by Plotly, 
 # the Python framework Dash is built on top of Flask, Plotly.js, and React.js. 
 # Dash allows the building of interactive web applications in pure Python 
 #  and is particularly suited for sharing insights gained from data.


 # pip install dash==1.19.0

import dash
import dash_html_components as html
import pandas as pd

# Load data
df = pd.read_csv('data/data.csv', index_col=0, parse_dates=True)
df.index = pd.to_datetime(df['Date'])

# Initialise the app
app = dash.Dash(__name__)

# Define the app
app.layout = html.Div()
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

app.layout = html.Div(children=[
                      html.Div(className='row',  # Define the row element
                               children=[
                                  html.H2('STAPPAOT - Online Attendance Capturing Tool'),
                                  html.P('''Visualising time series with Plotly - Dash'''),
                                  html.P('''Pick one or more stocks from the dropdown below.''')
                                  ])
                                ])