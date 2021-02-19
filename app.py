from scd30_i2c import SCD30
from os import path
import sys
import time
import datetime
import apprise
import json
import sqlite3

#Set the full path to the repository:
full_path = sys.argv[0].split("app.py")[0]

#DB name setting:
db_path = "air-data.db"
db_path = full_path+db_path

#Set up the sensor:
scd30 = SCD30()
scd30.set_measurement_interval(2)
scd30.start_periodic_measurement()

#Get authentification credentials:
with open(full_path+"auth.json") as f:
    auth = json.load(f)

apobj = apprise.Apprise()
apobj.add('pover://'+str(auth["key"])+'@'+str(auth["token"]))

#Defining functions for the push notifications:
def send_open(CO2_value):
    apobj.notify(
        body='High CO2 concentration of '+str(int(CO2_value))+'ppm, open the windows please.',
        title='CO2 Warning',
    )
def send_close():
    apobj.notify(
        body='Low CO2 value reached. You may stop ventilation.',
        title='CO2 Note',
    )

#Set up a database at first start:
if not path.exists(db_path):
    conn = sqlite3.connect(db_path)
    conn.execute('''CREATE TABLE AIRDATA
        (DATE          TEXT PRIMARY KEY,
         CO2           REAL,
         TEMP          REAL,
         HUM           REAL);''')
    conn.close()

#Staring the measurements
high_CO2 = False

while True:
    if scd30.get_data_ready():
        conn = sqlite3.connect(db_path)
        m = scd30.read_measurement()
        if m is not None:
            ts = str(datetime.datetime.now().isoformat())
            print(f"{ts}, CO2: {m[0]:.2f}ppm, temp: {m[1]:.2f}'C, rh: {m[2]:.2f}%")
            if m[0] > 1500 and high_CO2==False:
                send_open(m[0])
                high_CO2=True
            if m[0] < 1000 and high_CO2:
                send_close()
                high_CO2=False
            conn.execute("INSERT INTO AIRDATA (DATE,CO2,TEMP,HUM) VALUES (?,?,?,?)",(ts,m[0],m[1],m[2]));
            conn.commit()
        conn.close()
        time.sleep(1)
    else:
        time.sleep(0.2)
