/*
 * LadonSensor
 * 
 * Sensor reading handler.
 */

/* VARIABLES */
unsigned long lastSensorReading = 0UL;

/* FUNCTIONS */
void startSensor(void) {
	// Gets a reading from the adc pin to use as a random seed
	randomSeed(analogRead(0));
}

float readSensor(void) {
	return random(15, 35);
}
