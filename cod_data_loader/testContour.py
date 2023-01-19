from __future__ import print_function
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import utils.utils_image as image_util
import sys


use_mask = False
img = None
templ = None
mask = None
image_window = "Source Image"
result_window = "Result window"
match_method = 0
max_Trackbar = 5

match_method = 0
max_Trackbar = 5



def main(argv):
    # read images
    haystack_img = cv.imread("cod_data_loader/res/inventory2.jpg", cv.IMREAD_COLOR)
    needle_img = cv.imread("cod_data_loader/res/needle_kastov.jpg", cv.IMREAD_COLOR)
    mask = cv.imread("cod_data_loader/res/needle_kastov_mask_more.jpg", cv.IMREAD_COLOR)
    
    haystack_img = cv.cvtColor(haystack_img, cv.COLOR_BGR2GRAY)
    # haystack_img = cv.adaptiveThreshold(haystack_img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 115, 1)

    
        
        # There are 6 comparison methods to choose from:
    # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
    # You can see the differences at a glance here:
    # https://docs.opencv.org/master/d4/dc6/tutorial_py_template_matching.html
    # Note that the values are inverted for TM_SQDIFF and TM_SQDIFF_NORMED
    result = cv.matchTemplate(haystack_img, needle_img, cv.TM_SQDIFF_NORMED, mask=mask)

    # I've inverted the threshold and where comparison to work with TM_SQDIFF_NORMED
    threshold = 0.15
    # The np.where() return value will look like this:
    # (array([482, 483, 483, 483, 484], dtype=int32), array([514, 513, 514, 515, 514], dtype=int32))
    locations = np.where(result <= threshold)
    # We can zip those up into a list of (x, y) position tuples
    locations = list(zip(*locations[::-1]))
    print(locations)

    if locations:
        print('Found needle.')

        needle_w = needle_img.shape[1]
        needle_h = needle_img.shape[0]
        line_color = (0, 255, 0)
        line_type = cv.LINE_4

        # Loop over all the locations and draw their rectangle
        for loc in locations:
            # Determine the box positions
            top_left = loc
            bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)
            # Draw the box
            cv.rectangle(haystack_img, top_left, bottom_right, line_color, line_type)

        cv.imshow('Matches', haystack_img)
        cv.waitKey()
        #cv.imwrite('result.jpg', haystack_img)

    else:
        print('Needle not found.') 


if __name__ == "__main__":
    main(sys.argv[1:])
