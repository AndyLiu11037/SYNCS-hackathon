# Evaluate Circle

# Inputs:
# image (2d array-like): Will consider all non-zero entries in array as part of circle
# centre ((float, float))

# Outputs:
# (int) score from 0 to 100
import numpy as np
import statsmodels.api as sm

def evaluate_circle(image: np.ndarray, centre: tuple):
    centre = centre[::-1]
    coords = np.argwhere(image)
    shifted = coords - centre
    theta, r = np.arctan2(shifted[:,0], shifted[:,1]), np.sqrt(shifted[:,0]**2 + shifted[:,1]**2)
    shuffle = np.argsort(theta)
    theta = theta[shuffle]
    r = r[shuffle]
    smoothed = sm.nonparametric.lowess(r,theta,frac=1/30,it=3, return_sorted = False)
    theta_samp = np.linspace(min(theta), max(theta),200)
    r_spaced = np.interp(theta_samp,theta,smoothed)
    
    radius = np.median(r_spaced)
    error = np.mean(abs(r_spaced - radius))/radius
    
    score =  2 - 2/(1+np.exp(-8*error))
    return int(score*1000)/10