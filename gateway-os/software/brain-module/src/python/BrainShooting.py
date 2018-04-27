## IMPORTS ##
import logging		# Logging: provides a set of convenience functions for simple logging usage

import numpy as np 	# NumPy: the fundamental package for scientific computing with Python
import cv2 			# OpenCV: usage ranges from interactive art, to mines inspection, stitching maps on the web or through advanced robotics

## CLASS ##
class Shooting:

	## PUBLIC ##

	# __init__
	# --------
	# Initializes an instance of Shooting
	#
	# - cameraId {int}: Camera id to be used on video capture opening
	def __init__(self, cameraId):

		# Creates logger
		self.__logger = logging.getLogger("Shooting({})".format(cameraId))

		# Opens camera
		self.__capture = cv2.VideoCapture(cameraId)

		# Verifies if the camera has been succesfully opened or not
		if(self.__capture.isOpened() == True):

			# Configures camera
			self.__capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('X','2','6','4'))
			self.__capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
			self.__capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
			self.__capture.set(cv2.CAP_PROP_FPS, 30)

			self.__logger.info("video capture succesfully opened")
		else:
			self.__logger.error("couldn't open video capture")

	# captureFrame
	# ------------
	# Captures a frame and returns it
	#
	# returns {numpy.ndarray}: The captured frame
	def captureFrame(self):

		# Verifies if the camera is open
		if(self.__capture.isOpened() == True):

			# Throws away first 30 readings
			for i in range(30):
				self.__capture.read()

			# Capture frame
			ret, frame = self.__capture.read()

			# Verifies if the capture ocurred succesfully
			if(ret == True):
				self.__logger.info("frame succesfully captured")
				return frame
			else:
				self.__logger.error("couldn't capture frame")

		else:
			self.__logger.error("video capture not open")

		return None

	# releaseCamera
	# -------------
	# Releases camera for new usage
	def releaseCamera(self):
		if(self.__capture.isOpened() == True):
			self.__logger.info("video capture succesfully closed")
			self.__capture.release()
