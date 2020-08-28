import cv2
import numpy as np
import argparse

# Load an color image in grayscale
img = cv2.imread('./sample_images/10.jpg', 0)

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

output = thresh.copy()
output = cv2.cvtColor(output, cv2.COLOR_GRAY2BGR)

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
		print(red,green)
		cv2.circle(output, (x, y), r, ( red, green, 0), 4)
		cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
	# show the output image
	print(avg)
	cv2.circle(output, (avg[0], avg[1]), avg[2], ( 0, 0, 255), 4)
	cv2.imshow("output", np.hstack([cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR), output]))
	cv2.waitKey(0)

cv2.destroyAllWindows()