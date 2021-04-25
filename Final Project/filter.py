from cv2 import cv2
import numpy as np
import imutils
import pytesseract

img = cv2.imread("/home/stars/Documents/CV/Final Project/testPics/test (17).jpg")
#resized = cv2.resize(img, (0,0), fx=0.25, fy=0.25) 
resized = img

imgGray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
imgNoise = cv2.medianBlur(imgGray,3)
imgBlur = cv2.GaussianBlur(imgNoise,(5,5),0)
imgCanny = cv2.Canny(imgBlur, 0, 255)

cv2.imshow("process", imgCanny)
text = pytesseract.image_to_string(imgCanny)
print(text)

cnts = cv2.findContours(imgCanny.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

ret,thresh = cv2.threshold(imgCanny,200,225,1)
contours,h = cv2.findContours(thresh,1,2)

firstPass = resized.copy()

def detectShape(c):          #Function to determine type of polygon on basis of number of sides
       shape = 'unknown' 
       peri=cv2.arcLength(cnt,True) 
       vertices = cv2.approxPolyDP(cnt, 0.02 * peri, True)
       sides = len(vertices) 
       print(sides)
       if (sides == 3): 
            shape='triangle' 
       elif(sides==4): 
             x,y,w,h=cv2.boundingRect(cnt)
             aspectratio=float(w)/h 
             if (aspectratio==1):
                   shape='d6'
             else:
                   shape="d6" 
       elif(sides==5):
            shape='pentagon' 
       elif(sides==6):
            shape='hexagon' 
       elif(sides==8): 
            shape='d12' 
       else:
           shape='circle' 
       return shape 

for cnt in cnts:
    if cv2.arcLength(cnt,False) > 0 and cv2.arcLength(cnt,False) < 300:
        accuracy = 0.03*cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt, accuracy, True)

        moment=cv2.moments(approx) 
        if moment["m00"] != 0:
            cx = int(moment['m10'] / moment['m00']) 
            cy = int(moment['m01'] / moment['m00'])
        else:
            cx = 0
            cy = 0
        shape=detectShape(approx) 
        cv2.drawContours(resized,[approx],-1,(0,255,0),2)
        cv2.putText(resized,shape,(cx,cy),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)  #Putting name of polygon along with the shape 
        cv2.imshow('polygons_detected',resized) 



cv2.waitKey(0)
cv2.destroyAllWindows