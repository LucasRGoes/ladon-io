## IMPORTS ##
import logging									# Logging: provides a set of convenience functions for simple logging usage
import time										# Time: provides various time-related functions

import numpy as np 								# NumPy: the fundamental package for scientific computing with Python
import cv2 										# OpenCV: usage ranges from interactive art, to mines inspection, stitching maps on the web or through advanced robotics

from sklearn.cluster import MiniBatchKMeans 	# scikit-learn: Simple and efficient tools for data mining and data analysis

## CLASSES ##
class DataExtractor:

	# __init__
	# --------
	# Initializes an instance of PhotoExtractor
	def __init__(self, aMinThresh, aMaxThresh, bMinThresh, bMaxThresh):

		# Creates logger
		self.logger = logging.getLogger("DataExtractor")

		# Stores variables
		self.aMinThresh = aMinThresh
		self.aMaxThresh = aMaxThresh
		self.bMinThresh = bMinThresh
		self.bMaxThresh = bMaxThresh

	# extract
	# --------
	# Starts the extraction on the chosen frame
	def extract(self, frame):
		self.logger.info("started ...")
		start = time.time()

		# Background Extraction
		self.logger.info("starting background extraction ...")
		processedFrame = self.backgroundExtraction(frame)
		self.logger.info("background extraction ended")

		# Sample Detection and Data Extraction
		self.logger.info("starting sample detection ...")
		data = self.sampleDetection(processedFrame)
		self.logger.info("sample detection ended")

		end = time.time()
		self.logger.info("ended, took {}s".format(end - start))

		return data

	def checkMaskResult(self, frame):
	    # Converting frame to Lab and splitting it
	    frameLab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
	    _, a, b = cv2.split(frameLab)

	    # Formatting the components that are being used, a and b, and removing 0s
	    a = a.flatten()
	    b = b.flatten()
	    
	    # Extract min and max from components
	    aMin = np.amin(a)
	    aMax = np.amax(a)
	    bMin = np.amin(b)
	    bMax = np.amax(b)
	    
	    # Verify if the extracted data is ok according to the threshold values
	    if aMin >= self.aMinThresh and aMax <= self.aMaxThresh and bMin >= self.bMinThresh and bMax <= self.bMaxThresh:
	        return False
	    else:
	        return True

	def backgroundExtraction(self, frame):
		# Storing frame dimensions
		width = len(frame[0])
		height = len(frame)

		# Converts frame to L*a*b* color space
		frameLab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

		# Splits frame into L*, a* and b*, but stores only sample b*
		_, _, frameB = cv2.split(frameLab)

		# Reshaping frame b* into a list of pixels
		reshapedFrame = frameB.reshape((frameB.shape[0] * frameB.shape[1], 1))

		# Creating K-Means object
		clt = MiniBatchKMeans(n_clusters = 2, random_state = 5)

		# Calculating K-Means
		self.logger.info("starting k-means clustering ...")
		clt.fit(reshapedFrame)
		self.logger.info("k-means clustering ended")
		labels = clt.labels_

		# Turning K-Means results into a mask
		mask = np.uint8(labels).reshape((height, width))

		# Noise removal
		self.logger.info("starting noise removal ...")
		kernel = np.ones((3,3), np.uint8)
		mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations = 3)
		self.logger.info("noise removal ended")

		# Applying mask to original image
		kMeansFrame = cv2.bitwise_and(frame, frame, mask = mask)

		# Verifying if the mask needs inversal
		if self.checkMaskResult(kMeansFrame) == True:
			# Inverting mask and applying to original image
			mask = 1 - mask
			kMeansFrame = cv2.bitwise_and(frame, frame, mask = mask)

		return kMeansFrame

	def sampleDetection(self, frame):
		# Storing frame dimensions
		width = len(frame[0])
		height = len(frame)

		# Creates gray frame
		grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		# Finding its contours
		self.logger.info("starting contour finding ...")
		im2, contours, hierarchy = cv2.findContours(grayFrame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		self.logger.info("contour finding ended")

		# For each contour, store its area
		contourAreas = []
		for contour in contours:
			contourAreas.append( cv2.contourArea(contour) )
		contourAreas = np.array(contourAreas)

		# Getting the contour with the biggest area to be used as reference
		biggestArea = np.max(contourAreas)
		referenceArea = biggestArea * 0.3 # 30% of the biggest area

		# Getting the indexes of the areas that are higher or equal than the reference
		acceptedAreasIndexes = np.argwhere(contourAreas >= referenceArea)

		# Creates the objects that holds the extracted data
		bMax = []
		aMax = []
		aMin = []
		lMedian = []

		# For each accepted area, create a mask
		referenceBackground = np.zeros([height,width,3],dtype=np.uint8)
		for acceptedIndex in acceptedAreasIndexes:
			acceptedIndex = acceptedIndex[0]

			# Creating contour by drawing it and mask by splitting
			contourMask, _, _ = cv2.split( cv2.drawContours(referenceBackground.copy(), contours, acceptedIndex, (255,255,255), -1) )

			# Applying mask to original frame
			frameData = cv2.bitwise_and(frame, frame, mask = contourMask)

			# Converts frameData to Lab
			frameDataLab = cv2.cvtColor(frameData, cv2.COLOR_BGR2LAB)

			# Splitting frameData into its three components
			data_L, data_a, data_b = cv2.split(frameDataLab)

			# Formatting the components
			data_L = data_L.flatten()
			data_a = data_a.flatten()
			data_b = data_b.flatten()

			# Removing 0s
			data_L = data_L[data_L != 0]
			data_a = data_a[data_a != 0]
			data_b = data_b[data_b != 0]

			# Extracts information and stores it
			bMax.append( np.amax(data_b) )
			aMax.append( np.amax(data_a) )
			aMin.append( np.amin(data_a) )
			lMedian.append( np.median(data_L) )

		# Calculating the average for each extracted color space data
		data = {
			'b_max': np.average(bMax),
			'a_max': np.average(aMax),
			'a_min': np.average(aMin),
			'l_median': np.average(lMedian)
		}

		return data
