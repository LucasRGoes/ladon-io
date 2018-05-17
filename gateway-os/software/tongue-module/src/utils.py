## IMPORTS ##
import argparse	# Argparse: the recommended command-line parsing module
import math		# Math: it provides access to the mathematical functions defined by the C standard
import time		# Time: provides various time-related functions

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
	parser.add_argument("--mqtt-topic", type=str, default="#", help="the mqtt topic to subscribe")
	
	return parser

## CLASS ##
class LadonPackage:

	# __init__
	# --------
	# Initializes an instance of LadonPackage
	#
	# - package {dict}: Package to be used on LadonPackage creation
	def __init__(self, package):

		# Verifying parameters
		if package["path"] and type(package["path"]) is str:
			self.path = package["path"]
		else:
			raise ValueError("path")

		if package["id"] and type(package["id"]) is str:
			self.id = package["id"]
		else:
			raise ValueError("id")

		if package["type"] and type(package["type"]) is str:
			self.type = package["type"]
		else:
			raise ValueError("type")

		if package["description"] and type(package["description"]) is str:
			self.description = package["description"]
		else:
			raise ValueError("description")

		if package["value"]:
			self.value = package["value"]
		else:
			raise ValueError("value")

		if package["timestamp"]:
			self.timestamp = package["timestamp"]
		else:
			self.timestamp = math.floor(time.time())

	# __str__
	# --------
	# Prints LadonPackage as a string
	#
	# returns {string}: The printed package
	def __str__(self):
		return "LadonPackage(/{0}/{1}): Type: {2}, Description: {3}, Value: {4}, Timestamp: {5}".format(self.path, self.id, self.type, self.description, self.value, self.timestamp)

	# getPackage
	# --------
	# Returns the package as an object
	#
	# returns {dict}: The package
	def getPackage(self):
		return {
			"path": self.path,
			"id": self.id,
			"type": self.type,
			"description": self.description,
			"value": self.value,
			"timestamp": self.timestamp
		}
