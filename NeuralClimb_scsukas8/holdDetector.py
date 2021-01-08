import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
from util import openFile, showImage
import colorsys
from mpl_toolkits.mplot3d import Axes3D


def openImage(file_path=None):
    # Open Image
    file_path = openFile() if not file_path else file_path
    img = cv2.imread(file_path,1)

    # Image can be resized to a standard size to speed up processing.
    c = 1000.0/img.shape[0]
    x = int(img.shape[0] * c)
    y = int(img.shape[1] * c)
    img = cv2.resize(img, (y,x))

    return img

""" Object detection """

def buildDetector(minArea = 25):
    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    params.minThreshold = 0
    params.maxThreshold = 255


    # Filter by Area.
    params.filterByArea = True
    params.minArea = minArea

    # Filter by Circularity
    params.filterByCircularity = False
    params.minCircularity = 0.1

    # Filter by Convexity
    params.filterByConvexity = False
    params.minConvexity = 0.1
        
    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = 0.05

    # Create a detector with the parameters
    ver = (cv2.__version__).split('.')
    if int(ver[0]) < 3 :
        detector = cv2.SimpleBlobDetector(params)
    else : 
        detector = cv2.SimpleBlobDetector_create(params)

    return detector


def findHolds(img,detector = None):
    # Applying a gaussian blur removes some small impurities that
    # could fool the detection algorithm. It also smooths out the
    # color of each hold to make it more uniform.
    img = cv2.GaussianBlur(img, (5, 5), 0)

    # Using Otsu's method, the optimal threshold for the image can be found.
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    otsu, _ = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # Applys edge detection to find the borders between the hold and the wall
    # Otsu's threshold is intended to be used as the higher threshold with a
    # lower:upper ratio of 1:2. L2gradient is included for more precise results.
    edges = cv2.Canny(img,otsu, otsu * 2, L2gradient = True)
    # print(otsu)

    # Finds the contours of the image, without retaining the hierarchy or img
    _, contours, _ = cv2.findContours(edges,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    # print("contours")
    # print(len(contours))
    # Applies convex hulls to each contour, ensuring each contour
    # is a closed polygon.
    hulls = list(map(cv2.convexHull,contours))
    
    # Draws contours onto a blank canvas
    mask = np.zeros(img.shape,np.uint8)

    cv2.drawContours(mask,hulls,-1,(255,255,255),-1)

    showImage(mask)

    if detector == None:
        # Set up the detector with default parameters.
        detector = buildDetector()

    keypoints = detector.detect(mask)
    return keypoints , hulls



""" Color manipulations """

def getColorBin(img, tl, br):
    # Creates mask over image focus
    mask = np.zeros(img.shape[:2], np.uint8)
    mask[tl[1]:br[1], tl[0]:br[0]] = 255

    # Effecively quantizes the image when the histogram is made.
    # Useful for grouping similar colors.
    binLen = 4
    numBins = 256 / binLen

    #Finds the most common color/in the histogram/for each color channel.
    binColor = map(
        lambda x: np.argmax(
        [cv2.calcHist([img],[x],mask,[numBins],[0,256])])
        ,[0,1,2])

    fullColor = map(lambda x: x * binLen, binColor)

    return fullColor 

def findColors(img,keypoints):
    # If no keypoints return nothing
    if (keypoints == []):
        return []

    # Shift colorspace to HLS
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)

    # Preallocate space for color array corresponding to keypoints
    colors = np.empty([len(keypoints),3])

    # Iterates through the keypoints and finds the most common
    # color at each keypoint.
    for i, key in enumerate(keypoints):
        x = int(key.pt[0])
        y = int(key.pt[1])

        size = int(math.ceil(key.size)) 

        #Finds a rectangular window in which the keypoint fits
        br = (x + size, y + size)   
        tl = (x - size, y - size)

        color = getColorBin(hsv,tl,br)
        # for col in color:
        #     print(col)
        colors[i] = color
    
    return colors


""" Visualization """
def draw(img, keypoints):
    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the 
    # size of the circle corresponds to the size of blob
    for i, key in enumerate(keypoints):
        x = int(key.pt[0])
        y = int(key.pt[1])

        size = int(math.ceil(key.size)) 

        #Finds a rectangular window in which the keypoint fits
        br = (x + size, y + size)   
        tl = (x - size, y - size)
        cv2.rectangle(img,tl,br,(0,0,255),2)

    #OpenCV uses BGR format, so that'll need to be reversed for display
    img = img[...,::-1]

    # Display the resulting frame
    fig = plt.imshow(img)
    plt.title("Image with Keypoints")
    plt.show()




def plotColors(colors):

    # Build 3D scatterplot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Initialize arrays
    hs = []
    ls = []
    ss = []

    # Color data is mapped between 0 and 1
    colors = colors/256

    for color in colors:
        hs.append(color[0])
        ls.append(color[1])
        ss.append(color[2])

    # Regain RGB Values to color each data point
    colorsRGB = map(colorsys.hls_to_rgb,hs,ls,ss) 

    # Plot points in HLS space
    ax.scatter(hs, ls, ss, c=colorsRGB, marker='o')

    ax.set_xlabel('Hue')
    ax.set_ylabel('Lightness')
    ax.set_zlabel('Saturation')

    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    ax.set_zlim(0,1)

    plt.title("Color Space of Keypoints")
    plt.show()