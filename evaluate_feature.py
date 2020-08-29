# SYNCS Hackathon 2020
# jadaj - Circular

import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import cv2

# Inputs:
# image (2d array-like): Will consider all non-zero entries in array as part of circle
# centre ((float, float))

# Outputs:
# (int) score from 0 to 100
def evaluate_circle(image, centre):
    
    # Evaluation
    centre = centre[::-1]
    coords = np.argwhere(image)
    shifted = coords - centre
    theta, r = np.arctan2(shifted[:,0], shifted[:,1]), np.sqrt(shifted[:,0]**2 + shifted[:,1]**2)
    shuffle = np.argsort(theta)
    theta = theta[shuffle]
    r = r[shuffle]
    smoothed = sm.nonparametric.lowess(r,theta,frac=1/30,it=3, return_sorted = False)
    theta_samp = np.linspace(min(theta), max(theta),40)
    r_spaced = np.interp(theta_samp,theta,smoothed)
    
    radius = np.median(r_spaced)
    error = np.mean(abs(r_spaced - radius))/radius
    
    score =  2 - 2/(1+np.exp(-8*error))
    score = int(score*1000)/10
    
    # Shifting
    scale = 1.4
    height, width = image.shape
    top, bottom = int(centre[0] - radius*scale), int(centre[0] + radius*scale)
    left,right = int(centre[1] - radius*scale), int(centre[1] + radius*scale)
    toppad, bottompad = 0 - min(0,top), max(height,bottom) - height
    leftpad, rightpad = 0 - min(0,left), max(width,right) - width
    img_cut = image[max(0,top):bottom, max(0,left):right]
    n_height = img_cut.shape[0]
    img_stretch = np.hstack([np.zeros([n_height,leftpad]), img_cut, np.zeros([n_height,rightpad])])
    new_width = img_stretch.shape[1]
    img_stretch = np.vstack([np.zeros([toppad,new_width]), img_stretch, np.zeros([bottompad, new_width])])
    new_img = cv2.resize(img_stretch,(800,800))
    new_centre = (400,400)
    new_radius = 400/scale

    # Arrows
    coord_set = set(tuple(x) for x in np.argwhere(new_img).tolist())
    fig, ax = plt.subplots(figsize = (8,8))
    plt.imshow(new_img ==0 , 'gray')
    for phi in np.linspace(0, 2*np.pi, 60, endpoint = False):
        circle_point = new_radius*np.cos(phi) + new_centre[0], new_radius*np.sin(phi) + new_centre[1]
        dx,dy = 0.5*np.cos(phi), 0.5*np.sin(phi)
        x,y = new_centre
        ray_set = {new_centre}
        while (x>=0) and (x<800) and (y>=0) and (y<800):
            x += dx
            y += dy
            ray_set.add((int(x), int(y)))
        intersections = list(ray_set & coord_set)
        if len(intersections) > 0:
            draw_point = np.mean(np.array(intersections), axis = 0)
            vector = (circle_point - draw_point)
            if np.linalg.norm(vector)/new_radius > 0.03:
                plt.arrow(draw_point[1], draw_point[0], vector[1]*3,vector[0]*3, head_width=7, head_length=11, fc='r', ec='k')
    plt.axis('off')
    plt.savefig('overlay.png', bbox_inches='tight')
    plt.close()
    return score

# Inputs:
# l1,l2 (2d array-likes): Will consider all non-zero entries in array as part of respective line

# Output:
# angle from parallel (float)
def evaluate_lines(line_array):
    min_angle = np.inf
    coords = [np.argwhere(l) for l in line_array]
    gradients = [np.polyfit(c[:,0],c[:,1],1)[0] for c in coords]
    n = len(gradients)
    for i in range(n):
        for j in range(i+1,n):
            min_angle = min(min_angle, 
                            np.rad2deg(np.arctan(abs(gradients[i]-gradients[j])/(1+gradients[i]*gradients[j]))))
    return int(100*min_angle)/100