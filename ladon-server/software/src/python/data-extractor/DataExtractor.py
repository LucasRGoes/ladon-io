## IMPORTS ##
import base64							# Base64: Base16, Base32, Base64 data encodings
import cv2								# OpenCV: usage ranges from interactive art, to mines inspection, stitching maps on the web or through advanced robotics
import json 							# Json: is a lightweight data interchange format inspired by JavaScript object literal syntax
import sys 								# Sys: system-specific parameters and functions
import numpy as np 						# Numpy: fundamental package for scientific computing with Python

from processing import DataExtractor	# DataExtractor: LadonIO's data extraction pipeline from images

## MAIN ##

# Variables
aMinThresh = 90
aMaxThresh = 175
bMinThresh = 115
bMaxThresh = 205

# Stores image
imageUrl = sys.argv[1]

# Reading image
image = cv2.imread(imageUrl)

# Instantiates a DataExtractor object for image processing
dataExtractor = DataExtractor(aMinThresh, aMaxThresh, bMinThresh, bMaxThresh)

# Runs data extractor pipeline on the image
data = dataExtractor.extract(image)

# Encoding draw image
convertedImage = cv2.imencode('.jpg', data['draw_image'])[1].tostring()
data['draw_image'] = base64.b64encode( convertedImage ).decode('utf-8')

# Printing answer
print( json.dumps(data) )
sys.stdout.flush()

sys.exit()
