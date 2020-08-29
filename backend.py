import cv2
import numpy as np
import argparse

# Load an color image in grayscale
img = cv2.imread('./sample_images/7.jpg', 0)

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

# ret3, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# cv2.imshow('Image', cv2.hconcat([img, blur, thresh]) )
# cv2.waitKey(0)

markup = thresh.copy()
markup = cv2.cvtColor(markup, cv2.COLOR_GRAY2BGR)

# Identify how many possible circles there are based on contour filtering
_, contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# for i in range(0, len(contours)): 
# 	contour = contours[i]
# 	# Check circular: 
# 	(x,y), rad = cv2.minEnclosingCircle( contour )
# 	circArea = np.pi*rad**2
# 	contArea = cv2.contourArea( contour )
# 	perim = cv2.arcLength(contour, True)
# 	cv2.drawContours(output, contours, i, (0,255,100), 3)
# 	print(circArea, contArea, perim)
# 	if abs( (circArea-contArea) ) / circArea < 0.2:
# 		print("yes")

# 	cv2.imshow('image', output)
# 	cv2.waitKey(0)

# Apply circular hough transform to find candidate circles. 
circles = cv2.HoughCircles( thresh, cv2.HOUGH_GRADIENT, 2, 20, 100, 100)#, minRadius=20, maxRadius=100 )
print(circles)
if circles is not None:
	avg = np.round( np.average(circles, axis=1)[0] ).astype("int")
	# convert the (x, y) coordinates and radius of the circles to integers
	circles = np.round(circles[0, :]).astype("int")
	# loop over the (x, y) coordinates and radius of the circles
	for (x, y, r) in circles:
		# draw the circle in the output image, then draw a rectangle
		# corresponding to the center of the circle
		red = int(10*(x%20))
		green = int(255-20*(y%20))
		# print(red,green)
		# cv2.circle(output, (x, y), r, ( red, green, 0), 4)
		# cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
	
	# show the output image
	print(avg)
	cv2.circle(markup, (avg[0], avg[1]), avg[2], ( 0, 0, 255), 4)
	cv2.imshow("output", np.hstack([cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR), markup]))
	# cv2.waitKey(0)

# Find the closest contour
minDist = 999
circContour = 0
for contour in contours: 
	(x,y), rad = cv2.minEnclosingCircle( contour )
	currDist = np.sqrt( (x-avg[0])**2 + (y-avg[1])**2 )	# Euclidean distance
	if currDist < minDist:
		minDist = currDist
		circContour = contour
		encCircle = [(int(x), int(y)), int(rad)]

# Create a annulus mask with min enclosing circle to extract the true circle. 
# Bitwise AND to extract. Magic number for annulus centre. 
mask = thresh * 0
cv2.circle(mask, encCircle[0], encCircle[1], 255, -1)
cv2.circle(mask, encCircle[0], int(encCircle[1]/2), 0, -1)
truOutput = cv2.bitwise_and(mask, thresh)
cv2.imshow( "maskk", np.hstack([mask, truOutput]) )
cv2.waitKey(0)

# Show markup of closest contour to found circle and avg hough circle.
cv2.drawContours(markup, [circContour], 0, (100,255,100), 3)
cv2.imshow("output", np.hstack([cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR), markup]))
cv2.waitKey(0)

cv2.destroyAllWindows()