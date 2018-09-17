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
	parser.add_argument("-f", "--frequency", type=int, default=60, help="the frequency of looking for images to process in minutes")
	parser.add_argument("-i", "--id", type=str, default="nZyLYVd9bBcfeuAm", help="the unique identifier for devices and gateways")

	# MQTT
	parser.add_argument("-b", "--broker", type=str, default="localhost", help="the broker to connect to")
	parser.add_argument("-u", "--username", type=str, default="ladon", help="the username to use when connecting to the broker")
	parser.add_argument("-P", "--password", type=str, default="ladon", help="the password to use when connecting to the broker")

	# DATA PROCESSING PIPELINE
	parser.add_argument("--a-min-thresh", type=int, default=90, help="the a* minimum threshold from L*a*b* color space to use on the image processing pipeline")
	parser.add_argument("--a-max-thresh", type=int, default=175, help="the a* maximum threshold from L*a*b* color space to use on the image processing pipeline")
	parser.add_argument("--b-min-thresh", type=int, default=115, help="the b* minimum threshold from L*a*b* color space to use on the image processing pipeline")
	parser.add_argument("--b-max-thresh", type=int, default=205, help="the b* maximum threshold from L*a*b* color space to use on the image processing pipeline")

	return parser
