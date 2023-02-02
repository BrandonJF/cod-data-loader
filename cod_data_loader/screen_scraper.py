import cv2
import numpy as np
import pytesseract as tesseract
import re


# cap = cv2.VideoCapture('cod_data_loader/res/haystack_video_frame.png')
cap = cv2.VideoCapture('cod_data_loader/res/SlowBrowse.mp4')
threshold = 0.6
curr_frame = 0 
curr_second = 0

def extract_level_fraction(string):
    match = re.search(r'\d+\/\d+', string)
    if match:
        return match.group(0)
    else:
        return None
    
def cleanString(string):
    clean_str = re.sub(r"[^-/\w\d\s]", "", string)
    return clean_str

def processFrame(frame):
    height, width, channels = frame.shape
    offset_start = int(33*height/40)
    offset_end = int(9*height/10)
    partial_frame = frame[offset_start:offset_end, 0:width]
    cropped_img = partial_frame
    gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
    blurAmt = 3
    blur = cv2.GaussianBlur(gray, (blurAmt, blurAmt), 0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
    horizontal = np.copy(thresh)
    
    # Specify size on horizontal axis
    cols = horizontal.shape[1]
    horizontal_size = cols / 50
    horizontal_size=int(horizontal_size)

    # Create structure element for extracting horizontal lines through morphology operations
    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))
    
    # Apply morphology operations
    horizontal = cv2.erode(thresh, horizontalStructure)
    horizontal = cv2.dilate(horizontal, horizontalStructure)

    hcnts = cv2.findContours(horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    hcnts = hcnts[0] if len(hcnts) == 2 else hcnts[1]
    for c in hcnts:
        cv2.drawContours(thresh, [c], -1, (0,0,0), 2) # paint the horiz lines black on the thresholded image

    vertical_kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (3,13))
    dilate = cv2.dilate(thresh, vertical_kernal, iterations= 1)
    
    conts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(conts) > 0:
        conts = conts[0] if len(conts) == 2 else conts[1]
        conts = sorted(conts,  key= lambda x: cv2.boundingRect(x)[0])
        for c in conts:
            x, y, w, h = cv2.boundingRect(c)
            topLeft = (x,y)
            bottomRight = (x + w,y + h)
            if h > 20 and w > 80 and w < 160:
                cv2.rectangle(frame, (x, y+ offset_start), (x+w, y+h + offset_start),(36,255, 12), 2)
    
                image_roi = gray[y:y+h, x:x+w]
                image_roi = cv2.resize(image_roi, None, fx=3, fy=3, interpolation=cv2.INTER_LINEAR)
                
                text = tesseract.image_to_string(image_roi, config='--psm 4 --oem 1')
                text = cleanString(text).splitlines()
                if len(text) > 1:
                # print(text)
                    name, level = text[0], extract_level_fraction(text[1])
                    if (False and level == None):
                        cv2.imshow("roi", image_roi)
                        print(text)
                        cv2.waitKey(0)
                    print(f'weapon found: {name}: {level}')
                else:
                    print("No text found")
                # cv2.waitKey(0)
                
    cv2.imshow("partial_frame", frame)


# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")
while cap.isOpened():
    success, image = cap.read()
    curr_frame += 1
    if (curr_frame % 30 == 0):
        curr_second += 1
        print(f'Second: {curr_second}')
        processFrame(image)
        if cv2.waitKey(1) == ord('q'):
            break
    # if (success):
    #     processFrame(image)
    if not success:
        break
cv2.destroyAllWindows()



