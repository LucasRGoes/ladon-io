## IMPORTS ##
import cv2									# OpenCV: usage ranges from interactive art, to mines inspection, stitching maps on the web or through advanced robotics
import json 								# Json: is a lightweight data interchange format inspired by JavaScript object literal syntax
import logging								# Logging: provides a set of convenience functions for simple logging usage
import math									# Math: it provides access to the mathematical functions defined by the C standard
import os 									# OS: this module provides a portable way of using operating system dependent functionality 
import time									# Time: provides various time-related functions
import paho.mqtt.publish as publish			# Paho.Mqtt.Publish: provides a client class which enable applications to publish to an MQTT broker

from utils import argumentParserFactory	# argumentParserFactory: argument parser for the module
from processing import DataExtractor	# DataExtractor: LadonIO's data extraction pipeline from images

## MAIN ##

# Handles arguments
args = argumentParserFactory().parse_args()

# Configures logging module
logging.basicConfig(format='%(asctime)s [%(levelname)s] [%(name)s]: %(message)s', level=args.verbosity * 10)
logger = logging.getLogger("BrainModule")

logger.info("started")
while True:
	
	try:

		# Instantiates a DataExtractor object for image processing
		dataExtractor = DataExtractor(args.a_min_thresh, args.a_max_thresh, args.b_min_thresh, args.b_max_thresh)

		# Searches for a new image to extract data
		listImages = os.listdir('./captures')

		# Verifying if there are images to process
		if len(listImages) == 0:
			logger.info('no image to process')

			# Sleeps for the chosen number of minutes
			time.sleep(args.frequency * 60)
		else:
			# Stores timestamp from image name
			imageName = listImages[0]
			timestamp = int( imageName.replace('.png', '') )

			logger.info('new image to process: {}'.format(imageName))

			# Loads image
			image = cv2.imread( './captures/{}'.format(imageName) )

			# Runs data extractor pipeline on the image
			data = dataExtractor.extract(image)

			# Building objects for each data extracted to be published
			messages = []
			messages.append({
				"topic": "ladon/{0}/feature/{1}".format(args.id, 4),
				"payload": json.dumps({
					"metrics": {
						"content": 1,		# Number
						"feature": 4,		# b* Max
						"value": data['b_max'],
						"device": args.id,
						"timestamp": timestamp
					}
				}).encode("utf-8"),
				"qos": 1
			})
			messages.append({
				"topic": "ladon/{0}/feature/{1}".format(args.id, 5),
				"payload": json.dumps({
					"metrics": {
						"content": 1,		# Number
						"feature": 5,		# a* Max
						"value": data['a_max'],
						"device": args.id,
						"timestamp": timestamp
					}
				}).encode("utf-8"),
				"qos": 1
			})
			messages.append({
				"topic": "ladon/{0}/feature/{1}".format(args.id, 6),
				"payload": json.dumps({
					"metrics": {
						"content": 1,		# Number
						"feature": 6,		# a* Min
						"value": data['a_min'],
						"device": args.id,
						"timestamp": timestamp
					}
				}).encode("utf-8"),
				"qos": 1
			})
			messages.append({
				"topic": "ladon/{0}/feature/{1}".format(args.id, 7),
				"payload": json.dumps({
					"metrics": {
						"content": 1,		# Number
						"feature": 7,		# L* Median
						"value": data['l_median'],
						"device": args.id,
						"timestamp": timestamp
					}
				}).encode("utf-8"),
				"qos": 1
			})

			# Publishes to the MQTT broker
			publishedSuccesfully = False
			while publishedSuccesfully == False:

				try:
					publish.multiple(messages, hostname=args.broker, auth={
						"username": args.username,
						"password": args.password
					})

					publishedSuccesfully = True
				except Exception as e:
					logger.error(e)

					# Sleeps for 5 seconds until next attempt
					logger.warn('retrying in 5 seconds ...')
					time.sleep(5)

			#endwhile: while publishedSuccesfully == False

			# Moves image to another directory
			os.rename('./captures/{}'.format(listImages[0]), './processed/{}'.format(listImages[0]))

			# Sleeps for 10 seconds
			time.sleep(10)

	except Exception as e:
		logger.error(e)

		# Sleeps for one minute before trying again
		logger.warn('retrying in 60 seconds ...')
		time.sleep(60)
