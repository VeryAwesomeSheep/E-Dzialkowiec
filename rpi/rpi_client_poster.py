#***************************************************************
#* Project:   Inzynierski Projekt Zespolowy 1
#* Authors:   Marcin Ficek, Marcel Baranek
#*            Andrzej Miszczuk, Grzegorz Kostanski
#* Created:   ZUT - 2023
#*
#* Name:      rpi_client_poster.py
#* Purpose:   Raspberry Pi TCP client for collecting data from
#*            ESP8266 servers with sensors and sending it
#*            via GPRS to the server.
#**************************************************************/
from tools.rpi_tools import *

# SIM800L module configuration
PIN = ""
USER = None
PASS = None
APN = ""
DEST_URL = ""

# ESP8266 servers information
HOSTS = []
PORT = None

# Reporting interval in seconds
INTERVAL = 60

if __name__ == "__main__":
  if initializeGPRS(PIN, APN, USER, PASS):
    while True:
      time.sleep(INTERVAL)
      data = readDataFromSensors(HOSTS, PORT)
      sendDataOverGPRS(DEST_URL, data)