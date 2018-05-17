## IMPORTS ##
import logging	# Logging: provides a set of convenience functions for simple logging usage

## CLASS ##
class MongoWrapper:

	# __init__
	# --------
	# Initializes an instance of MongoWrapper
	def __init__(self):

		# Creates logger
		self.__logger = logging.getLogger("MongoWrapper")
