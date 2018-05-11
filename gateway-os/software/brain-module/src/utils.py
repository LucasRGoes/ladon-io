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
	parser.add_argument("-f", "--frequency", type=int, default=30, help="the frequency of capture in minutes")
	parser.add_argument("-a", "--attempts", type=int, default=5, help="the number of attempts on opening the camera")

	return parser
