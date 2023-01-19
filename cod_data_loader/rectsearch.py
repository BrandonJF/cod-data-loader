from __future__ import print_function
import cv2 as cv2
import numpy as np
from matplotlib import pyplot as plt
import utils.utils_image as image_util
import sys

global img
global orig

#just converting formats of numpy arrays to pass it from one cv2 function to another.
def convert_for_bounding(coords):
    nb_pts=len(coords[0])
    coordz=np.zeros((nb_pts,2))
    for i in range(nb_pts):
        coordz[i,:]=np.array([int(coords[0][i]),int(coords[1][i])])
    return coordz

#finding width and length of bounding boxes
def find_wid(xs):
    maxx=0
    for i in range(4):
        for j in range(i+1,4):
            if abs(xs[i]-xs[j])>=maxx:
                maxx=abs(xs[i]-xs[j])
    return maxx


    
def RunOps(val):
    threshold_upper_value = cv2.getTrackbarPos(trackbar_upper_value, window_name)
    threshold_lower_value = cv2.getTrackbarPos(trackbar_lower_value, window_name)
    threshold_area_value = cv2.getTrackbarPos(trackbar_area_value, window_name)
    global img
    newImage = img.copy()
    #thresholding with your "180 - 240" range
    img = cv2.inRange(img, 180, 240)

    #finding all components
    nb_edges, output, stats, centroids = cv2.connectedComponentsWithStats(img, connectivity=8)
    size_edges = stats[1:, -1]; nb_edges = nb_edges - 1
    contours=[]
    for i in range(0, nb_edges):
        #eliminating small components
        if size_edges[i]>=100:
            img2=np.zeros((h,w))
            img2[output == i + 1] = 255
            contours.append(convert_for_bounding(np.nonzero(img2)))
    
    #finding bounding rectangle for each component
    for i in range(0,len(contours)):
        c=np.array(contours[i]).astype(int)
        ar=cv2.minAreaRect(c)
        box = cv2.boxPoints(ar)
        box = np.int0([box[:,1],box[:,0]]).T
        xs=box[:,0]
        ys=box[:,1]
        wid=find_wid(xs)
        hei=find_wid(ys)

        #for each rectangle, we'll check if its ratio is like a card one
        card_ratio = 285 / 205
        if hei!=0:
            if hei/wid <=card_ratio*1.05 and hei/wid >= card_ratio*0.95:
                cv2.drawContours(orig, [box], -1, (0,0,255), 2)       
    cv2.imshow('orig', orig)

    cv2.imshow('newimage', newImage)
    cv2.waitKey()
    # cv2.imshow('gray', gray)
    # cv2.imshow('canny', canny)



max_value = 255
max_type = 4
max_binary_value = 255
trackbar_type = 'Type: \n 0: Binary \n 1: Binary Inverted \n 2: Truncate \n 3: To Zero \n 4: To Zero Inverted'
trackbar_upper_value = 'uppercanny'
trackbar_lower_value = 'lowercanny'
trackbar_area_value = 'contarea'
window_name = 'canny'


img = cv2.imread("cod_data_loader/res/inventory1.jpg")
orig=np.copy(img)
img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
h,w=img.shape


cv2.namedWindow(window_name)
cv2.createTrackbar(trackbar_upper_value, window_name , 0, max_value, RunOps)
cv2.createTrackbar(trackbar_lower_value, window_name , 0, max_value, RunOps)
cv2.createTrackbar(trackbar_area_value, window_name , 0, max_value, RunOps)
RunOps(0)

