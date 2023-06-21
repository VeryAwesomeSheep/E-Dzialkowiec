# E-Działkowiec++
E-Działkowiec++ is a project made for the subject "Engineering team project 1" at the West Pomeranian University of Technology in Szczecin.<br><br>
This project implements a simple system of collecting data from a garden.<br><br>
System consists of three parts:
* [Server] - Flask server that revceives data from the garden, stores it into a database and presents it on a simple website.
* [Master controller] - Raspberry Pi Zero W that collects data from sensors and after aggregation sends it to the server.
* [Slave controllers] - At the moment, three ESP8266 controllers that collect data from DHT11 sensor and send it to the master controller.

Communication between the garden and the server is done via HTTP requests sent via GPRS.<br>
Communication between the master controller and the slave controllers is done via TCP protocol.