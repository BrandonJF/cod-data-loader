import cv2
import numpy as np
import pytesseract as tesseract
import re


cap = cv2.VideoCapture('cod_data_loader/res/haystack_video_frame.png')
# cap = cv2.VideoCapture('cod_data_loader/res/FastWeapon.mp4')
template = cv2.imread("cod_data_loader/res/haystack_video_frame.png")
threshold = 0.6
templateHeight,templateWidth, templateColorChannels = template.shape

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
    # frame = frame[int(8*height/10):int(9*height/10), 0:width]
    frame = frame[int(33*height/40):int(9*height/10), 0:width]
    copy = frame.copy()
    cropped_img = frame
    gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("frame", gray)
    cv2.waitKey(0)
     # Find areas of image above threshold
    _, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    cv2.imshow("frame", thresh)
    cv2.waitKey(0)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding boxes around areas above threshold
    MIN_CONTROUR_AREA = 2000
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > MIN_CONTROUR_AREA:
            x, y, w, h = cv2.boundingRect(contour)
            topLeft = (x,y)
            bottomRight = (x + int(w / 2), y + h)
            cv2.rectangle(copy, topLeft, bottomRight, (0, 255, 0), 2)
            image_roi = copy[topLeft[1]:bottomRight[1], 
                                    topLeft[0]:bottomRight[0]] 
            text = tesseract.image_to_string(image_roi)
            print(text)
            # name, level = text[0], extract_level_fraction(text[1])
            # print(f'weapon found: {name}: {level}')

    # Show image
    cv2.imshow("Image", copy)

    # cv2.imshow("video", frame)
    # cv2.waitKey(0)
        
    

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



