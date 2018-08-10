## IMPORTS ##
import argparse	# Argparse: the recommended command-line parsing module

# argumentParserFactory
# ------------
# Handles ArgumentParser creator
#
# returns {ArgumentParser}: The parser created
def argumentParserFactory():
	# Creates an argument parser
	parser = argparse.ArgumentParser(description="listens for MQTT packages to store valid ones on MongoDB")

	# COMMON
	parser.add_argument("-v", "--verbosity", type=int, default=2, choices=[0, 1, 2, 3, 4, 5], help="increase output verbosity")

	# MODULE
	parser.add_argument("--mongo-user", type=str, default="ladon", help="the user for mongo connection")
	parser.add_argument("--mongo-password", type=str, default="ladon", help="the password for mongo connection")

	return parser
