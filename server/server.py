#***************************************************************
#* Project:   Inzynierski Projekt Zespolowy 1
#* Authors:   Marcin Ficek, Marcel Baranek
#*            Andrzej Miszczuk, Grzegorz Kostanski
#* Created:   ZUT - 2023
#*
#* Name:      server.py
#* Purpose:   HTTP server for receiving data from Raspberry Pi,
#*            storing it in the database and displaying it.
#**************************************************************/

#run from home dir with "flask --app server run --debug --host=0.0.0.0 --port=7001"

from flask import Flask, url_for, redirect, render_template, request
import json, sqlite3
from tools.db_tools import *

app = Flask(__name__)

@app.route('/post_record', methods=['POST'])
def post_record():
  payload = request.json
  add_record(payload)

  return "200"

@app.route('/')
def index():
  create_db()

  with sqlite3.connect('edzialkowiec.db') as con:
    cursor = con.cursor()
    cursor.execute('SELECT * FROM records')
    output = cursor.fetchall()

  data = []
  for row in output:
    data.append({
      'id': row[0],
      'date': row[1],
      'time': row[2],
      'sensor1': "Temperatura: {}\nWilgotność: {}".format(row[3], row[4]),
      'sensor2': "Temperatura: {}\nWilgotność: {}".format(row[5], row[6]),
      'sensor3': "Temperatura: {}\nWilgotność: {}".format(row[7], row[8])
    })

  return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run()