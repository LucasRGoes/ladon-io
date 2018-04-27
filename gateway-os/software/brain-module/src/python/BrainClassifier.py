## IMPORTS ##
import logging		# Logging: provides a set of convenience functions for simple logging usage

## CLASS ##
class BrainClassifier:

	# __init__
	# --------
	# Initializes an instance of BrainClassifier
	def __init__(self):

		# Creates logger
		self._logger = logging.getLogger("BrainClassifier".format(cameraId))
		self._logger.info("creation succesfull")