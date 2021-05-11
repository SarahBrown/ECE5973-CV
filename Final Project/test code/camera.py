from cv2 import cv2
import numpy as np

cap = cv2.VideoCapture(2)

def nothing(x):
    pass

if not (cap.isOpened()):
    print('Could not open video device')

window_name='camera'

cv2.namedWindow(window_name,cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(window_name,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

# create trackbars for color change
cv2.createTrackbar('HMin',window_name,0,179,nothing) # Hue is from 0-179 for Opencv
cv2.createTrackbar('SMin',window_name,0,255,nothing)
cv2.createTrackbar('VMin',window_name,0,255,nothing)
cv2.createTrackbar('HMax',window_name,0,179,nothing)
cv2.createTrackbar('SMax',window_name,0,255,nothing)
cv2.createTrackbar('VMax',window_name,0,255,nothing)

# Set default value for MAX HSV trackbars.
cv2.setTrackbarPos('HMax', window_name, 179)
cv2.setTrackbarPos('SMax', window_name, 255)
cv2.setTrackbarPos('VMax', window_name, 255)

# Initialize to check if HSV min/max value changes
hMin = sMin = vMin = hMax = sMax = vMax = 0
phMin = psMin = pvMin = phMax = psMax = pvMax = 0

while (True):
    ret, frame = cap.read()

     # get current positions of all trackbars
    hMin = cv2.getTrackbarPos('HMin',window_name)
    sMin = cv2.getTrackbarPos('SMin',window_name)
    vMin = cv2.getTrackbarPos('VMin',window_name)

    hMax = cv2.getTrackbarPos('HMax',window_name)
    sMax = cv2.getTrackbarPos('SMax',window_name)
    vMax = cv2.getTrackbarPos('VMax',window_name)

    # Set minimum and max HSV values to display
    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])

    # Create HSV Image and threshold into a range.
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    output = cv2.bitwise_and(frame,frame, mask= mask)

    if( (phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax) ):
        print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (hMin , sMin , vMin, hMax, sMax , vMax))
        phMin = hMin
        psMin = sMin
        pvMin = vMin
        phMax = hMax
        psMax = sMax
        pvMax = vMax

    cv2.imshow(window_name,output)
    if cv2.waitKey(1) & 0xFF == ord('q'): # btw, you need to click the screen first. And then 
                                         # press q to quit
        break
        
cap.release()
cv2.destroyAllWindows()