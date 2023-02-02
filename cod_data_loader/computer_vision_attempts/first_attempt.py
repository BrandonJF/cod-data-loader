from __future__ import print_function
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import utils.utils_image as image_util
import sys


use_mask = True
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

    global img
    global templ

    img = cv.imread("cod_data_loader/res/inventory1.jpg", cv.IMREAD_COLOR)
    templ = cv.imread("cod_data_loader/res/needle_kastov.jpg", cv.IMREAD_COLOR)
    mask = cv.imread("cod_data_loader/res/needle_kastov_mask.jpg", cv.IMREAD_COLOR)

    if (img is None) or (templ is None):
        print("Can't read one of the images.")
        return -1

    cv.namedWindow(image_window, cv.WINDOW_AUTOSIZE)
    cv.namedWindow(result_window, cv.WINDOW_AUTOSIZE)
    
      
    trackbar_label = 'Method: \n 0: SQDIFF \n 1: SQDIFF NORMED \n 2: TM CCORR \n 3: TM CCORR NORMED \n 4: TM COEFF \n 5: TM COEFF NORMED'
    cv.createTrackbar( trackbar_label, image_window, match_method, max_Trackbar, MatchingMethod )
    
    MatchingMethod(match_method)



def MatchingMethod(param):
    global match_method
    match_method = param
    
    img_display = img.copy()
    
    method_accepts_mask = (cv.TM_SQDIFF == match_method or match_method == cv.TM_CCORR_NORMED)
    if (use_mask and method_accepts_mask):
        result = cv.matchTemplate(img, templ, match_method, None, mask)
    else:
        result = cv.matchTemplate(img, templ, match_method)
    
    
    cv.normalize( result, result, 0, 1, cv.NORM_MINMAX, -1 )
    
    _minVal, _maxVal, minLoc, maxLoc = cv.minMaxLoc(result, None)
    
    
    if (match_method == cv.TM_SQDIFF or match_method == cv.TM_SQDIFF_NORMED):
        matchLoc = minLoc
    else:
        matchLoc = maxLoc
    
    
    cv.rectangle(img_display, matchLoc, (matchLoc[0] + templ.shape[0], matchLoc[1] + templ.shape[1]), (0,0,0), 2, 8, 0 )
    cv.rectangle(result, matchLoc, (matchLoc[0] + templ.shape[0], matchLoc[1] + templ.shape[1]), (0,0,0), 2, 8, 0 )
    cv.imshow(image_window, img_display)
    cv.imshow(result_window, result)
    if cv.waitKey(0) == 27:
        cv.destroyAllWindows()
    pass


if __name__ == "__main__":
    main(sys.argv[1:])
