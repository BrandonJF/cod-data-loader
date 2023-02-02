import cv2
import numpy as np
import pytesseract as tesseract
import re


# Load the image and template
# img = cv2.imread("cod_data_loader/res/inventory1.jpg")
# cropped_img = img[int(img.shape[0]/2):int(img.shape[0])]
# img = cropped_img

cap = cv2.VideoCapture('cod_data_loader/res/haystack_video_frame.png')
# cap = cv2.VideoCapture('cod_data_loader/res/FastWeapon.mp4')
# cap = cv2.VideoCapture('cod_data_loader/res/haystack_video_frame.png')

# template = cv2.imread("cod_data_loader/res/needle_level_video_small.png")
# template = cv2.imread("cod_data_loader/res/needle_level_hires.png")
template = cv2.imread("cod_data_loader/res/haystack_video_frame.png")

threshold = 0.6


templateHeight,templateWidth, templateColorChannels = template.shape

print(template.shape)

# Convert to grayscale
# img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

# Create a window to display the image
cv2.namedWindow('Matching regions')

def extract_level_fraction(string):
    match = re.search(r'\d+\/\d+', string)
    if match:
        return match.group(0)
    else:
        return None

def processFrame(frame):
    # global threshold
    # threshold = val/100
    # Perform template matching
    # cropped_img = frame[int(frame.shape[0]/2):int(frame.shape[0])]
    height, width, channels = frame.shape
    frame = frame[int(33*height/40):int(9*height/10), 0:width]
    cropped_img = frame
    img_gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("frame", img_gray)
    cv2.waitKey(0)
    result = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    # result = cv2.matchTemplate(img_gray, template_gray, cv2.TM_SQDIFF_NORMED)

    # Find all the matching regions
    locations = np.where(result >= threshold)
    # locations = list(zip(*locations[::-1]))
    
    if locations:
        rectangles = []
        # Draw rectangles around the matching regions
        img_copy = cropped_img.copy() 
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
        if len(rectangles) > 0: 
            for (x, y, w, h) in rectangles:
                topLeft = (x,y)
                bottomRight = (x + w, y + h)
                cv2.rectangle(img_copy, topLeft, bottomRight, (0, 0, 255), 2)
                image_roi = img_copy[topLeft[1]:bottomRight[1], 
                                    topLeft[0]:bottomRight[0]] 
                # text = tesseract.image_to_string(image_roi).splitlines()
                # name, level = text[0], extract_level_fraction(text[1])
            
                # print(f'weapon found: {name}: {level}') 
                cv2.imshow("roi", image_roi)
                # cv2.waitKey(0)

                # Show the image with the matching regions
                # cv2.imshow('Matching regions', img_copy) #undo this
                cv2.waitKey(0)
    cv2.imshow("video", frame)
    cv2.waitKey(0)
        
    

# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")
while cap.isOpened():
    success, image = cap.read()
    if (success):
        processFrame(image)
    else:
        break
# Create a trackbar to control the threshold
# cv2.createTrackbar('Threshold', 'Matching regions', int(threshold*100), 100, on_trackbar)

# on_trackbar(int(threshold*100))
# cv2.waitKey(0)
cv2.destroyAllWindows()



