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
	parser.add_argument("-k", "--kafka", type=str, default="ladonio.ddns.net", help="the kafka broker")
	parser.add_argument("-b", "--broker", type=str, default="localhost", help="the mqtt broker")
	parser.add_argument("--kafka-topic", type=str, default="ladon", help="the kafka topic to publish")
	parser.add_argument("--mqtt-topic", type=str, default="/kafka", help="the mqtt topic to subscribe")
	
	return parser
