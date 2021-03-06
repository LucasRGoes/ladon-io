/*
 * LadonManager
 * 
 * Ladon modules handler.
 */

/* LIBRARIES */
#include "DHTesp.h"
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

/* DEFINES */
#define WIFI_SSID		"Ladon_TCC"
#define WIFI_PSK		"Mko09ijN"
#define HOSTNAME		"ldevice"

#define MQTT_BROKER		"192.168.0.2" // "lgateway.local"
#define MQTT_CLIENT_ID	"ldevice"
#define MQTT_USERNAME	"ladon"
#define MQTT_PASSWORD	"ladon"

#define DHTPIN 			D4    // what digital pin the DHT22 is conected to
#define POOLING_TIME	60000 // milliseconds

#define DEVICE_ID		"vzyJYkThrw9u9gP5"

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

		// Creates topic
		String topic = "ladon/";
		topic += String(DEVICE_ID);
		topic += "/feature/";

		// Gets temperature reading and validate
		float temperature = readTemperature();
		if(!isnan(temperature)) {
			Serial.println("Temperature: " + String(temperature));
			sendPackage(topic + "1", 1, temperature);
		} else {
			Serial.println("Failed to read temperature!");
		}

		// Gets humidity reading and validate
		float humidity = readHumidity();
		if(!isnan(humidity)) {
			Serial.println("Humidity: " + String(humidity));
			sendPackage(topic + "2", 2, humidity);
		} else {
			Serial.println("Failed to read humidity!");
		}

		lastSensorReading = now;

	} else {

		// Verify if millis has reseted
		if(now - lastSensorReading < 0) { lastSensorReading = 0UL; }

	}

	delay(1000);

}
