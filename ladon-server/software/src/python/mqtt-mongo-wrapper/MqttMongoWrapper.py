## IMPORTS ##
import base64							# Base64: Base16, Base32 and Base64 data encodings
import json								# Json: is a lightweight data interchange format inspired by JavaScript object literal syntax
import logging							# Logging: provides a set of convenience functions for simple logging usage
import math								# Math: it provides access to the mathematical functions defined by the C standard
import time								# Time: provides various time-related functions

import paho.mqtt.subscribe as subscribe # Paho.Mqtt.Subscribe: provides a client class which enable applications to subscribe to an MQTT broker

from utils import argumentParserFactory	# argumentParserFactory: argument parser for the module
from MongoWrapper import MongoWrapper	# MongoWrapper: mongo client wrapper

## MAIN ##

# Handles arguments
args = argumentParserFactory().parse_args()

# Configures logging module
logging.basicConfig(format='%(asctime)s [%(levelname)s] [%(name)s]: %(message)s', level=args.verbosity * 10)
logger = logging.getLogger("MqttMongoWrapper")
logger.info("started")

# Creates a MongoWrapper
mongo = MongoWrapper(args.mongo_user, args.mongo_password)

# Creates function to be called on message arrival
def onMessage(client, userdata, message):

	try:
		# Parses message and stores arrival time
		package = json.loads( message.payload.decode('utf-8') )
		package["metrics"]["arrivedOn"] = math.floor(time.time()) * 1000

		# Verifying if a timestamp has been informed
		if "timestamp" in package["metrics"] == True:
			package["metrics"]["sentOn"] = package["metrics"]["timestamp"] * 1000
			package["metrics"].pop("timestamp", None)
		else:
			package["metrics"]["sentOn"] = package["sentOn"]	

		# Using only metrics
		package = package["metrics"]

		# Verifies package type
		if package["content"] == 2: # Photo
			
			# Extracting photo from package
			photo = base64.b64decode( package["value"] )

			# Building photoPath
			photoPath = "var/log/ladon/captures/{}.png".format(package["sentOn"])

			# Storing photo
			file = open(photoPath, "wb")
			file.write(photo)
			file.close()

			# Substituting value at package to the path
			package["value"] = photoPath

		# Storing package at MongoDB
		logger.info("package arrived and being stored: {}".format(package))
		mongo.storePackage(package)

	except Exception as err:
		logger.error("failure at onMessage: {}".format(err))


# Subscribes to all topics and waits for messages
subscribe.callback(onMessage, "#", qos=1, hostname="localhost", auth={'username': 'ladon', 'password': 'ladon'})
