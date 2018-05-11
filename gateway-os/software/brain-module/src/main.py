## IMPORTS ##
import cv2								# OpenCV: usage ranges from interactive art, to mines inspection, stitching maps on the web or through advanced robotics
import logging							# Logging: provides a set of convenience functions for simple logging usage
import math								# Math: it provides access to the mathematical functions defined by the C standard
import time								# Time: provides various time-related functions

from utils import argumentParserFactory	# argumentParserFactory: argument parser for the module
from capture import VideoCaptureWrapper	# VideoCaptureWrapper: wrapper for OpenCV VideoCapture

## MAIN ##

# Handles arguments
args = argumentParserFactory().parse_args()

# Configures logging module
logging.basicConfig(format='%(asctime)s [%(levelname)s] [%(name)s]: %(message)s', level=args.verbosity * 10)

while True:

	# Instantiates a VideoCaptureWrapper object for frame capturing
	wrapper = VideoCaptureWrapper(args.camera)

	# Tries opening the VideoCaptureWrapper
	if wrapper.open(args.attempts):

		# Captures frame and closes VideoCaptureWrapper
		frame = wrapper.captureFrame()
		wrapper.close()

		# Saves frame
		fileName = "{}.png".format(math.floor(time.time()))
		cv2.imwrite("captures/{}".format(fileName), frame)

	else:
		# Closes VideoCaptureWrapper
		wrapper.close()

	# Sleeps for the chosen number of minutes
	time.sleep(args.frequency * 60)
