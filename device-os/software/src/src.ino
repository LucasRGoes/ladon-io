/* LIBRARIES */
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

/* DEFINES */
#define WIFI_SSID		"Goes"
#define WIFI_PSK		"23523373"

#define MQTT_BROKER		"raspberrypi.local"
#define MQTT_CLIENT_ID	"device-os"

#define HOSTNAME		"deviceos"

/* FUNCTIONS */
void mqttReconnect(void);

/* VARIABLES */
WiFiClient espClient;
PubSubClient mqttClient(espClient);

void setup() {

	// Serial Setup
	Serial.begin(115200);

	// WiFi Setup
	delay(10);
	Serial.print("\n\n");
	Serial.print("Connecting to ");
	Serial.print(WIFI_SSID);
	Serial.print(" ");

	// Setting mode and hostname
	WiFi.mode(WIFI_STA);
	WiFi.setAutoReconnect(true);
	WiFi.hostname(HOSTNAME);

	// Connecting to WiFi AP
	WiFi.begin(WIFI_SSID, WIFI_PSK);

	// Doesn't exit until connected
	while (WiFi.status() != WL_CONNECTED) {
		delay(500);
		Serial.print(".");
	}

	Serial.println("");
	Serial.println("WiFi connected");  
	Serial.print("IP address: ");
	Serial.println(WiFi.localIP());
	Serial.print("\n");

	// MQTT Setup
	mqttClient.setServer(MQTT_BROKER, 1883);
	//mqttClient.setCallback(callback);

}

void loop() {

	// Handling MQTT connection
	if (!mqttClient.connected()) {
		mqttReconnect();
	}
	mqttClient.loop();

	Serial.println("Publishing...");
	mqttClient.publish("Teste", "Teste");

	// Final delay
	delay(5000);

}

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