import pandas as pd
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import sqlite3
from datetime import datetime, timedelta
import plotly.express as px
import socket

port = 8080
host = socket.gethostbyname(socket.gethostname())

conn = sqlite3.connect('air-data.db')
conn.execute('pragma journal_mode=wal')
cursor =conn.cursor()

df = pd.read_sql("SELECT DATE,CO2,TEMP,HUM FROM AIRDATA ORDER BY DATE DESC LIMIT 100",conn)

app = dash.Dash(__name__)

#TODO: Improve the design
app.layout = html.Div([
    dcc.Interval(
            id='interval-component',
            interval=60*10000, # in milliseconds
            n_intervals=0
    ),
    dcc.Graph(id='CO2_plot'),
    dcc.Interval(
            id='interval-component2',
            interval=60*10000, # in milliseconds
            n_intervals=0
    ),
    dcc.Graph(id='T_plot'),
    dcc.Interval(
            id='interval-component3',
            interval=60*10000, # in milliseconds
            n_intervals=0
    ),
    dcc.Graph(id='H2O_plot'),
])




@app.callback(
    Output('CO2_plot', 'figure'),
    [Input('interval-component', 'n_intervals')])
def update_static_figure(n_intervals):
    fig = px.scatter(df,x="DATE",y="CO2")
    return fig


@app.callback(
    Output('H2O_plot', 'figure'),
    [Input('interval-component3', 'n_intervals')])
def update_static_figure(n_intervals):
    fig = px.scatter(df,x="DATE",y="HUM")
    return fig


@app.callback(
    Output('T_plot', 'figure'),
    [Input('interval-component2', 'n_intervals')])
def update_static_figure(n_intervals):
    fig = px.scatter(df,x="DATE",y="TEMP")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, host=host, port=port)
