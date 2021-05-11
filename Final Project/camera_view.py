from cv2 import cv2
import numpy as np
import imutils
import pytesseract

config = '--oem 3 --psm 6 outputbase digits -c tessedit_char_whitelist=123456'

def nothing(x):
    pass

def filter(img):
    imgReturn = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgReturn = cv2.medianBlur(imgReturn,3)
    imgReturn = cv2.GaussianBlur(imgReturn,(3,3),5)
    imgCanny = cv2.Canny(imgReturn, 0, 255,(7,7))
    imgReturn = cv2.GaussianBlur(imgCanny,(5,5),5)

    return(imgReturn, imgCanny)


def dieText(img):
    mask = np.zeros(img.shape[:2], dtype="uint8")
    process_img, process_canny = filter(img)

    cnts = cv2.findContours(process_img.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    firstPass = process_img.copy()

    for cnt in cnts:
        if cv2.arcLength(cnt,False) > 400:
            accuracy = 0.03*cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt, accuracy, True)
            moment=cv2.moments(approx) 
            if moment["m00"] != 0:
                cx = int(moment['m10'] / moment['m00']) 
                cy = int(moment['m01'] / moment['m00'])
            else:
                cx = 0
                cy = 0
            
            #mask = cv2.circle(mask, (cx,cy), 70, (255,255,255), -1)
            #mask = cv2.rectangle(mask, (cx-80,cy-80), (cx+60,cy+60), (255,255,255), -1)
            cv2.drawContours(mask,[approx],-1,(255,255,255),50)

    maskNot = cv2.bitwise_not(mask)
    masked = cv2.bitwise_and(process_canny, process_canny, mask=maskNot)
    #masked = cv2.bitwise_and(process_canny, process_canny, mask=mask) #for when drawing shape on top
    masked = cv2.dilate(masked, (3,3), iterations=2)
    masked = cv2.GaussianBlur(masked,(3,3),5)
    masked = 255 - masked


    masked_text = pytesseract.image_to_string(masked, config=config)
    process_img_text = pytesseract.image_to_string(process_img, config=config)
    return(process_img, masked, process_img_text, masked_text, maskNot)

cap = cv2.VideoCapture(2)

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

    if cv2.waitKey(1) & 0xFF == ord('q'):                
        break
        
cap.release()
cv2.destroyAllWindows()