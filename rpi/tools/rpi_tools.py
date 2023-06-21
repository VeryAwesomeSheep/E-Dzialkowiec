#***************************************************************
#* Project:   Inzynierski Projekt Zespolowy 1
#* Authors:   Marcin Ficek, Marcel Baranek
#*            Andrzej Miszczuk, Grzegorz Kostanski
#* Created:   ZUT - 2023
#*
#* Name:      rpi_client_poster.py
#* Purpose:   Helper functions for Raspberry Pi.
#**************************************************************/
import socket, time, json, serial
from datetime import datetime

terminal = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)

ASCII = ['\0', '\1', '\2' '\3', '\4', '\5', '\6', '\a', '\b', '\t', '\n', '\v', '\f', '\r',
         '\x0e', '\x0f', '\x10', '\x11', '\x12', '\x13', '\x14', '\x15', '\x16', '\x17', '\x18',
         '\x19', '\x1a', '\x1b', '\x1c', '\x1d', '\x1e', '\x1f']

def readDataFromSensors(HOSTS, PORT):
  print('Reading data from sensors...')

  data = []
  for HOST in HOSTS:
    sensorData = []
    try:
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.connect((HOST, PORT))
      print('Connected to {}:{}.'.format(HOST, PORT))

      while True:
        sensorData.append(s.recv(4))
        if len(sensorData) == 2: break
      s.close()
      print('Disconnected from {}:{}.'.format(HOST, PORT))
    except socket.error:
      print('Connection to {}:{} failed.'.format(HOST, PORT))
      pass

    data.append(sensorData)

  try:
    for i in range(len(data)):
      for j in range(2):
        if data[i][j] in ASCII:
          data[i][j] = convertNonPrintableASCIIToDec(data[i][j])
        else:
          data[i][j] = ord(data[i][j])
  except IndexError:
    pass

  print('Data read completed.')

  return data

def preparePayload(data):
  header = "application/json"

  payload = {
    'date': getCurrentTime()[0],
    'time': getCurrentTime()[1]}

  for i in range(3):
    try:
      payload.update({'sensor{}temp'.format(i+1): data[i][0]})
      payload.update({'sensor{}hum'.format(i+1): data[i][1]})
    except IndexError:
      payload.update({'sensor{}temp'.format(i+1): 126})
      payload.update({'sensor{}hum'.format(i+1): 126})

  return header, payload

def initializeGPRS(PIN, APN, USER=None, PASS=None):
  print('Initializing GPRS...')

  # Check if SIM800L is connected
  response = writeCMD('AT')
  if 'OK' not in response: return False

  # Enable verbose error messages
  response = writeCMD('AT+CMEE=2')
  if 'OK' not in response: return False

  # Check if SIM card is ready and unlocked
  response = writeCMD('AT+CPIN?')
  if 'OK' not in response:
    # Unlock SIM card
    response = writeCMD('AT+CPIN={}'.format(PIN))
    if 'OK' not in response: return False

  # Check if SIM card is ready and unlocked
  response = writeCMD('AT+CPIN?')
  if 'OK' not in response: return False

  # Configure APN
  repsponse = writeCMD('AT+SAPBR=3,1,APN,"{}"'.format(APN))
  if 'OK' not in response: return False

  # Configure user and password
  if USER != None:
    response = writeCMD('AT+SAPBR=3,1,USER,"{}"'.format(USER))
    if 'OK' not in response: return False
  if PASS != None:
    response = writeCMD('AT+SAPBR=3,1,PWD,"{}"'.format(PASS))
    if 'OK' not in response: return False

  print('GPRS initialized successfully.')

  return True

def sendDataOverGPRS(address, data):
  print('Sending data over GPRS...')

  header, payload = preparePayload(data)

  # Open GPRS connection
  response = writeCMD('AT+SAPBR=1,1')
  if 'OK' not in response: return False

  # Initialize HTTP service
  response = writeCMD('AT+HTTPINIT')
  if 'OK' not in response: return False

  # Set carrier profile identifier
  response = writeCMD('AT+HTTPPARA=CID,1')
  if 'OK' not in response: return False

  # Set HTTP URL
  response = writeCMD('AT+HTTPPARA=URL,"{}"'.format(address))
  if 'OK' not in response: return False

  # Set HTTP header
  response = writeCMD('AT+HTTPPARA=CONTENT,{}'.format(header))
  if 'OK' not in response: return False

  # Open HTTP data channel
  response = writeCMD('AT+HTTPDATA=192,5000')
  time.sleep(1)

  response = writeCMD('{}'.format(json.dumps(payload)))
  if 'OK' not in response: return False

  # Send HTTP POST request
  response = writeCMD('AT+HTTPACTION=1')
  if 'OK' not in response: return False

  # Verify HTTP POST request
  response = writeCMD('AT+HTTPREAD')
  if 'OK' not in response: return False

  # Terminate HTTP service
  response = writeCMD('AT+HTTPTERM')
  if 'OK' not in response: return False

  # Close GPRS connection
  response = writeCMD('AT+SAPBR=0,1')
  if 'OK' not in response: return False

  print('Data sent successfully.')

  return True

def writeCMD(cmd, printResponse=True):
  terminal.readall()
  command = cmd + '\r\n'
  terminal.write(command.encode())
  time.sleep(0.1)
  response = terminal.readall().decode()
  if printResponse: print('CMD: {} -> Response: {}'.format(cmd, response))
  else: print('CMD: {}'.format(cmd))

  return response

def getCurrentTime():
  date, time = datetime.now().strftime('%d-%m-%Y %H:%M:%S').split(' ')
  return date, time

def convertNonPrintableASCIIToDec(char):
    return ASCII.index(char)
