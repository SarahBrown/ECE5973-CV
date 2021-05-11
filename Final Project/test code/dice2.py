from cv2 import cv2
import numpy as np
import imutils

MIN_THRESH = 0
img = cv2.imread("/home/stars/Documents/CV/Final Project/testPics/test (2).jpg")

resized = cv2.resize(img, (0,0), fx=0.25, fy=0.25) 
orig_resized = resized.copy()

cv2.imshow("org",resized)

gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

ret,thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

for c in cnts:
    accuracy = 0.03*cv2.arcLength(c,True)
    approx = cv2.approxPolyDP(c, accuracy, True)
    cv2.drawContours(resized,[approx],0,(0,255,0),2)
    cv2.imshow("approx", resized)
cv2.waitKey(0)
cv2.destroyAllWindows()