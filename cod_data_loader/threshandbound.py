import cv2

# Load image
image = cv2.imread("cod_data_loader/res/haystack_inventory_slice1.png")


# Convert image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Define global threshold variable
threshold = 25

def update(val):
    copy = image.copy()
    global threshold
    threshold = val
    # Find areas of image above threshold
    _, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding boxes around areas above threshold
    MIN_CONTROUR_AREA = 2000
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > MIN_CONTROUR_AREA:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(copy, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Show image
    cv2.imshow("Image", copy)

# Create trackbar
cv2.namedWindow("Image")
cv2.createTrackbar("Threshold", "Image", threshold, 255, update)

# Show image
# cv2.imshow("Image", image)
update(25)
cv2.waitKey(0)
cv2.destroyAllWindows()