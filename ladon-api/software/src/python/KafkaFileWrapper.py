## IMPORTS ##
import json										# Json: is a lightweight data interchange format inspired by JavaScript object literal syntax
import logging									# Logging: provides a set of convenience functions for simple logging usage

from kafka import KafkaConsumer					# KafkaConsumer: is a high-level, asynchronous message consumer
from BucketSupervisor import BucketSupervisor	# BucketSupervisor: saves buckets by supervising their sizes

## MAIN ##

# Configures logging module
logging.basicConfig(format='%(asctime)s [%(levelname)s] [%(name)s]: %(message)s', level=20)
logger = logging.getLogger("KafkaFileWrapper")
logger.info("started")

# Creates a BucketSupervisor and start it
supervisor = BucketSupervisor()
supervisor.start()

# Creates a Kafka consumer
consumer = KafkaConsumer(
				'ladon',
				bootstrap_servers = "orcinus",
				value_deserializer = lambda v: json.loads(v.decode("utf-8"))
			)

# Receives message from Kafka broker
for msg in consumer:

	# Get package
	package = msg.value

	# Verify package type
	if package["type"] == "file":
		# Updates value
		package["value"] = bytearray(package["value"]["__value__"])

		# Adds package to bucket
		supervisor.addPackageToBucket(package)

	else:
		logger.info("message arrived: {}".format(package))
