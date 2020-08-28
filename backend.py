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

# ret3, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

cv2.imshow('Image', cv2.hconcat([img, blur, thresh]) )
# cv2.imshow('Image', cv2.hconcat(img, cv2.hconcat(blur, thresh) ) )
cv2.waitKey(0)


# Apply circular hough transform to find candidate circles. 


cv2.destroyAllWindows()