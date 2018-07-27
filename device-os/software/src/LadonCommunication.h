/*
 * LadonCommunication
 * 
 * MQTT communication handler.
 */

/* VARIABLES */
WiFiClient espClient;
PubSubClient mqttClient(espClient);

/* FUNCTIONS */
void mqttReconnect(void) {

  // Loop until we're reconnected
  while (!mqttClient.connected()) {

    Serial.print("Attempting MQTT connection...");

    // Attempt to connect
    if (mqttClient.connect(MQTT_CLIENT_ID)) {
      Serial.println("Connected to MQTT broker");
    } else {

      Serial.print("Failed to connect to MQTT broker, rc=");
      Serial.print(mqttClient.state());
      Serial.println(", trying again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);

    }

  }

}

void startCommunication(void) {

	// MQTT Setup
	mqttClient.setServer(MQTT_BROKER, 1883);
	//mqttClient.setCallback(callback);

}

void handleCommunication(void) {

	// Handling MQTT connection
	if (!mqttClient.connected()) {
		mqttReconnect();
	}
	mqttClient.loop();

}

void sendPackage(String topic, float value) {

  // Creates JSON string and publishes it
  String toPublish = "{\"content\":\"number\",\"value\":" + String(value) + "}";
  mqttClient.publish(topic.c_str(), toPublish.c_str());

}
