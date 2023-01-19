import cv2 as cv
def showimage(vis):
    cv.imshow('img', vis)
    if cv.waitKey(0) == 9:
        cv.destroyAllWindows()