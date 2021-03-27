from cv2 import cv2
import numpy as np


img = cv2.imread('/home/stars/Documents/CV/Final Project/testPics/test (2).jpg')
img = cv2.resize(img, (0,0), fx=0.1, fy=0.1) 

lower = np.array([89,0,0])
upper = np.array([179,255,255])

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, lower, upper)

cv2.imshow("mask", mask)

applyMask = cv2.bitwise_and(img, img, mask=mask)
cv2.imshow("masked", applyMask)

gray = cv2.cvtColor(applyMask, cv2.COLOR_BGR2GRAY)
edged = cv2.Canny(gray, 170, 255)

ret,thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

(contours,_) = cv2.findContours(edged,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #Find contours in an image
def detectShape(c):          #Function to determine type of polygon on basis of number of sides
       shape = 'unknown' 
       peri=cv2.arcLength(cnt,True) 
       vertices = cv2.approxPolyDP(cnt, 0.02 * peri, True)
       sides = len(vertices) 
       if (sides == 3): 
            shape='triangle' 
       elif(sides==4): 
             x,y,w,h=cv2.boundingRect(cnt)
             aspectratio=float(w)/h 
             if (aspectratio==1):
                   shape='square'
             else:
                   shape="rectangle" 
       elif(sides==5):
            shape='pentagon' 
       elif(sides==6):
            shape='hexagon' 
       elif(sides==8): 
            shape='octagon' 
       elif(sides==10): 
            shape='star'
       else:
           shape='circle' 
       return shape 
for cnt in contours:
    moment=cv2.moments(cnt) 
    if moment["m00"] != 0:
        cx = int(moment['m10'] / moment['m00']) 
        cy = int(moment['m01'] / moment['m00'])
    else:
        cx = 0
        cy = 0
    shape=detectShape(cnt) 
    cv2.drawContours(img,[cnt],-1,(0,255,0),2)
    cv2.putText(img,shape,(cx,cy),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)  #Putting name of polygon along with the shape 
    cv2.imshow('polygons_detected',img) 
cv2.waitKey(0) 
cv2.destroyAllWindows()