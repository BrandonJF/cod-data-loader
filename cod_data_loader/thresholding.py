from __future__ import print_function
import cv2 as cv2
import numpy as np
from matplotlib import pyplot as plt
import utils.utils_image as image_util
import sys



def main(argv):
    # # read images
    # haystack_img = cv.imread("cod_data_loader/res/inventory2.jpg", cv.IMREAD_COLOR)
    # needle_img = cv.imread("cod_data_loader/res/needle_kastov.jpg", cv.IMREAD_COLOR)
    # # Load the image
    
    image = cv2.imread("cod_data_loader/res/inventory2.jpg")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    
    
    # Set the light grey threshold value (can be adjusted)
    light_grey = 55
    # Apply binary thresholding to filter out any pixels darker than the light grey value
    # apply basic thresholding -- the first parameter is the image
    # we want to threshold, the second value is is our threshold
    # check; if a pixel value is greater than our threshold (in this
    # case, 200), we set it to be *white, otherwise it is *black*
    # _, thresh = cv2.threshold(blur, light_grey, 255, cv2.THRESH_BINARY)
    
    (T, thresh) = cv2.threshold(blur, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # cv2.imshow("Threshold", threshInv)
    print("[INFO] otsu's thresholding value: {}".format(T))
    # Dilate to combine adjacent text contours
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
    dilate = cv2.dilate(thresh, kernel, iterations=4)

    # Find contours, highlight text areas, and extract ROIs
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    ROI_number = 0
    MIN_CONTROUR_AREA = 2000
    for c in cnts:
        area = cv2.contourArea(c)
        if area > MIN_CONTROUR_AREA:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 3)
            # ROI = image[y:y+h, x:x+w]
            # cv2.imwrite('ROI_{}.png'.format(ROI_number), ROI)
            # ROI_number += 1

    cv2.imshow('thresh', thresh)
    cv2.imshow('dilate', dilate)
    cv2.imshow('image', image)
    # cv2.imshow('gray', gray)
    cv2.waitKey()


if __name__ == "__main__":
    main(sys.argv[1:])
