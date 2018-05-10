## IMPORTS ##
import argparse							# Argparse: the recommended command-line parsing module
import json 							# Json: is a lightweight data interchange format inspired by JavaScript object literal syntax
import logging							# Logging: provides a set of convenience functions for simple logging usage
import random							# Random: this module implements pseudo-random number generators for various distributions

from kafka import KafkaProducer			# KafkaProducer: is a high-level, asynchronous message producer

## ladon05121995

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

## TESTING ##

# Opens image
photoFile = open("/home/lucas/Downloads/Teste.png", "rb")
fileContent = photoFile.read()
photoFile.close()

# Creates a producer
producer = KafkaProducer(
			bootstrap_servers=args.kafka,
			value_serializer=lambda v: json.dumps(v, default=serializeBytes).encode('utf-8'),
			retries=5
		   )

# Creates a hash for this photo
photoHash = random.getrandbits(128)

# For each chunk of the image
for chunkId, chunk in enumerate(chunks(fileContent, 10240)):
	# Sends message
	future = producer.send('ladon', value={'hash': photoHash, 'chunk_id': chunkId, 'chunk': chunk})
	result = future.get(timeout=60)
	producer.flush()

	print("Sent Chunk ID: {}".format(chunkId))