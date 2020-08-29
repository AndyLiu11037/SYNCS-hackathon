import cv2
import numpy as np

def detect_circles(thresh: np.ndarray, contours, showImg: bool):
	print("Detecting circles...")
	markup = thresh.copy()
	markup = cv2.cvtColor(markup, cv2.COLOR_GRAY2BGR)

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
	circles = cv2.HoughCircles( thresh, cv2.HOUGH_GRADIENT, 2.2, 20, 100, 100)#, minRadius=20, maxRadius=100 )
	# print(circles)
	try:
	# if circles is not None:
	# 	# Check if null circle result (no circles found)
	# 	if len( circles.shape ) > 1:
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
		# cv2.imshow("output", np.hstack([cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR), markup]))
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
		output = cv2.bitwise_and(mask, thresh)
		# cv2.imshow( "maskk", np.hstack([mask, output]) )
		# cv2.waitKey(0)

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

def detect_lines(thresh: np.ndarray, contours, showImg: bool):
	print("Detecting lines...")
	markup = thresh.copy()
	markup = cv2.cvtColor(markup, cv2.COLOR_GRAY2BGR)

	# Edge detection as prereq for hough lines
	edges = cv2.Canny(thresh, 50, 150, apertureSize = 7)
	mask = thresh * 0

	# Apply linear hough transform to find candidate circles. 
	lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/360, threshold=50, minLineLength=100, maxLineGap=30)
	print(lines)
	try:
		areaLines = np.array([])
		for line in lines:
			for x1,y1,x2,y2 in line:
				cv2.line(mask, (x1,y1), (x2,y2), 255, 10)

		# Loop through all the contours and look for overlap with found lines
		accContours = [] 	# Array to store valid contours
		for contour in contours:
			mask2 = thresh * 0
			cv2.drawContours(mask2, [contour], 0, 255, -1)
			area = cv2.countNonZero(mask2)

			areaAnd = cv2.countNonZero( cv2.bitwise_and(mask2, mask) )
			
			# print(area, areaCont, areaAnd)
			# If 65% of the contour is covered by the hough lines, accept
			if (area-areaAnd)/area < 0.35:
				accContours.append(contour)
		success = True
	except:
		print("No lines found :(")
		success = False
			
	if showImg:
		cv2.imshow( 'Edges, output', np.hstack( [cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR), cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR), markup] ) )
		cv2.waitKey(0)

	output = markup
	cv2.imwrite('LineOutput.png', output)
	avg = [0,0,0]

	return [success, output, avg]