## IMPORTS ##
import logging							# Logging: provides a set of convenience functions for simple logging usage
import os 								# OS: this module provides a portable way of using operating system dependent functionality 
import time 							# Time: provides various time-related functions

from threading import Lock, Thread		# Threading: this module constructs higher-level threading interfaces on top of the lower level thread module
from ChunkBucket import ChunkBucket		# ChunkBucket: bucket that stores chunks
from MongoWrapper import MongoWrapper	# MongoWrapper: mongo client wrapper

## CLASS ##
class BucketSupervisor(Thread):

	# __init__
	# --------
	# Initializes an instance of BucketSupervisor
	def __init__(self, user, password):

		# Thread constructor
		Thread.__init__(self)

		# Creates a lock
		self.__lock = Lock()

		# Creates logger
		self.__logger = logging.getLogger("BucketSupervisor")

		# Creates buckets map
		self.__buckets = {}

		# Creates mongo client
		self.__mongo = MongoWrapper(user, password)

	# run
	# --------
	# Run method from thread
	def run(self):
		while True:

			# Locks thread
			self.__lock.acquire()

			self.__logger.info("verifying buckets...")

			# For each bucket stored in buckets
			toRemove = []
			for timestamp, bucket in self.__buckets.items():

				# Get current bucket size and compare to the last one
				currentSize = bucket["chunkBucket"].bucketSize()
				if currentSize != bucket["lastSize"]:
					# If different, update lastSize
					bucket["lastSize"] = currentSize
				else:
					# If equals, save bucket to file
					self.__logger.info("saving bucket {} to local storage".format(timestamp))
					bucket["chunkBucket"].saveBucketAsFile("captures/{}.png".format(timestamp))

					# Stores key to delete in toRemove
					toRemove.append(timestamp)

			self.__logger.info("buckets verified")

			# Removing saved keys
			for timestamp in toRemove:
				self.__buckets.pop(timestamp, None)

			# Unlocks thread
			self.__lock.release()

			# Sleeps for 30 seconds
			time.sleep(30)


	# addPackageToBucket
	# --------
	# Adds package content to a bucket
	#
	# - package {dict}: The package to be stored
	def addPackageToBucket(self, package):

		# Get timestamp to use as key
		key = str(package["timestamp"])

		# Locks thread
		self.__lock.acquire()

		# Verify if a bucket with this key already exists
		if not key in self.__buckets:
			self.__logger.info("creating bucket: {}".format(key))

			# Stores package at mongo
			toStore = package.copy()
			toStore["value"] = "{0}/captures/{1}.png".format(os.getcwd(), package["arrival"])
			toStore.pop("chunk_id", None)
			self.__mongo.storePackage(toStore)

			# Initializes a ChunkBucket
			self.__buckets[key] = {
				"chunkBucket": ChunkBucket(),
				"lastSize": 0
			}

		# Stores package data into bucket
		self.__buckets[key]["chunkBucket"].addToBucket(package["chunk_id"], package["value"])

		# Unlocks thread
		self.__lock.release()
