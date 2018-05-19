/*
 * LadonSensor
 * 
 * Sensor reading handler.
 */

/* VARIABLES */
DHTesp dht;
unsigned long lastSensorReading = 0UL;

/* FUNCTIONS */
void startSensor(void) {
	dht.setup(DHTPIN);
}

float readHumidity(void) {
	return dht.getHumidity();
}

float readTemperature(void) {
	return dht.getTemperature();
}

float readSensor(void) {
	return random(15, 35);
}
