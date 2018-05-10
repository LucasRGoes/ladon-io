## IMPORTS ##
import argparse							# Argparse: the recommended command-line parsing module
import json 							# Json: is a lightweight data interchange format inspired by JavaScript object literal syntax
import logging							# Logging: provides a set of convenience functions for simple logging usage
import os 								# OS: this module provides a portable way of using operating system dependent functionality 
import random							# Random: this module implements pseudo-random number generators for various distributions
import time								# Time: provides various time-related functions

from kafka import KafkaProducer			# KafkaProducer: is a high-level, asynchronous message producer

## FUNCTIONS ##

# argumentParserFactory
# ------------
# Handles ArgumentParser creator
#
# returns {ArgumentParser}: The parser created
def argumentParserFactory():
	# Creates an argument parser
	parser = argparse.ArgumentParser(description="listens to a mqtt broker and repasses the messages to a kafka broker")

	parser.add_argument("-v", "--verbosity", type=int, default=2, choices=[0, 1, 2, 3, 4, 5], help="increase output verbosity")
	parser.add_argument("-m", "--mqtt", type=str, default="localhost", help="the mqtt broker")
	parser.add_argument("-k", "--kafka", type=str, default="ladonio.ddns.net", help="the kafka broker")
	parser.add_argument("--mqtt-topic", type=str, default="#", help="the mqtt topic to subscribe")
	parser.add_argument("--kafka-topic", type=str, default="ladon", help="the kafka topic to publish")
	parser.add_argument("-f", "--frequency", type=int, default=30, help="the frequency to send data")

	return parser

def chunks(l, n):
	# Yield successive n-sized chunks from l
	for i in range(0, len(l), n):
		yield l[i:i + n]

def serializeBytes(obj):
	if isinstance(obj, bytes):
		return {'__class__': 'bytes',
				'__value__': list(obj)}
	raise TypeError(repr(obj) + ' is not a JSON serializable')

## MAIN ##

# Handles arguments
args = argumentParserFactory().parse_args()

# Configuring logging module
logging.basicConfig(format='%(asctime)s [%(levelname)s] [%(name)s]: %(message)s', level=args.verbosity * 10)
logger = logging.getLogger("TonguePipeline")

# Enter loop
while True:
	# Lists files inside captures folder
	listFiles = os.listdir("captures")
	
	# Verify if there is something inside the folder
	if len(listFiles) > 0:
		toSendFileName = listFiles[0]
		logger.info("Sending: {}".format(toSendFileName))

		# Reads file
		toSendFile = open("captures/{}".format(toSendFileName), "rb")
		toSend = toSendFile.read()
		toSendFile.close()		

		# Creates a kafka producer
		producer = KafkaProducer(
					bootstrap_servers=args.kafka,
					value_serializer=lambda v: json.dumps(v, default=serializeBytes).encode('utf-8'),
					retries=5
				   )

		# For each chunk of the image
		try:
			for chunkId, chunk in enumerate(chunks(toSend, 10240)):
				# Sends message
				future = producer.send('ladon', value={'file_name': toSendFileName, 'chunk_id': chunkId, 'chunk': chunk})
				result = future.get(timeout=60)
				producer.flush()
				logger.info("Sent Chunk ID: {}".format(chunkId))

			logger.info("File succesfully sent")
			os.rename("captures/{}".format(toSendFileName), "sent/{}".format(toSendFileName))

		except:
			logger.error("Failed to send")

	else:
		logger.info("Nothing to send")

	# Sleeps for the chosen number of minutes
	time.sleep(args.frequency * 60)
