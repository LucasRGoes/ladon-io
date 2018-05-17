## IMPORTS ##
import logging	# Logging: provides a set of convenience functions for simple logging usage

## CLASS ##
class ChunkBucket:

	# __init__
	# --------
	# Initializes an instance of ChunkBucket
	def __init__(self):

		# Creates logger
		self.__logger = logging.getLogger("ChunkBucket")

		# Creates bucket
		self.__bucket = []

	# addToBucket
	# --------
	# Add chunk to bucket
	#
	# - chunkId {int}: The chunk id
	# - chunk {bytes}: The chunk content
	def addToBucket(self, chunkId, chunk):
		self.__bucket.insert(chunkId, chunk)

	# saveBucketAsFile
	# --------
	# Saves bucket content as a file
	#
	# - fileName {string}: The file name to be saved
	#
	# returns {boolean}: The file was or wasn't saved
	def saveBucketAsFile(self, fileName):

		# Verifies if the file is ok
		if self.verifyBucket == False:
			return False

		# Creates file
		fileTemp = open(fileName, "wb")

		# Writes to file
		for chunk in self.__bucket:
			fileTemp.write(chunk)

		# Closes file
		fileTemp.close()

		return True

	# verifyBucket
	# --------
	# Verifies bucket content
	#
	# returns {boolean}: The file is or isn't ok
	def verifyBucket(self):

		self.__logger.info("verifying bucket...")
		# For each chunk on bucket
		for chunk in self.__bucket:
			if chunk is None:
				self.__logger.error("failure on verifyBucket")
				return False

		self.__logger.info("success on verifyBucket")
		return True

	# bucketSize
	# --------
	# Get bucket size
	#
	# returns {int}: The bucket size
	def bucketSize(self):
		return len(self.__bucket)
