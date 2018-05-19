## IMPORTS ##
import logging					# Logging: provides a set of convenience functions for simple logging usage

from pymongo import MongoClient	# Pymongo: is a Python distribution containing tools for working with MongoDB

## CLASS ##
class MongoWrapper:

	class __MongoWrapper:

		# __init__ (Private Constructor)
		# --------
		# Initializes an instance of MongoWrapper
		def __init__(self):

			# Creates logger
			self.logger = logging.getLogger("MongoWrapper")

			# Creates Mongo client
			self.client = MongoClient("mongodb://{0}:{1}@127.0.0.1".format("ladon", "ladon05121995"))

	# __init__ (Public Constructor)
	# --------
	# Initializes an instance of MongoWrapper
	instance = None
    def __init__(self):
        if not MongoWrapper.instance:
            MongoWrapper.instance = MongoWrapper.__MongoWrapper()

        self.__logger = MongoWrapper.instance.logger
        self.__client = MongoWrapper.instance.client

	# storePackage
	# --------
	# Stores package at mongo database
	#
	# - package {dict}: 
    def storePackage(self, package):

    	# Gets the packages collection
    	database = self.__client["ladon"]
    	packages = database["packages"]

    	# Inserts the package
    	packages.insert_one(package)
    	self.__logger.info("package inserted");