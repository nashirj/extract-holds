"""Example"""

import holdDetector as hd

#Open dialog to select image
path = 'Image3.jpeg'
# path = '../wall_pics/wall3.png'
img = hd.openImage(path)

# Set initial detector parameters
hd.buildDetector(minArea = 500)

# Finds each hold. Returns keypoints for each hold
# and the points that define the contours of each hold
holds, contours = hd.findHolds(img)

# #Finds a color associated with each keypoint
# colors = hd.findColors(img,holds)

#Draws keypoints onto image and plots colors in 3D space
hd.draw(img,holds)
# hd.plotColors(colors)