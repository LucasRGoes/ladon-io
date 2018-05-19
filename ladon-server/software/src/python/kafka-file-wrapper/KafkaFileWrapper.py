## IMPORTS ##
import json										# Json: is a lightweight data interchange format inspired by JavaScript object literal syntax
import logging									# Logging: provides a set of convenience functions for simple logging usage
import math										# Math: it provides access to the mathematical functions defined by the C standard
import time										# Time: provides various time-related functions

from kafka import KafkaConsumer					# KafkaConsumer: is a high-level, asynchronous message consumer
from BucketSupervisor import BucketSupervisor	# BucketSupervisor: saves buckets by supervising their sizes
from MongoWrapper import MongoWrapper			# MongoWrapper: mongo client wrapper

## MAIN ##

# Configures logging module
logging.basicConfig(format='%(asctime)s [%(levelname)s] [%(name)s]: %(message)s', level=20)
logger = logging.getLogger("KafkaFileWrapper")
logger.info("started")

# Creates a BucketSupervisor and start it
supervisor = BucketSupervisor()
supervisor.start()

# Creates a MongoWrapper
mongo = MongoWrapper()

# Receives message from Kafka broker
while(True):

	# Creates a Kafka consumer
	consumer = KafkaConsumer(
					'ladon',
					bootstrap_servers = "localhost",
					value_deserializer = lambda v: json.loads(v.decode("utf-8"))
				)

	try:

		for msg in consumer:

			# Get package and stores arrival moment
			package = msg.value
			package["arrival"] = math.floor(time.time())

			# Verify package type
			if package["type"] == "file":
				# Deserializes value
				package["value"] = bytearray(package["value"]["__value__"])

				# Adds package to bucket
				supervisor.addPackageToBucket(package)

			else:
				logger.info("package arrived: {}".format(package))
				mongo.storePackage(package)

	except Exception as err:
		logger.error("failure at KafkaConsumer: {}".format(err))

	# Closes consumer
	consumer.close()