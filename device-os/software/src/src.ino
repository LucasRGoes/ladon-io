/* LIBRARIES */
#include <ESP8266WiFi.h>

/* DEFINES */
#define WIFI_SSID	"Goes"
#define WIFI_PSK	"23523373"

#define MQTT_HOST	"raspberrypi.local"

#define HOSTNAME	"deviceos"

void setup() {

	// Serial Setup
	Serial.begin(115200);

	// WiFi Setup
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

}

void loop() {

	Serial.println("Teste");

	// Final delay
	delay(5000);

}