## IMPORTS ##
import logging		# Logging: provides a set of convenience functions for simple logging usage
import os 			# OS: this module provides a portable way of using operating system dependent functionality
import time			# Time: provides various time-related functions

import numpy as np 	# NumPy: the fundamental package for scientific computing with Python
import cv2 			# OpenCV: usage ranges from interactive art, to mines inspection, stitching maps on the web or through advanced robotics

## CLASS ##
class Processing:

	# __init__
	# --------
	# Initializes an instance of Processing
	#
	# - frame {numpy.ndarray}: The frame to be processed
	def __init__(self):

		# Creates logger
		self.logger = logging.getLogger("Processing")

		# Creates background subtractor
		self.createBackgroundSubtractor()

	# createBackgroundSubtractor
	# --------
	# Creates a background subtractor with the images to be used as background reference
	def createBackgroundSubtractor(self):

		# Gets the list of images
		backgroundsList = os.listdir("backgrounds")

		# Creates MOG2 background subtraction object
		self.backgroundSubtractor = cv2.createBackgroundSubtractorMOG2(history=len(backgroundsList), varThreshold=16, detectShadows=True);

		# Applies all reference images to MOG2
		for background in backgroundsList:
			backgroundImage = cv2.imread('backgrounds/{}'.format(background))
			self.backgroundSubtractor.apply(backgroundImage)

	# process
	# --------
	# Starts the processing on the chosen frame
	def process(self, frame):

		self.logger.info("started ...")
		start = time.time()

		# Perform background subtraction
		#frame = self.subtractBackground(frame)

		# Convert the frame to a color invariate space
		c1c2c3 = self.convertToC1C2C3(frame)

		# Creates a mask from c1c2c3 color space
		mask = self.generateMask(c1c2c3)

		# Applies threshold to frame
		frame = cv2.bitwise_or(frame, frame, mask = mask)

		# Calculates median for each color space
		b, g, r = cv2.split(frame)
		bM = np.ma.median(np.ma.masked_where(b == 0, b))
		gM = np.ma.median(np.ma.masked_where(g == 0, g))
		rM = np.ma.median(np.ma.masked_where(r == 0, r))

		end = time.time()
		self.logger.info("ended, took {}s".format(end - start))

		return frame, bM, gM, rM

	def subtractBackground(self, frame):

		# Creates mask from background subtractor applies morphological transformations
		fgmask = self.backgroundSubtractor.apply(frame)

		kernel = np.ones((5,5), np.uint8)
		fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel, iterations = 2)

		# Applies mask to original image
		return cv2.bitwise_or(frame, frame, mask = fgmask)

	def convertToC1C2C3(self, frame):

		# Change image type to float32
		frameAsFloat = frame.astype(np.float32) + 0.001 # To avoid division by 0

		# Convert to c1c2c3 color space
		# (c1 = arctan(R / max(G, B)))
		# (c2 = arctan(G / max(R, B)))
		# (c3 = arctan(B / max(R, G)))
		c1c2c3 = np.arctan(frameAsFloat/np.dstack((cv2.max(frameAsFloat[...,1], frameAsFloat[...,2]), cv2.max(frameAsFloat[...,0], frameAsFloat[...,2]), cv2.max(frameAsFloat[...,0], frameAsFloat[...,1]))))

		return c1c2c3

	def generateMask(self, c1c2c3):

		# Spliting color spaces
		c1, c2, c3 = cv2.split(c1c2c3)

		# Applying median blur to c1, c2 and c3
		c1 = cv2.medianBlur(c1, 5)
		c2 = cv2.medianBlur(c2, 5)
		c3 = cv2.medianBlur(c3, 5)

		# Generates threshold for frames c1, c2 and c3
		ret, c1Mask = cv2.threshold(c1, 0.62, 255, cv2.THRESH_BINARY_INV)
		ret, c2Mask = cv2.threshold(c2, 0.67, 255, cv2.THRESH_BINARY)
		ret, c3Mask = cv2.threshold(c3, 0.65, 255, cv2.THRESH_BINARY)

		# for value in np.arange(0.4, 0.81, 0.01):
		# 	ret, test = cv2.threshold(c2, value, 255, cv2.THRESH_BINARY)
		# 	test = np.uint8(test)

		# 	cv2.namedWindow("{}".format(value), cv2.WINDOW_NORMAL)
		# 	cv2.resizeWindow("{}".format(value), 683, 384)
		# 	cv2.imshow("{}".format(value), cv2.bitwise_or(self.__frame, self.__frame, mask = test))

		# 	cv2.waitKey(0)
		# 	cv2.destroyAllWindows()

		# Converts masks
		c1Mask = np.uint8(c1Mask)
		c2Mask = np.uint8(c2Mask)
		c3Mask = np.uint8(c3Mask)

		# Creates the final mask to be used
		mask = cv2.bitwise_and(c1Mask, c1Mask, mask = c2Mask)
		mask = cv2.bitwise_and(mask, mask, mask = c3Mask)

		# Noise removal
		kernel = np.ones((7,7), np.uint8)
		mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations = 2)
		mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations = 3)

		return mask
