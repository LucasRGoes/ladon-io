## IMPORTS ##
import argparse	# Argparse: the recommended command-line parsing module

# argumentParserFactory
# ------------
# Handles ArgumentParser creator
#
# returns {ArgumentParser}: The parser created
def argumentParserFactory():
	# Creates an argument parser
	parser = argparse.ArgumentParser(description="captures and stores frames with a fixed frequency")

	# COMMON
	parser.add_argument("-v", "--verbosity", type=int, default=2, choices=[0, 1, 2, 3, 4, 5], help="increase output verbosity")

	# MODULE
	parser.add_argument("-c", "--camera", type=int, default=0, help="id of the camera to be used")
	parser.add_argument("-f", "--frequency", type=int, default=60, help="the frequency of capture in minutes")
	parser.add_argument("-a", "--attempts", type=int, default=5, help="the number of attempts on opening the camera")
	parser.add_argument("-i", "--id", type=str, default="nZyLYVd9bBcfeuAm", help="the unique identifier for devices and gateways")
	
	# MQTT
	parser.add_argument("-b", "--broker", type=str, default="localhost", help="the broker to connect to")
	parser.add_argument("-u", "--username", type=str, default="ladon", help="the username to use when connecting to the broker")
	parser.add_argument("-P", "--password", type=str, default="ladon", help="the password to use when connecting to the broker")

	return parser
