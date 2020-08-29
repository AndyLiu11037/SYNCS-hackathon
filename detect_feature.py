# SYNCS Hackathon 2020
# jadaj - Circular

import cv2
import numpy as np

# Inputs:
# thresh (2d array-like): Binarised photo
# contours (list of lists): List of contours in thresh
# showImg (bool): Flag to show intermediate images for debugging

# Outputs:
# success (bool): Flag indicating successful identification of circle
# output (2d array-like): Binary image showing the circle
# accContours (list of 2d array-like): Masks featuring contour of found circle
def detect_circles(thresh: np.ndarray, contours, showImg: bool):
	print("Detecting circles...")
	markup = thresh.copy()
	markup = cv2.cvtColor(markup, cv2.COLOR_GRAY2BGR)

	# Apply circular hough transform to find candidate circles. 
	circles = cv2.HoughCircles( thresh, cv2.HOUGH_GRADIENT, 2, 10, 100, 100)
	try:
	 	# Check if null circle result (no circles found)
		avg = np.round( np.average(circles, axis=1)[0] ).astype("int")
		cv2.circle(markup, (avg[0], avg[1]), avg[2], ( 0, 0, 255), 4)

		# Find the closest matching contour to the hough circle
		# Compare min enclosing circle of contours to hough circle 
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
		output = cv2.bitwise_and(mask, thresh)

		# Show markup of closest contour to found circle and avg hough circle.
		cv2.drawContours(markup, [circContour], 0, (100,255,100), 3)
		if showImg:
			cv2.imshow("output", np.hstack([cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR), markup]))
			cv2.waitKey(0)

		cv2.imwrite('Output.png', output)
		success = True

	except: 
		success = False
		output = thresh
		avg = [0, 0, 0]

	return [success, output, avg]

# Inputs:
# thresh (2d array-like): Binarised photo
# contours (list of lists): List of contours in thresh
# showImg (bool): Flag to show intermediate images for debugging

# Outputs:
# success (bool): Flag indicating successful identification of at least 2 lines
# output (2d array-like): Binary image showing the found lines
# accContours (list of 2d array-like): Masks featuring contours of found lines
def detect_lines(thresh: np.ndarray, contours, showImg: bool):
	print("Detecting lines...")
	markup = thresh.copy()
	markup = cv2.cvtColor(markup, cv2.COLOR_GRAY2BGR)

	# Edge detection as prereq for hough lines
	edges = cv2.Canny(thresh, 50, 150, apertureSize = 7)
	mask = thresh * 0

	# Apply linear hough transform to find candidate circles. 
	lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/360, threshold=50, minLineLength=50, maxLineGap=30)
	output = thresh * 0
	try:
		areaLines = np.array([])
		for line in lines:
			for x1,y1,x2,y2 in line:
				cv2.line(mask, (x1,y1), (x2,y2), 255, 10)

		# Loop through all the contours and look for overlap with found lines
		accContours = [] 	# Array to store valid contour masks
		for contour in contours:
			cntMask = thresh * 0
			cv2.drawContours(cntMask, [contour], 0, 255, -1)
			cntCount = cv2.countNonZero(cntMask)

			areaAnd = cv2.countNonZero( cv2.bitwise_and(cntMask, mask) )
			
			# If 65% of the contour is covered by the hough lines, accept
			if (cntCount-areaAnd)/cntCount < 0.35:
				accContours.append(cntMask)
				cv2.drawContours(output, [contour], 0, 255, -1)
		
		if len(accContours) < 2 or len(accContours) > 100:
			success = False 
			print("Couldn't properly find lines")
		else:
			success = True
			cv2.imwrite('LineOutput.png', output)
		
	except:
		success = False
			
	if showImg:
		cv2.imshow( 'Edges, output', np.hstack( [cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR), cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR), markup] ) )
		cv2.waitKey(0)

	return [success, output, accContours]