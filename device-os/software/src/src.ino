/*
 * LadonManager
 * 
 * Ladon modules handler.
 */

/* LIBRARIES */
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

/* DEFINES */
#define WIFI_SSID		"Goes"
#define WIFI_PSK		"23523373"
#define HOSTNAME		"deviceos"

#define MQTT_BROKER		"lgateway.local"
#define MQTT_CLIENT_ID	"device-os"

#define POOLING_TIME	60000 // milliseconds

#define DEVICE_HASH		"vzyJYkThrw9u9gP5"

/* MODULES */
#include "LadonConnection.h"
#include "LadonCommunication.h"
#include "LadonSensor.h"

/* SETUP */
void setup() {

	// Serial Setup
	Serial.begin(115200);

	// Starts connection, communication and sensor modules
	startConnection();
	startCommunication();
	startSensor();

}

/* LOOP */
void loop() {

	handleCommunication();

	// Verify if the pooling time has been reached
	unsigned long now = millis();
	if(now - lastSensorReading >= POOLING_TIME || lastSensorReading == 0UL) {

		// Gets reading
		float reading = readSensor();

		// Creates topic
		String topic = "/ladon/";
		topic += String(DEVICE_HASH);

		// Creates JSON string and publishes it
		String toPublish = "{\"type\":\"number\",\"description\":\"temperature\",\"value\":"
							+ String(reading) + "}";

		Serial.println("Temperature: " + String(reading));
		mqttClient.publish(topic.c_str(), toPublish.c_str());

		lastSensorReading = now;

	} else {

		// Verify if millis has reseted
		if(now - lastSensorReading < 0) { lastSensorReading = 0UL; }

	}

	delay(1000);

}
