from __future__ import print_function
import cv2 as cv2
import numpy as np
from matplotlib import pyplot as plt
import utils.utils_image as image_util
import sys


max_value = 255
max_type = 4
max_binary_value = 255
trackbar_type = 'Type: \n 0: Binary \n 1: Binary Inverted \n 2: Truncate \n 3: To Zero \n 4: To Zero Inverted'
trackbar_upper_value = 'uppercanny'
trackbar_lower_value = 'lowercanny'
trackbar_area_value = 'contarea'
window_name = 'canny'
global thresh
global image
global canny

image = None

def main(argv):
    # # read images
    # haystack_img = cv.imread("cod_data_loader/res/inventory2.jpg", cv.IMREAD_COLOR)
    # needle_img = cv.imread("cod_data_loader/res/needle_kastov.jpg", cv.IMREAD_COLOR)
    # # Load the image
    global image
    global canny
    global blur
    image = cv2.imread("cod_data_loader/res/inventory1.jpg")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    
    cv2.namedWindow(window_name)
    cv2.createTrackbar(trackbar_upper_value, window_name , 0, max_value, ShowWindows)
    cv2.createTrackbar(trackbar_lower_value, window_name , 0, max_value, ShowWindows)
    cv2.createTrackbar(trackbar_area_value, window_name , 0, max_value, ShowWindows)
    ShowWindows(0)
  
    cv2.waitKey()
    
def ShowWindows(val):
    threshold_upper_value = cv2.getTrackbarPos(trackbar_upper_value, window_name)
    threshold_lower_value = cv2.getTrackbarPos(trackbar_lower_value, window_name)
    threshold_area_value = cv2.getTrackbarPos(trackbar_area_value, window_name)
    canny = cv2.Canny(blur, threshold_lower_value, threshold_upper_value, 1)

    # Find contours
    cnts = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    ROI_number = 0
    MIN_CONTROUR_AREA = threshold_area_value
    conts_found = 0
    newImage = image.copy()

    for c in cnts:
        area = cv2.contourArea(c)
        if area > MIN_CONTROUR_AREA:
            conts_found += 1
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(newImage, (x, y), (x + w, y + h), (36,255,12), 3)
            # ROI = image[y:y+h, x:x+w]
            # cv2.imwrite('ROI_{}.png'.format(ROI_number), ROI)
            # ROI_number += 1
    # cv2.imshow('thresh', thresh)
    # cv2.imshow('dilate', dilate)
    print(f'Conts found {conts_found}')
    cv2.imshow('image', newImage)
    # cv2.imshow('gray', gray)
    cv2.imshow('canny', canny)


if __name__ == "__main__":
    main(sys.argv[1:])
