# SYNCS Hackathon 2020
# jadaj - Circular

import cv2
import numpy as np

from evaluate_feature import *
from detect_feature import *

# Inputs:
# img (3d array-like): RGB image
# showImg (bool): Flag to show intermediate images for debugging

# Outputs:
# thresh (2d array-like): Binary filtered image
def img_preprocess(img: np.ndarray, showImg: bool):
	# Make image grayscale
	img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

	#####	Resize the image for faster processing and to fit on screen   #####
	height, width = img.shape[:2]
	lim_dim = 550

	# Find which length is longer and scale it appropriately 
	if height > width:
		scale = width/lim_dim
	else:
		scale = height/lim_dim

	img = cv2.resize(img, ( int(width/scale), int(height/scale) ), dst=img, interpolation = cv2.INTER_CUBIC)

	# Create a binary mask
	blur = cv2.GaussianBlur(img, (5,5), 0)
	clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
	contrast = clahe.apply(blur)
	_, thresh = cv2.threshold(contrast, 90, 255, cv2. THRESH_BINARY_INV)
	dilKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))
	thresh = cv2.dilate(thresh, dilKernel, 2)
	eroKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
	thresh = cv2.erode(thresh, eroKernel, 1)
	
	if showImg:
		cv2.imshow('Orig, Blurred, Thresh', cv2.hconcat([img, blur, contrast, thresh]) )
		cv2.waitKey(0)
	return thresh

# Inputs:
# img (2d array-like): Colour photo from app
# feature (string): What feature to detect in the photo

# Outputs:
# null
def backend(img: np.ndarray, feature: str):
	# ret3, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

	thresh = img_preprocess(img, showImg=False)

	# Identify how many possible circles there are based on contour filtering
	_, contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	if feature == 'Circle':
		success, output, circles = detect_circles(thresh, contours, showImg=False)

		if success:
			score,image = evaluate_circle( output, circles[0:2])
			return score,image
			# cv2.imshow('Output of detection', output)
			# cv2.waitKey(0)
		else: 
			print('No', feature, 'found :(')
			return -1000,0

	elif feature == 'parallel':
		success, output, lines = detect_lines(thresh, contours, showImg=False)

		if success:
			# for mask in lines:
			# 	cv2.imshow('Output of detection', mask)
			# 	cv2.waitKey(0)
			score = evaluate_lines( lines, output ) 
			image = "no"
			return score, image
		else: 
			print('No', feature, 'found :(')

	else: 
		print('Unknown feature requested...')
	

	cv2.destroyAllWindows()
	return score, image

if __name__ == '__main__':
	feature = 'circles'
	# feature = 'lines'

	# Load an color image in grayscale
	img = cv2.imread('./sample_circles/12.jpg')
	# img = cv2.imread('./sample_lines/3.jpg')

	# for i in range(1,6):
	# 	img = cv2.imread('./sample_lines/' + str(i) + '.jpg', 0)
	# 	img_preprocess(img, showImg=True)

	backend(img, feature)