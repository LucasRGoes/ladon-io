/*
 * LadonConnection
 * 
 * WiFi connection handler.
 */

/* FUNCTIONS */
void startConnection(void) {

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

}
