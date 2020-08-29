# Inputs:
# l1,l2 (2d array-likes): Will consider all non-zero entries in array as part of respective line

# Output:
# angle (float)
def evaluate_lines(l1,l2):
    coords1, coords2 = np.argwhere(l1), np.argwhere(l2)
    m1 = np.polyfit(coords1[:,0],coords1[:,1],1)[0]
    m2 = np.polyfit(coords2[:,0],coords2[:,1],1)[0]
    angle = np.rad2deg(np.arctan(abs(m1-m2)/(1+m1*m2)))
    return int(10*angle)/10