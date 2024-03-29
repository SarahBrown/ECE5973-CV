from cv2 import cv2
import numpy as np

cap = cv2.VideoCapture(2)
#cap.set(15,-4)

def nothing(x):
    pass

if not (cap.isOpened()):
    print('Could not open video device')

window_name='camera'

cv2.namedWindow(window_name,cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(window_name,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

while (True):
    ret, frame = cap.read()

    imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imgGray = cv2.equalizeHist(imgGray)
    imgBlur = cv2.GaussianBlur(imgGray, (5,5), 0)
    imgCanny = cv2.Canny(imgBlur,240,255)

    # ret,thresh = cv2.threshold(imgGray, 240, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # (contours,_) = cv2.findContours(imgCanny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #Find contours in an image
    # def detectShape(c):          #Function to determine type of polygon on basis of number of sides
    #     shape = 'unknown' 
    #     peri=cv2.arcLength(cnt,True) 
    #     vertices = cv2.approxPolyDP(cnt, 0.02 * peri, True)
    #     sides = len(vertices) 
    #     if (sides == 3): 
    #             shape='triangle' 
    #     elif(sides==4): 
    #             x,y,w,h=cv2.boundingRect(cnt)
    #             aspectratio=float(w)/h 
    #             if (aspectratio==1):
    #                 shape='square'
    #             else:
    #                 shape="rectangle" 
    #     elif(sides==5):
    #             shape='pentagon' 
    #     elif(sides==6):
    #             shape='hexagon' 
    #     elif(sides==8): 
    #             shape='octagon' 
    #     elif(sides==10): 
    #             shape='star'
    #     else:
    #         shape='circle' 
    #     return shape 

    # for cnt in contours:
    #     moment=cv2.moments(cnt) 
    #     if moment["m00"] != 0:
    #         cx = int(moment['m10'] / moment['m00']) 
    #         cy = int(moment['m01'] / moment['m00'])
    #     else:
    #         cx = 0
    #         cy = 0
    #     shape=detectShape(cnt) 
    #     cv2.drawContours(frame,[cnt],-1,(0,255,0),2)
    #     cv2.putText(frame,shape,(cx,cy),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)  #Putting name of polygon along with the shape 
    #     cv2.imshow(window_name,frame) 

    output = imgCanny

    cv2.imshow(window_name,output)
    if cv2.waitKey(1) & 0xFF == ord('q'): # btw, you need to click the screen first. And then 
                                         # press q to quit
        break
        
cap.release()
cv2.destroyAllWindows()