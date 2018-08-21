## IMPORTS ##
import base64							# Base64: Base16, Base32, Base64 data encodings
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
logger = logging.getLogger("FangModule")

logger.info("started")
while True:

	try:

		# Instantiates a VideoCaptureWrapper object for frame capturing
		wrapper = VideoCaptureWrapper(args.camera)

		# Tries opening the VideoCaptureWrapper
		if wrapper.open(args.attempts):

			# Captures frame and closes VideoCaptureWrapper
			frame = wrapper.captureFrame()
			wrapper.close()

			# Stores the timestamp from the capture moment
			timestamp = math.floor(time.time())

			# Gets frame path and saves it
			fullPath = "{0}/captures/{1}.png".format(os.getcwd(), timestamp)
			cv2.imwrite(fullPath, frame)

			# Loads image with base64 encoding
			with open(fullPath, "rb") as imageFile:
				value = base64.b64encode( imageFile.read() ).decode('utf-8')

				# Builds the object to be published
				package = {
					"metrics": {
						"content": 2,		# File
						"feature": 3,		# Photo
						"value": value,
						"device": args.id,
						"timestamp": timestamp
					}
				}

				# Publishes to the MQTT broker
				publish.single(
					"ladon/{0}/feature/{1}".format(args.id, 3),
					json.dumps(package).encode("utf-8"),
					hostname=args.broker,
					auth={
						"username": args.username,
						"password": args.password
					}
				)
				

		else:
			# Closes VideoCaptureWrapper
			wrapper.close()

		#endif: if wrapper.open(args.attempts)

		# Sleeps for the chosen number of minutes
		time.sleep(args.frequency * 60)

	except Error as e:
		logger.error(e)
