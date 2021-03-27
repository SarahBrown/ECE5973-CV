from cv2 import cv2
import numpy as np
import imutils

MIN_THRESH = 0
img = cv2.imread("test2.png")
kernel = np.ones((5,5),np.uint8)
print(img.shape)
img = img[:,:]

scale_percent = 20 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

imgGray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(resized, (5,5), 0)
imgCanny = cv2.Canny(resized, 125, 200)


cv2.imshow("process", imgCanny)

cnts = cv2.findContours(imgCanny.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

for c in cnts:
    if cv2.arcLength(c,False) > 20:
        cv2.drawContours(img, [c], -1, (0,0,255), 3)
        cv2.imshow("found edges", img)

cv2.waitKey(0)
cv2.destroyAllWindows