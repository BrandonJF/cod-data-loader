import cv2
import numpy as np
import pytesseract as tesseract
import re


# Load the image and template
img = cv2.imread("cod_data_loader/res/inventory1.jpg")
cropped_img = img[int(img.shape[0]/2):int(img.shape[0])]
img = cropped_img
template = cv2.imread("cod_data_loader/res/needle_level.jpg")

templateHeight,templateWidth, templateColorChannels = template.shape

print(template.shape)

# Convert to grayscale
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

# Create a window to display the image
cv2.namedWindow('Matching regions')

def extract_level_fraction(string):
    match = re.search(r'\d+\/\d+', string)
    if match:
        return match.group(0)
    else:
        return None

def on_trackbar(val):
    global threshold
    threshold = val/100
    # Perform template matching
    result = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)

    # Find all the matching regions
    locations = np.where(result >= threshold)
    # locations = list(zip(*locations[::-1]))
    rectangles = []
    # Draw rectangles around the matching regions
    img_copy = img.copy() 
    for pt in zip(*locations[::-1]):
        
        rightSideX = pt[0] + templateWidth * 2 #roughly setting it to twice the length of the template for bounding
        rightSideY = pt[1] + templateHeight
        bottomRightPt = (rightSideX, rightSideY)
        topLeftPt = (pt[0], pt[1] - round(templateHeight * 1.5))
        rect = [topLeftPt[0], topLeftPt[1], templateWidth * 3, round(templateHeight * 2.5)]
        rectangles.append(rect)
        # cv2.circle(img_copy, center= bottomRightPt, radius = 5, color = (255, 0, 0), thickness = 2)
    rectangles, weights = cv2.groupRectangles(rectangles, groupThreshold=1, eps=0.5)
    print(f'rectsFound: {len(rectangles)}')    
    for (x, y, w, h) in rectangles:
        topLeft = (x,y)
        bottomRight = (x + w, y + h)
        cv2.rectangle(img_copy, topLeft, bottomRight, (0, 0, 255), 2)
        image_roi = img_copy[topLeft[1]:bottomRight[1], 
                              topLeft[0]:bottomRight[0]] 
        text = tesseract.image_to_string(image_roi).splitlines()
        name, level = text[0], extract_level_fraction(text[1])
    
        print(f'weapon found: {name}: {level}') 
        # cv2.imshow("roi", image_roi)
        # cv2.waitKey(0)

    # Show the image with the matching regions
    cv2.imshow('Matching regions', img_copy)
# Create a trackbar to control the threshold
threshold = 0.7
cv2.createTrackbar('Threshold', 'Matching regions', int(threshold*100), 100, on_trackbar)

on_trackbar(int(threshold*100))
cv2.waitKey(0)
cv2.destroyAllWindows()



