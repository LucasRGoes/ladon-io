## IMPORTS ##
import cv2								# OpenCV: usage ranges from interactive art, to mines inspection, stitching maps on the web or through advanced robotics
import json 							# Json: is a lightweight data interchange format inspired by JavaScript object literal syntax
import logging							# Logging: provides a set of convenience functions for simple logging usage
import math								# Math: it provides access to the mathematical functions defined by the C standard
import os 								# OS: this module provides a portable way of using operating system dependent functionality 
import time								# Time: provides various time-related functions
import paho.mqtt.publish as publish		# Paho.Mqtt.Publish: provides a client class which enable applications to publish to an MQTT broker

from utils import argumentParserFactory	# argumentParserFactory: argument parser for the module
from capture import VideoCaptureWrapper	# VideoCaptureWrapper: wrapper for OpenCV VideoCapture

## MAIN ##

# Handles arguments
args = argumentParserFactory().parse_args()

# Configures logging module
logging.basicConfig(format='%(asctime)s [%(levelname)s] [%(name)s]: %(message)s', level=args.verbosity * 10)
logger = logging.getLogger("BrainModule")

logger.info("started")
while True:

	# Instantiates a VideoCaptureWrapper object for frame capturing
	wrapper = VideoCaptureWrapper(args.camera)

	# Tries opening the VideoCaptureWrapper
	if wrapper.open(args.attempts):

		# Captures frame and closes VideoCaptureWrapper
		frame = wrapper.captureFrame()
		wrapper.close()

		# Stores the timestamp from the capture moment
		timestamp = math.floor(time.time())

		# Verify the last name from the captures folder to get the next number
		fileNumber = 0
		fileList = os.listdir("captures")
		if fileList:
			# Directory has images
			sortedList = []
			for fileName in map( lambda f: int(f.replace(".png", "")), fileList ):
				sortedList.append(fileName)
			sortedList.sort()
			fileNumber = sortedList[-1] + 1

		# Gets frame path and saves it
		fullPath = "{0}/captures/{1}.png".format(os.getcwd(), fileNumber)
		cv2.imwrite(fullPath, frame)

		# Builds the object to be published
		package = {
			"type": "file",
			"description": "photo",
			"value": fullPath,
			"timestamp": timestamp
		}

		# Publishes to the MQTT broker
		publish.single("/{0}/{1}".format(args.path, args.id), json.dumps(package).encode("utf-8"), hostname=args.broker)

	else:
		# Closes VideoCaptureWrapper
		wrapper.close()

	# Sleeps for the chosen number of minutes
	time.sleep(args.frequency * 60)
