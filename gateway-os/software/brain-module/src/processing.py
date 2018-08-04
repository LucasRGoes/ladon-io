## IMPORTS ##
import logging						# Logging: provides a set of convenience functions for simple logging usage
import os 							# OS: this module provides a portable way of using operating system dependent functionality
import time							# Time: provides various time-related functions

import numpy as np 					# NumPy: the fundamental package for scientific computing with Python
import cv2 							# OpenCV: usage ranges from interactive art, to mines inspection, stitching maps on the web or through advanced robotics

from sklearn.cluster import KMeans 	# scikit-learn: Simple and efficient tools for data mining and data analysis
from scipy import stats

## CLASSES ##
class PhotoExtractor:

	# __init__
	# --------
	# Initializes an instance of PhotoExtractor
	def __init__(self):

		# Creates logger
		self.logger = logging.getLogger("PhotoExtractor")

	# extract
	# --------
	# Starts the extraction on the chosen frame
	def extract(self, frame):
		self.logger.info("started ...")
		start = time.time()

		# Background Extraction
		processedFrame = self.backgroundExtraction(frame)

		# Sample Detection and Data Extraction
		RGB, Lab, HSV = self.sampleDetection(processedFrame)

		end = time.time()
		self.logger.info("ended, took {}s".format(end - start))

		return RGB, Lab, HSV

	def backgroundExtraction(self, frame):
		# Storing frame dimensions
		width = len(frame)
		height = len(frame[0])

		# Converts frame to L*a*b* color space
		frameLab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

		# Splits frame into L*, a* and b*, but stores only sample b*
		_, _, frameB = cv2.split(frameLab)

		# Reshaping frame b* into a list of pixels
		reshapedFrame = frameB.reshape((frameB.shape[0] * frameB.shape[1], 1))

		# Creating initial centroids for K-Means
		firstCentroid = frameB[0, width - 1]
		secondCentroid = frameB[690, int(width / 2)]
		init = np.array([[firstCentroid], [secondCentroid]], np.float64)

		# Creating K-Means object
		clt = KMeans(n_clusters = 2, init = init, n_init = 1, random_state = 5, n_jobs = -1)

		# Calculating K-Means
		clt.fit(reshapedFrame)
		labels = clt.labels_

		# Turning K-Means results into a mask
		mask = np.uint8(labels).reshape((height, width))

		# Noise removal
		kernel = np.ones((3,3), np.uint8)
		mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations = 3)

		# Applying mask to original image
		kMeansFrame = cv2.bitwise_and(frame, frame, mask = mask)

		return kMeansFrame

	def sampleDetection(self, frame):
		# Storing frame dimensions
		width = len(frame)
		height = len(frame[0])

		# Creates gray frame
		grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		# Finding its contours
		im2, contours, hierarchy = cv2.findContours(grayFrame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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

		# Creates the objects that hold the extracted data
		RGB_data = {
			R_data: [],
			G_data: [],
			B_data: []
		}
		Lab_data = {
			L_data: [],
			a_data: [],
			b_data: []
		}
		HSV_data = {
			H_data: [],
			S_data: [],
			V_data: []
		}

		# For each accepted area, create a mask
		referenceBackground = np.zeros([height,width,3],dtype=np.uint8)
		for acceptedIndex in acceptedAreasIndexes:
			acceptedIndex = acceptedIndex[0]

			# Creating contour by drawing it and mask by splitting
			contourMask, _, _ = cv2.split( cv2.drawContours(referenceBackground.copy(), contours, acceptedIndex, (255,255,255), -1) )

			# Applying mask to original frame
			frameData = cv2.bitwise_and(frame, frame, mask = contourMask)

			# Converts frameData to RGB, Lab and HSV
			frameDataRGB = cv2.cvtColor(frameData, cv2.COLOR_BGR2RGB)
			frameDataLab = cv2.cvtColor(frameData, cv2.COLOR_BGR2LAB)
			frameDataHSV = cv2.cvtColor(frameData, cv2.COLOR_BGR2HSV)

	        # Splitting frameData into its three components
	        data_R, data_G, data_B = cv2.split(frameDataRGB)
	        data_L, data_a, data_b = cv2.split(frameDataLab)
	        data_H, data_S, data_V = cv2.split(frameDataHSV)

			# Formatting the components
			data_R = data_R.flatten()
			data_G = data_G.flatten()
			data_B = data_B.flatten()

			data_L = data_L.flatten()
			data_a = data_a.flatten()
			data_b = data_b.flatten()

			data_H = data_H.flatten()
			data_S = data_S.flatten()
			data_V = data_V.flatten()

			# Removing 0s
			data_R = data_R[data_R != 0]
			data_G = data_G[data_G != 0]
			data_B = data_B[data_B != 0]

			data_L = data_L[data_L != 0]
			data_a = data_a[data_a != 0]
			data_b = data_b[data_b != 0]

			data_H = data_H[data_H != 0]
			data_S = data_S[data_S != 0]
			data_V = data_V[data_V != 0]

			# Extracts information and stores it
			RGB_data.R_data.append({
				average: np.average(data_R),
				min: np.amin(data_R),
				median: np.median(data_R),
				max: np.amax(data_R),
				mode: stats.mode(data_R).mode[0]
			})
			RGB_data.G_data.append({
				average: np.average(data_G),
				min: np.amin(data_G),
				median: np.median(data_G),
				max: np.amax(data_G),
				mode: stats.mode(data_G).mode[0]
			})
			RGB_data.B_data.append({
				average: np.average(data_B),
				min: np.amin(data_B),
				median: np.median(data_B),
				max: np.amax(data_B),
				mode: stats.mode(data_B).mode[0]
			})

			Lab_data.L_data.append({
				average: np.average(data_L),
				min: np.amin(data_L),
				median: np.median(data_L),
				max: np.amax(data_L),
				mode: stats.mode(data_L).mode[0]
			})
			Lab_data.a_data.append({
				average: np.average(data_a),
				min: np.amin(data_a),
				median: np.median(data_a),
				max: np.amax(data_a),
				mode: stats.mode(data_a).mode[0]
			})
			Lab_data.b_data.append({
				average: np.average(data_b),
				min: np.amin(data_b),
				median: np.median(data_b),
				max: np.amax(data_b),
				mode: stats.mode(data_b).mode[0]
			})

			HSV_data.H_data.append({
				average: np.average(data_H),
				min: np.amin(data_H),
				median: np.median(data_H),
				max: np.amax(data_H),
				mode: stats.mode(data_H).mode[0]
			})
			HSV_data.S_data.append({
				average: np.average(data_S),
				min: np.amin(data_S),
				median: np.median(data_S),
				max: np.amax(data_S),
				mode: stats.mode(data_S).mode[0]
			})
			HSV_data.V_data.append({
				average: np.average(data_V),
				min: np.amin(data_V),
				median: np.median(data_V),
				max: np.amax(data_V),
				mode: stats.mode(data_V).mode[0]
			})

		return RGB_data, Lab_data, HSV_data
