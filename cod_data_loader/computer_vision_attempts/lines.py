import cv2 as cv2
import numpy as np

trackbar_upper_value = 'uppercanny'
trackbar_lower_value = 'lowercanny'
trackbar_area_value = 'contarea'
window_modification_name = 'window_mods'
max_value = 255
image = cv2.imread("cod_data_loader/res/inventory1.jpg")

def createTrackers():
    cv2.namedWindow(window_modification_name)
    cv2.createTrackbar(trackbar_upper_value, window_modification_name , 0, max_value, ShowLines)
    cv2.createTrackbar(trackbar_lower_value, window_modification_name , 0, max_value, ShowLines)
    cv2.createTrackbar(trackbar_area_value, window_modification_name , 0, max_value, ShowLines)
    
def ShowLines(val):
    result = image.copy()

    global thresh
    global opening
    threshold_area_value = cv2.getTrackbarPos(trackbar_area_value, window_modification_name)
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray,100,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,51,9)

    # Fill rectangular contours
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(thresh, [c], -1, (255,255,255), -1)

    # Morph open
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=4)

    # Draw rectangles
    cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 3)
        
ShowLines(0)
createTrackers()
cv2.imshow(window_modification_name, thresh)
cv2.imshow('opening', opening)
cv2.imshow('image', image)
cv2.waitKey()