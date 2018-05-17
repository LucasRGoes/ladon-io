## IMPORTS ##
import logging		# Logging: provides a set of convenience functions for simple logging usage

import numpy as np 	# NumPy: the fundamental package for scientific computing with Python
import cv2 			# OpenCV: usage ranges from interactive art, to mines inspection, stitching maps on the web or through advanced robotics

## CLASS ##
class Processing:

	# __init__
	# --------
	# Initializes an instance of Processing
	#
	# - frame {numpy.ndarray}: The frame to be processed
	def __init__(self, frame):

		# Creates logger
		self.__logger = logging.getLogger("Processing")

		# Stores frame
		self.__frame = frame

	# start
	# --------
	# Starts the processing
	def start(self):

		# Convert the frame to a color invariate space
		c1, c2, c3 = self.convertToC1C2C3()

		# Apply thresholding
		thresholded = self.generateAndApplyMask(c1, 0.61)

		# Gets L*a*b* color space (Color independent device)
		lab = cv2.cvtColor(thresholded, cv2.COLOR_BGR2Lab)

		return lab

	def convertToC1C2C3(self):

		# Change image type to float32
		frameAsFloat = self.__frame.astype(np.float32) + 0.001 # To avoid division by 0

		# Convert to c1c2c3 color space
		# (c1 = arctan(R / max(G, B)))
		# (c2 = arctan(G / max(R, B)))
		# (c3 = arctan(B / max(R, G)))
		c1c2c3 = np.arctan(frameAsFloat/np.dstack((cv2.max(frameAsFloat[...,1], frameAsFloat[...,2]), cv2.max(frameAsFloat[...,0], frameAsFloat[...,2]), cv2.max(frameAsFloat[...,0], frameAsFloat[...,1]))))

		return cv2.split(c1c2c3)

	def generateAndApplyMask(self, toThreshold, thresholdValue):

		# Applies threshold
		ret, mask = cv2.threshold(toThreshold, thresholdValue, 255, cv2.THRESH_BINARY_INV)

		# Converts mask
		mask = np.uint8(mask)

		# Applies mask
		return cv2.bitwise_or(self.__frame, self.__frame, mask = mask)
