## IMPORTS ##
import json 									# Json: is a lightweight data interchange format inspired by JavaScript object literal syntax
import logging									# Logging: provides a set of convenience functions for simple logging usage
import paho.mqtt.subscribe as subscribe			# Paho.Mqtt.Subscribe: provides a client class which enable applications to subscribe to an MQTT broker

from utils import argumentParserFactory			# argumentParserFactory: argument parser for the module
from utils import LadonPackage					# LadonPackage: class representing a package to be sent over Kafka
from communication import KafkaProducerWrapper	# KafkaProducerWrapper: wrapper for Kafka Producer

## MAIN ##

# Handles arguments
args = argumentParserFactory().parse_args()

# Configures logging module
logging.basicConfig(format='%(asctime)s [%(levelname)s] [%(name)s]: %(message)s', level=args.verbosity * 10)
logger = logging.getLogger("TongueModule")
logger.info("started")

# Instantiates a KafkaProducerWrapper object
wrapper = KafkaProducerWrapper(args.kafka, args.kafka_topic)

# Creates a callback for MQTT subscription
def onMessage(client, userdata, message):
	
	try:
		# Deserializes message
		package = json.loads(message.payload.decode("utf-8"))

		# Adds topic parameters to message
		_, path, id = message.topic.split("/")
		package["path"] = path
		package["id"] = id

		# Creates the package
		ladonPackage = LadonPackage(package)
		logger.info("valid package arrived: {}".format(ladonPackage))

		# Sends package
		wrapper.sendPackage(ladonPackage.getPackage())

	except Exception as e:
		logger.warn("failure on onMessage: {}".format(e))

# Subscribes to MQTT broker
subscribe.callback(onMessage, args.mqtt_topic, hostname=args.broker)
