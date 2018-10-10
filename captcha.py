import skimage
import matplotlib.pyplot as plt
import numpy as np
from skimage.filters import try_all_threshold
from skimage import exposure
from skimage import feature
from skimage.feature import match_template
from PIL import Image
from skimage.morphology import disk
import cv2
import imutils
import cv2
import os

def getfiles(path, types):
    """Get list of files available at a given path
      types: a list of possible files to extract, it can be any type.
      Example: getfiles('/tmp/',['.txt','.cpp','.m']); 
    
    """
    check_path(path)
    imlist = []
    for filename in os.listdir(path):
        if os.path.splitext(filename)[1].lower() in types:
            imlist.append(os.path.join(path, filename))

    return imlist


def check_path(fname, message=''):
    """ Function check for the validity of path (existence of file or directory path),
    if not found raise exception"""
    if len(message) == 0:
        message = 'path ' + fname + ' Not found'
    if not os.path.exists(fname):
        print message
        raise ValueError(message)


def binarize(image):
    img=skimage.io.imread(image)
    nimg=skimage.color.rgba2rgb(img)
    nimg=skimage.color.rgb2gray(nimg)
    thresh=skimage.filters.threshold_yen(nimg)
    binary=nimg>thresh
    plt.imsave('binary.jpg',binary,cmap='gray')

def make_temp(filename):
    template = cv2.imread(filename)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    template = cv2.Canny(template, 50, 200)
    (tH, tW) = template.shape[:2]
    return template


def temp_matching(img,template):
    image = cv2.imread(img)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    found = None
    (tH, tW) = template.shape[:2]
    for scale in np.linspace(0.2, 1.0, 20)[::-1]:
            # resize the image according to the scale, and keep track
            # of the ratio of the resizing
            resized = imutils.resize(gray, width = int(gray.shape[1] * scale))
            r = gray.shape[1] / float(resized.shape[1])

            # if the resized image is smaller than the template, then break
            # from the loop
            if resized.shape[0] < tH or resized.shape[1] < tW:
                break

            # detect edges in the resized, grayscale image and apply template
            # matching to find the template in the image
            edged = cv2.Canny(resized, 50, 200)
            result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
#             result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF_NORMED)
            (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

            # if we have found a new maximum correlation value, then ipdate
            # the bookkeeping variable
            if found is None or maxVal > found[0]:
                found = (maxVal, maxLoc, r)

    # unpack the bookkeeping varaible and compute the (x, y) coordinates
    # of the bounding box based on the resized ratio
    (_, maxLoc, r) = found
    print _
    (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
    (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))

    # draw a bounding box around the detected result and display the image
    # cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
    # cv2.imshow("Image", image)
    # cv2.waitKey(0)
    # key.append(k)
    # cv2.destroyAllWindows()

    
    return startX,endX,startY,endY,_


def main(temp,image):
    template=make_temp(temp)
    binarize(image)
    cords=temp_matching('./binary.jpg',template)
    if(cords[4]<3300000):
        return 0
    return cords


