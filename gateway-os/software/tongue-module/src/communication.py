## IMPORTS ##
import json 						# Json: is a lightweight data interchange format inspired by JavaScript object literal syntax
import logging						# Logging: provides a set of convenience functions for simple logging usage
import os 							# OS: this module provides a portable way of using operating system dependent functionality 

from kafka import KafkaProducer 	# KafkaProducer: is a high-level, asynchronous message producer

## CLASS ##
class KafkaProducerWrapper:

	# __init__
	# --------
	# Initializes an instance of KafkaProducerWrapper
	#
	# - broker {string}: Broker to be used on Kafka connection
	# - topic {string}: Topic to be used on Kafka connection
	def __init__(self, broker, topic):

		# Creates logger
		self.__logger = logging.getLogger("KafkaProducerWrapper")

		# Stores broker and topic
		self.__broker = broker
		self.__topic = topic

		# Creates producer
		self.__producer = KafkaProducer(
							bootstrap_servers = self.__broker,
							value_serializer = lambda v: json.dumps(v, default = KafkaProducerWrapper.__serializeBytes).encode("utf-8"),
							retries = 5
						)

	# sendPackage
	# --------
	# Sends package to Kafka broker
	#
	# - package {dict}: The package to be sent
	#
	# returns {boolean}: If the package was or wasn't sent
	def sendPackage(self, package):

		self.__logger.info("sending package...")

		# Verifies package type
		if package["type"] == "file":

			# Reads file as bytes
			filePath = package["value"]
			fileTemp = open(filePath, "rb")
			fileContent = fileTemp.read()
			fileTemp.close()

			try:

				# For each chunk of the file
				for chunkId, chunk in enumerate(self.__chunks(fileContent, 10240)):

					# Substitutes chunk into value and adds chunkId
					package["value"] = chunk
					package["chunk_id"] = chunkId

					# Sends file in chunks
					future = self.__producer.send(self.__topic, value = package)
					result = future.get(timeout = 60)
					self.__producer.flush()

					self.__logger.info("sent chunk: {}".format(chunkId))

				self.__logger.info("success on sendPackage")

				# Moves file to sent dir
				newFilePath = filePath.replace("captures", "sent")
				os.rename(filePath, newFilePath)

			except:
				self.__logger.info("failure on sendPackage")
				return False

		else:
			future = self.__producer.send(self.__topic, value = package)
			result = future.get(timeout = 60)
			self.__producer.flush()

			if result == True:
				self.__logger.info("success on sendPackage")
			else:
				self.__logger.info("failure on sendPackage")

			return result

	# chunks
	# --------
	# Chunks bytes into n-sized chunks
	#
	# - l {bytes}: The bytes to be chunked
	# - n {ìnt}: N-sized chunks
	#
	# returns {byte array}: The chunks
	def __chunks(self, l, n):
		# Yield successive n-sized chunks from l
		for i in range(0, len(l), n):
			yield l[i:i + n]

	# serializeBytes
	# ------------
	# Helps serializing bytes
	#
	# - obj {bytes}: The bytes to be serialized
	#
	# returns {list}: The serialized list
	def __serializeBytes(obj):
		if isinstance(obj, bytes):
			return {'__class__': 'bytes',
					'__value__': list(obj)}
		raise TypeError(repr(obj) + ' is not a JSON serializable')
