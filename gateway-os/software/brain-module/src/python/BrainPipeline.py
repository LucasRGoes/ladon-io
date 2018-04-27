## IMPORTS ##
import argparse							# Argparse: the recommended command-line parsing module
import datetime							# Datetime: supplies classes for manipulating dates and times in both simple and complex ways
import logging							# Logging: provides a set of convenience functions for simple logging usage
import os 								# OS: this module provides a portable way of using operating system dependent functionality 
import pathlib							# Pathlib: this module offers classes representing filesystem paths with semantics appropriate for different operating systems
import time								# Time: provides various time-related functions

import cv2								# OpenCV: usage ranges from interactive art, to mines inspection, stitching maps on the web or through advanced robotics

from BrainShooting import Shooting		# BrainShooting: responsible for camera capturing
from BrainProcessing import Processing	# BrainProcessing: responsible for processing frames

## FUNCTIONS ##

# argumentParserFactory
# ------------
# Handles ArgumentParser creator
#
# returns {ArgumentParser}: The parser created
def argumentParserFactory():
	# Creates an argument parser
	parser = argparse.ArgumentParser(description="captures and stores frames with a fixed frequency")

	parser.add_argument("-v", "--verbosity", type=int, default=2, choices=[0, 1, 2, 3, 4, 5], help="increase output verbosity")
	parser.add_argument("-c", "--camera", type=int, default=0, help="id of the camera to be used")
	parser.add_argument("-f", "--frequency", type=int, default=30, help="the frequency to capture frames in minutes")

	return parser

# createDailyDirectory
# ------------
# Creates directories based on date
#
# returns {string}: The name of the directory created or that already existed
def createDailyDirectory():
	# Get date
	date = datetime.datetime.now()
	directoryName = "{}/captures/{}_{}_{}".format(os.path.expanduser("~"), date.day, date.month, date.year)

	# Creates directory if it doesn't exist
	pathlib.Path(directoryName).mkdir(parents=True, exist_ok=True) 
	return directoryName

## MAIN ##

# Handles arguments
args = argumentParserFactory().parse_args()

# Configuring logging module
logging.basicConfig(format='%(asctime)s [%(levelname)s] [%(name)s]: %(message)s', level=args.verbosity * 10)

# Enter loop
while True:
	# Verify directory
	directoryName = createDailyDirectory()

	# Instantiates a shooting class for frame capturing
	capture = Shooting(args.camera)

	# Captures frame and releases shooting class
	frame = capture.captureFrame()
	capture.releaseCamera()

	# Saves frame
	fileName = "{}.png".format(time.time())
	cv2.imwrite("{}/{}".format(directoryName, fileName), frame)

	# Sleeps for the chosen number of minutes
	time.sleep(args.frequency * 60)