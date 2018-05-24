## IMPORTS ##
import logging						# Logging: provides a set of convenience functions for simple logging usage
import os 							# OS: this module provides a portable way of using operating system dependent functionality

import numpy as np 					# NumPy: the fundamental package for scientific computing with Python
import cv2 							# OpenCV: usage ranges from interactive art, to mines inspection, stitching maps on the web or through advanced robotics

from processing import Processing	# Processing

# Configures logging module
logging.basicConfig(format='%(asctime)s [%(levelname)s] [%(name)s]: %(message)s', level=20)

proc = Processing()

# img1 = cv2.imread('captures/1526757539.png')
# img2 = cv2.imread('captures/1526841936.png')
# img3 = cv2.imread('captures/1527129313.png')

# imageProcessed, b, g, r = proc.process(img1)
# cv2.namedWindow("img1", cv2.WINDOW_NORMAL)
# cv2.resizeWindow("img1", 683, 384)
# cv2.imshow("img1", imageProcessed)

# imageProcessed, b, g, r = proc.process(img2)
# cv2.namedWindow("img2", cv2.WINDOW_NORMAL)
# cv2.resizeWindow("img2", 683, 384)
# cv2.imshow("img2", imageProcessed)

# imageProcessed, b, g, r = proc.process(img3)
# cv2.namedWindow("img3", cv2.WINDOW_NORMAL)
# cv2.resizeWindow("img3", 683, 384)
# cv2.imshow("img3", imageProcessed)

# cv2.waitKey(0)
# cv2.destroyAllWindows()

# Gets captures list and sorts it
fileList = os.listdir("captures")
sortedList = []
for fileName in map( lambda f: int(f.replace(".png", "")), fileList ):
	sortedList.append(fileName)
sortedList.sort()

# Stores size of sorted list
listLength = len(sortedList)

# Creates the image to show the color change
colorChange = np.zeros( (listLength, listLength, 3), np.uint8 )

# For each file at captures list
for index, file in enumerate(sortedList):

	print("Image: {}.png".format(file))
	img = cv2.imread('captures/{}.png'.format(file))

	# Processes image and draws a line with its median colors
	frame, b, g, r = proc.process(img)
	print("B:{0} G:{1} R:{2}".format(b, g, r))
	cv2.line( colorChange, (index, 0), (index, listLength - 1), (b, g, r) )

cv2.namedWindow("colorChange", cv2.WINDOW_NORMAL)
cv2.resizeWindow("colorChange", listLength, listLength)
cv2.imshow("colorChange", colorChange)

cv2.waitKey(0)
cv2.destroyAllWindows()
