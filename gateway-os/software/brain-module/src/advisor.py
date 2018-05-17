## IMPORTS ##
import logging		# Logging: provides a set of convenience functions for simple logging usage

## CLASS ##
class BrainAdvisor:

	# __init__
	# --------
	# Initializes an instance of BrainAdvisor
	def __init__(self):

		# Creates logger
		self._logger = logging.getLogger("BrainAdvisor".format(cameraId))
		self._logger.info("creation succesfull")