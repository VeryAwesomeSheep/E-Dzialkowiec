/***************************************************************
 * Project:   Inzynierski Projekt Zespolowy 1
 * Authors:   Marcin Ficek, Marcel Baranek
 *            Andrzej Miszczuk, Grzegorz Kostanski
 * Created:   ZUT - 2023
 *
 * Name:      esp_server.c
 * Purpose:   ESP8266 TCP server for collecting and sending
 *            data from sensor to the main controller
***************************************************************/

#include <ESP8266WiFi.h>
#include "DHT.h"

/* WiFi credentials */
const char* ssid = "";
const char* passowrd = "";

/* WiFi configuration */
#define PORT NULL
WiFiServer server(PORT);
WiFiClient client;

/* DHT configuration */
#define DHTPIN 2
DHT dht;

/* Structures */
typedef struct DHTData {
  float temperature;
  float humidity;
} DHTData;

/* Function declarations */
DHTData getDHT();
void printDHTSerial(DHTData *data);

/* Function definitions */
void setup() {
  Serial.begin(9600);
  delay(1000);

  // Setup DHT sensor
  Serial.println("Starting DHT sensor...");
  dht.setup(DHTPIN);
  Serial.println("DHT sensor active.");

  // Setup WiFi server
  Serial.println("Starting ESP8266 server...");
  WiFi.begin(ssid, passowrd);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print("Connecting...");
  }
  Serial.println("Connected to WiFi.");
  Serial.println(WiFi.localIP());

  server.begin();
  Serial.println("Server started.");
}

void loop() {
  client = server.accept();

  if (client) {
    Serial.print("New client: ");
    Serial.println(client.remoteIP());

    if (client.connected()) {
      DHTData data = getDHT();
      printDHTSerial(&data);

      client.write((int)data.temperature);
      client.write((int)data.humidity);
    }

  client.stop();
  Serial.println("Client disconnected.");
  }
}

/* Since DHT11 sensor range is 0-50C and 20-80% then 126 is used as error code
   which is later checked on the server before putting into database */
DHTData getDHT() {
  DHTData data;
  data.temperature = dht.getTemperature();
  if (isnan(data.temperature)) {
    Serial.println("Failed to read temperature from DHT sensor.");
    data.temperature = 126;
  }
  data.humidity = dht.getHumidity();
  if (isnan(data.humidity)) {
    Serial.println("Failed to read humidity from DHT sensor.");
    data.humidity = 126;
  }

  return data;
}

void printDHTSerial(DHTData *data) {
  Serial.print("Temperature: ");
  Serial.print(data->temperature);
  Serial.print(" Humidity: ");
  Serial.println(data->humidity);
}