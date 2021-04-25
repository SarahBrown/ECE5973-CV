from cv2 import cv2
import numpy as np
import imutils
import pytesseract

config = '--oem 3 --psm 6 outputbase digits'

def nothing(x):
    pass

def detectShape(c):          
       shape = 'unknown' 
       peri=cv2.arcLength(c,True) 
       vertices = cv2.approxPolyDP(c, 0.02 * peri, True)
       sides = len(vertices) 
       if (sides == 3): 
            shape='d4' 
       elif(sides==4): 
             x,y,w,h=cv2.boundingRect(c)
             aspectratio=float(w)/h 
             if (aspectratio==1):
                   shape='d6'
             else:
                   shape="d6" 
       elif(sides==7): 
            shape='d12' 
       else:
           shape='circle' 
       return shape 

def dieShape(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgNoise = cv2.medianBlur(imgGray,3)
    imgBlur = cv2.GaussianBlur(imgNoise,(3,3),0)
    imgCanny = cv2.Canny(imgBlur, 0, 255)

    cnts = cv2.findContours(imgCanny.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    ret,thresh = cv2.threshold(imgCanny,200,225,1)
    contours,h = cv2.findContours(thresh,1,2)

    firstPass = img.copy()

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
            cv2.drawContours(firstPass,[approx],-1,(0,255,0),2)
            cv2.putText(firstPass,shape,(cx,cy),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)

    return(firstPass)

def dieText(img):
    mask = np.zeros(img.shape[:2], dtype="uint8")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgNoise = cv2.medianBlur(imgGray,3)
    imgBlur = cv2.GaussianBlur(imgNoise,(5,5),0)
    imgCanny = cv2.Canny(imgBlur, 0, 255)

    cnts = cv2.findContours(imgCanny.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    firstPass = imgCanny.copy()

    for cnt in cnts:
        if cv2.arcLength(cnt,False) > 700:
            accuracy = 0.03*cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt, accuracy, True)

            # moment=cv2.moments(approx) 
            # if moment["m00"] != 0:
            #     cx = int(moment['m10'] / moment['m00']) 
            #     cy = int(moment['m01'] / moment['m00'])
            # else:
            #     cx = 0
            #     cy = 0
            # shape=detectShape(approx) 
            cv2.drawContours(mask,[approx],-1,(255,255,255),15)
            #cv2.drawContours(mask, [cnt], -1, (255,255,255),5)

    maskNot = cv2.bitwise_not(mask)
    masked = cv2.bitwise_and(firstPass, firstPass, mask=maskNot)

    text3 = pytesseract.image_to_string(masked, config=config)
    text2 = pytesseract.image_to_string(imgCanny, config=config)
    return(imgCanny, mask, maskNot, masked, text3,text2)

cap = cv2.VideoCapture(2)
#cap.set(15,-4)

if not (cap.isOpened()):
    print('Could not open video device')

window_name='camera'

#cv2.namedWindow(window_name,cv2.WND_PROP_FULLSCREEN)
#cv2.setWindowProperty(window_name,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

while (True):
    ret, frame = cap.read()

    imgCanny, mask, maskNot, frameDie,text,text2 = dieText(frame)
    frameDie = cv2.cvtColor(frameDie, cv2.COLOR_GRAY2BGR)
    imgCanny = cv2.cvtColor(imgCanny, cv2.COLOR_GRAY2BGR)
    hframes = np.hstack((frame,imgCanny, frameDie))
    cv2.imshow(window_name,hframes)
    cv2.imshow("mask", mask)
    print("masked")
    print(text)
    print("imgcanny")
    print(text2)

    if cv2.waitKey(1) & 0xFF == ord('q'): # btw, you need to click the screen first. And then 
                                         # press q to quit
        break
        
cap.release()
cv2.destroyAllWindows()