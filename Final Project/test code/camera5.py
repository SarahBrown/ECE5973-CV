from cv2 import cv2
import numpy as np
import imutils
import pytesseract

config = '--oem 3 --psm 6 outputbase digits'

def nothing(x):
    pass

def filter(img):
    imgFilter = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgFilter = cv2.medianBlur(imgFilter,9)
    imgFilter = cv2.GaussianBlur(imgFilter,(5,5),0)
    imgFilter = cv2.Canny(imgFilter, 0, 255,(5,5))
    return(imgFilter)


def dieText(img):
    mask = np.zeros(img.shape[:2], dtype="uint8")
    process_img = filter(img)

    cnts = cv2.findContours(process_img.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    firstPass = process_img.copy()

    for cnt in cnts:
        if cv2.arcLength(cnt,False) > 450:
            accuracy = 0.03*cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt, accuracy, True)
            moment=cv2.moments(approx) 
            if moment["m00"] != 0:
                cx = int(moment['m10'] / moment['m00']) 
                cy = int(moment['m01'] / moment['m00'])
            else:
                cx = 0
                cy = 0
            
            #mask = cv2.circle(mask, (cx,cy), 60, (255,255,255), -1)
            cv2.drawContours(mask,[approx],-1,(255,255,255),15) #this one
            #cv2.drawContours(mask, [cnt], -1, (255,255,255),5)

    maskNot = cv2.bitwise_not(mask)
    masked = cv2.bitwise_and(firstPass, firstPass, mask=maskNot)
    masked = cv2.dilate(masked, (11,11))
    masked = 255 - masked

    masked_text = pytesseract.image_to_string(masked, config=config)
    process_img_text = pytesseract.image_to_string(process_img, config=config)
    return(process_img, masked, process_img_text, masked_text, mask)

cap = cv2.VideoCapture(0)
#cap.set(15,-4)

if not (cap.isOpened()):
    print('Could not open video device')

window_name='camera'

while (True):
    ret, frame = cap.read()

    img_canny, img_masked, text_canny, text_mask, mask = dieText(frame)

    img_masked = cv2.cvtColor(img_masked, cv2.COLOR_GRAY2BGR)
    img_canny = cv2.cvtColor(img_canny, cv2.COLOR_GRAY2BGR)
    hframes = np.hstack((frame,img_canny, img_masked))

    cv2.imshow(window_name,hframes)
    cv2.imshow("mask", mask)

    print("masked")
    print(text_mask)
    print("imgcanny")
    print(text_canny)

    if cv2.waitKey(1) & 0xFF == ord('q'): # btw, you need to click the screen first. And then 
                                         # press q to quit
        break
        
cap.release()
cv2.destroyAllWindows()