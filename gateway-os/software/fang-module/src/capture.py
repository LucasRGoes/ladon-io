## IMPORTS ##
import logging		# Logging: provides a set of convenience functions for simple logging usage
import time			# Time: provides various time-related functions

import numpy as np	# NumPy: the fundamental package for scientific computing with Python
import cv2 			# OpenCV: usage ranges from interactive art, to mines inspection, stitching maps on the web or through advanced robotics

## CLASS ##
class VideoCaptureWrapper:

	# __init__
	# --------
	# Initializes an instance of VideoCaptureWrapper
	#
	# - cameraId {int}: Camera id to be used on VideoCapture opening
	def __init__(self, cameraId):

		# Creates logger
		self.__logger = logging.getLogger("VideoCaptureWrapper({})".format(cameraId))

		# Stores cameraId
		self.__cameraId = cameraId

	# open
	# --------
	# Opens VideoCapture
	#
	# - numberTries {int}: Number of tries on opening the VideoCapture
	#
	# returns {boolean}: VideoCapture opened or not
	def open(self, numberTries):

		# Tries opening VideoCapture numberTries max
		for i in range(0, numberTries):

			# Tries to open VideoCapture
			self.__capture = cv2.VideoCapture(self.__cameraId)

			# Verifies if VideoCapture has been succesfully opened or not
			if(self.isOpen() == True):

				# Configures VideoCapture
				self.__capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('X','2','6','4'))
				self.__capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
				self.__capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
				self.__capture.set(cv2.CAP_PROP_FPS, 30)

				self.__logger.info("success on open")
				return True

			else:

				# Sleeps 500ms for next try
				self.__logger.error("failure on open ({})".format(i + 1))
				time.sleep(0.5)

		return False

	# close
	# -------------
	# Releases VideoCapture
	#
	# returns {boolean}: VideoCapture closed or not
	def close(self):
		if(self.isOpen() == True):
			self.__capture.release()
			self.__logger.info("success on close")
			return True
		else:
			self.__logger.info("is already closed")
			return False
			
	# isOpen
	# ------------
	# Verifies if the VideoCapture is open
	#
	# returns {boolean}: VideoCapture open or not
	def isOpen(self):
		if self.__capture is None:
			return False
		else:
			return self.__capture.isOpened()

	# captureFrame
	# ------------
	# Captures a frame
	#
	# returns {numpy.ndarray}: The captured frame
	def captureFrame(self):

		# Verifies if VideoCapture is open
		if(self.isOpen() == True):

			# Throws away first 30 readings
			for i in range(30):
				self.__capture.read()

			# Capture frame
			ret, frame = self.__capture.read()

			# Verifies if the capture ocurred succesfully
			if(ret == True):
				self.__logger.info("success on captureFrame")
				return frame
			else:
				self.__logger.error("failure on captureFrame, error on capture")

		else:
			self.__logger.error("failure on captureFrame, not open")

		return None
