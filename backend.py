import cv2
import numpy as np

from evaluate_feature import *
from detect_feature import *

def img_preprocess(img: np.ndarray, showImg: bool):
	#####	Resize the image for faster processing and to fit on screen   #####
	height, width = img.shape[:2]
	lim_dim = 550

	# Find which length is longer and scale it appropriately 
	if height > width:
		scale = width/lim_dim
	else:
		scale = height/lim_dim

	img = cv2.resize(img, ( int(width/scale), int(height/scale) ), dst=img, interpolation = cv2.INTER_CUBIC)

	# Create a binary mask - TODO: Apply increasing contrast methods to this. 
	blur = cv2.GaussianBlur(img, (5,5), 0)
	_, thresh = cv2.threshold(blur, 80, 255, cv2. THRESH_BINARY_INV)
	dilKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))
	thresh = cv2.dilate(thresh, dilKernel, 2)
	eroKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
	thresh = cv2.erode(thresh, eroKernel, 1)
	
	if showImg:
		cv2.imshow('Orig, Blurred, Thresh', cv2.hconcat([img, blur, thresh]) )
		cv2.waitKey(0)
	return thresh

# Should take input from front end - an image and a feature type (string)
def jong(img: np.ndarray, feature: str):
	# ret3, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

	thresh = img_preprocess(img, showImg=False)

	# Identify how many possible circles there are based on contour filtering
	_, contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	if feature == 'circles':
		success, output, circles = detect_circles(thresh, contours, showImg=False)

		if success:
			print(evaluate_circle( output, circles[0:2] ))
		else: 
			print('No', feature, 'found :(')

	elif feature == 'lines':
		success, output, circles = detect_lines(thresh, contours, showImg=False)

		if success:
			cv2.imshow('Output', output)
			cv2.waitKey(0)
		else: 
			print('No', feature, 'found :(')

	else: 
		print('Unknown feature requested...')
	

	cv2.destroyAllWindows()

if __name__ == '__main__':
	# feature = 'circles'
	feature = 'lines'
	# Load an color image in grayscale
	# img = cv2.imread('./sample_circles/12.jpg', 0)
	img = cv2.imread('./sample_lines/5.jpg', 0)

	# for i in range(1,6):
	# 	img = cv2.imread('./sample_lines/' + str(i) + '.jpg', 0)
	# 	img_preprocess(img, showImg=True)

	jong(img, feature)