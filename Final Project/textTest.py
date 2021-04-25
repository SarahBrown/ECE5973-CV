from cv2 import cv2
import numpy as np
import imutils
import pytesseract

config = "--psm 10"

img = cv2.imread("/home/stars/Documents/CV/Final Project/testPics/test (17).jpg")
#resized = cv2.resize(img, (0,0), fx=0.25, fy=0.25) 
resized = img
mask = np.zeros(img.shape[:2], dtype="uint8")


imgGray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
imgNoise = cv2.medianBlur(imgGray,3)
imgBlur = cv2.GaussianBlur(imgNoise,(3,3),0)
imgCanny = cv2.Canny(imgBlur, 0, 255)

# adaptive_threshold = cv2.adaptiveThreshold(imgCanny, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85,11)
#adaptive_threshold = cv2.Canny(adaptive_threshold, 0, 255)


cv2.imshow("canny", imgCanny)
# text = pytesseract.image_to_string(imgCanny, config=config)
# print(text)

# cv2.imshow("thresh", adaptive_threshold)
# text2 = pytesseract.image_to_string(adaptive_threshold, config=config)
# print(text2)

cnts = cv2.findContours(imgCanny.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

firstPass = imgCanny.copy()

for cnt in cnts:
    if cv2.arcLength(cnt,False) > 0:
        cv2.drawContours(mask, [cnt], -1, (255,255,255),3)

        
cv2.imshow("mask", mask)
maskNot = cv2.bitwise_not(mask)
cv2.imshow("maskNot", maskNot)
masked = cv2.bitwise_and(firstPass, firstPass, mask=maskNot)
cv2.imshow("masked",masked)

text3 = pytesseract.image_to_string(masked, config=config)
print(text3)


cv2.waitKey(0)
cv2.destroyAllWindows