#***************************************************************
#* Project:   Inzynierski Projekt Zespolowy 1
#* Authors:   Marcin Ficek, Marcel Baranek
#*            Andrzej Miszczuk, Grzegorz Kostanski
#* Created:   ZUT - 2023
#*
#* Name:      db_tools.py
#* Purpose:   Helper functions for database operations.
#**************************************************************/
import sqlite3, json

def create_db():
  with sqlite3.connect('edzialkowiec.db') as con:
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS records
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   date TEXT,
                   time TEXT,
                   temperature1 REAL,
                   humidity1 REAL,
                   temperature2 REAL,
                   humidity2 REAL,
                   temperature3 REAL,
                   humidity3 REAL)''')
    con.commit()

def add_record(payload):
  create_db()

  record = [payload['date'], payload['time'], payload['sensor1temp'], payload['sensor1hum'], payload['sensor2temp'], payload['sensor2hum'], payload['sensor3temp'], payload['sensor3hum']]

  # 126 is a placeholder for unavailable data
  for i in range(len(record)):
    if record[i] == 126: record[i] = None

  with sqlite3.connect('edzialkowiec.db') as con:
    cur = con.cursor()
    cur.execute('INSERT INTO records VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)', record)
    con.commit()

def read_db_record(id):
  with sqlite3.connect('edzialkowiec.db') as con:
    cur = con.cursor()
    cur.execute('SELECT * FROM records WHERE id = ?', (id,))
    print(cur.fetchone())

def read_db_all():
  with sqlite3.connect('edzialkowiec.db') as con:
    cur = con.cursor()
    cur.execute('SELECT * FROM records')
    print(cur.fetchall())

def get_json():
  with sqlite3.connect('edzialkowiec.db') as con:
    cursor = con.cursor()
    cursor.execute('SELECT * FROM records')
    output = cursor.fetchall()

  return json.dumps(output)