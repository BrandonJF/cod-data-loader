import cv2
import numpy as np
def on_trackbar(val):
    global ksize
    ksize = val

img = cv2.imread("cod_data_loader/res/haystack_inventory_slice2.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ksize = 0
cv2.namedWindow("image")
cv2.createTrackbar("Kernel size", "image", ksize, 15, on_trackbar)

while True:
    ksize = cv2.getTrackbarPos("Kernel size", "image")
    if ksize % 2 == 0:
        ksize += 1
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
    abs_sobel64f = np.absolute(sobelx)
    sobel_8u = np.uint8(abs_sobel64f)

    # Find the contours in the image
    contours, _ = cv2.findContours(sobel_8u, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding boxes around the contours
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        if h >= img.shape[0]/2:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

    cv2.imshow("image", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()




