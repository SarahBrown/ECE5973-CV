from cv2 import cv2
import numpy as np

lower = np.array([67,0,0])
upper = np.array([179,255,255])

img = cv2.imread('/home/stars/Documents/CV/Final Project/testPics/test (2).jpg')
small = cv2.resize(img, (0,0), fx=0.1, fy=0.1) 

imgGray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
# imgGray = cv2.equalizeHist(imgGray)
# # imgGray = cv2.cvtColor(imgGray, cv2.COLOR_GRAY2BGR)

# cv2.imshow('small',imgGray)
# cv2.waitKey(0)

# imgBlur = cv2.GaussianBlur(imgGray, (3,3), 0)
# imgCanny = cv2.Canny(imgBlur,50,225)

# cv2.imshow('small',imgCanny)
# cv2.waitKey(0)

hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, lower, upper)

cv2.imshow('small',mask)
cv2.waitKey(0)

blurred = cv2.GaussianBlur(imgGray, (3,3), 0)

cv2.imshow('small',blurred)
cv2.waitKey(0)

thresh = cv2.threshold(blurred, 175, 200, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

cv2.imshow('small',thresh)
cv2.waitKey(0)


# # ret,thresh = cv2.threshold(gray,200,225,1)

# contours,h = cv2.findContours(thresh,1,2)
# print (len(contours))

# for cnt in contours:
#     approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
#     print (len(approx))
#     if len(approx)==5:
#         print ("pentagon")
#         cv2.drawContours(small,[cnt],0,255,-1)
#     elif len(approx)==3:
#         print ("triangle")
#         cv2.drawContours(small,[cnt],0,(0,255,0),-1)
#     elif len(approx)==4:
#         print ("square")
#         cv2.drawContours(small,[cnt],0,(0,0,255),-1)
#     elif len(approx) == 9:
#         print ("half-circle")
#         cv2.drawContours(small,[cnt],0,(255,255,0),-1)
#     elif len(approx) > 15:
#         print ("circle") 
#         cv2.drawContours(small,[cnt],0,(0,255,255),-1)

# cv2.imshow('small',small)
# cv2.waitKey(0)
cv2.destroyAllWindows()
