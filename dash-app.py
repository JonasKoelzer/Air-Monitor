import pandas as pd
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
from dash.dependencies import Input, Output, State
import sqlite3
from datetime import datetime, timedelta
import plotly.express as px
import socket
import sys

port = 8080
host = socket.gethostbyname(socket.gethostname())

def get_connection():
    full_path = sys.argv[0].split("dash-app.py")[0]
    conn = sqlite3.connect(full_path+'air-data.db')
    conn.execute('pragma journal_mode=wal')
    return conn


app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Interval(
            id='interval-component4',
            interval=60*1000, # in milliseconds
            n_intervals=0
    ),
    html.Div(
            daq.Gauge(
                    id='CO2_gauge',
                    color={"gradient":True,"ranges":{"green":[4,7],"yellow":[7,15],"red":[15,20]}},
                    value=6,
                    label='CO2 in PPM',
                    max=20,
                    min=4,
            )
    ,style={'width': '49%', 'display': 'inline-block'}),
    html.Div(
            daq.Gauge(
                    id='HUM_gauge',
                    color={"gradient":True,"ranges":{"green":[40,70],"yellow":[0,40],"red":[70,100]}},
                    value=50,
                    label='Humidity in %',
                    max=100,
                    min=0,
            )
    ,style={'width': '49%', 'display': 'inline-block'}),
    dcc.Interval(
            id='interval-component',
            interval=60*1000, # in milliseconds
            n_intervals=0
    ),
    dcc.Graph(id='CO2_plot'),
    dcc.Interval(
            id='interval-component2',
            interval=60*1000, # in milliseconds
            n_intervals=0
    ),
    dcc.Graph(id='T_plot'),
    dcc.Interval(
            id='interval-component3',
            interval=60*1000, # in milliseconds
            n_intervals=0
    ),
    dcc.Graph(id='H2O_plot'),
])


@app.callback(
    Output('CO2_plot', 'figure'),
    [Input('interval-component', 'n_intervals')])
def update_static_figure(n_intervals):
    conn = get_connection()
    df = pd.read_sql("SELECT DATE,CO2,TEMP,HUM FROM AIRDATA ORDER BY DATE DESC LIMIT 100",conn)
    fig = px.scatter(df,x="DATE",y="CO2")
    return fig


@app.callback(
    Output('H2O_plot', 'figure'),
    [Input('interval-component3', 'n_intervals')])
def update_static_figure(n_intervals):
    conn = get_connection()
    df = pd.read_sql("SELECT DATE,CO2,TEMP,HUM FROM AIRDATA ORDER BY DATE DESC LIMIT 100",conn)
    fig = px.scatter(df,x="DATE",y="HUM")
    return fig


@app.callback(
    Output('T_plot', 'figure'),
    [Input('interval-component2', 'n_intervals')])
def update_static_figure(n_intervals):
    conn = get_connection()
    df = pd.read_sql("SELECT DATE,CO2,TEMP,HUM FROM AIRDATA ORDER BY DATE DESC LIMIT 100",conn)
    fig = px.scatter(df,x="DATE",y="TEMP")
    return fig

@app.callback(
    Output('CO2_gauge', 'value'),
    [Input('interval-component4', 'n_intervals')])
def update_static_figure(n_intervals):
    conn = get_connection()
    df = pd.read_sql("SELECT DATE,CO2,TEMP,HUM FROM AIRDATA ORDER BY DATE DESC LIMIT 1",conn)
    co2 = df["CO2"][0]
    return co2/100.

@app.callback(
    Output('HUM_gauge', 'value'),
    [Input('interval-component4', 'n_intervals')])
def update_static_figure(n_intervals):
    conn = get_connection()
    df = pd.read_sql("SELECT DATE,CO2,TEMP,HUM FROM AIRDATA ORDER BY DATE DESC LIMIT 1",conn)
    hum = df["HUM"][0]
    return hum


if __name__ == '__main__':
    app.run_server(debug=True, host=host, port=port)
