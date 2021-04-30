import PySimpleGUI as sg
from cv2 import cv2
import numpy as np
import imutils
import pytesseract
import statistics

configd6 = '--oem 3 --psm 6 outputbase digits -c tessedit_char_whitelist=123456'
#config = '--psm 6'


def filter(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgNoise = cv2.medianBlur(imgGray,3) #was 3, better with 5?
    imgBlur = cv2.GaussianBlur(imgNoise,(5,5),0) #was(5,5),0, better with (5,5),3
    imgCanny = cv2.Canny(imgBlur, 0, 255,(7,7))
    return(imgCanny)

def detectShape(c):          
       shape = 'unknown' 
       peri=cv2.arcLength(c,True) 
       vertices = cv2.approxPolyDP(c, 0.02 * peri, True)
       sides = len(vertices) 
       #print(sides)
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

def dieText(img):
    dieShape = ''
    mask = np.zeros(img.shape[:2], dtype="uint8")
    process_img = filter(img)

    cnts = cv2.findContours(process_img.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    firstPass = process_img.copy()

    for cnt in cnts:
        if cv2.arcLength(cnt,False) > 500:
            accuracy = 0.03*cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt, accuracy, True)
            dieShape=detectShape(approx) 

            # moment=cv2.moments(approx) 
            # if moment["m00"] != 0:
            #     cx = int(moment['m10'] / moment['m00']) 
            #     cy = int(moment['m01'] / moment['m00'])
            # else:
            #     cx = 0
            #     cy = 0
            
            #mask = cv2.circle(mask, (cx,cy), 30, (255,255,255), -1)
            cv2.drawContours(mask,[approx],-1,(255,255,255),15) #this one
            #cv2.drawContours(mask, [cnt], -1, (255,255,255),5)

    maskNot = cv2.bitwise_not(mask)
    masked = cv2.bitwise_and(firstPass, firstPass, mask=maskNot)
    masked = cv2.dilate(masked, (9,9))
    masked = 255 - masked

    masked_text = pytesseract.image_to_string(masked, config=configd6)
    #process_img_text = pytesseract.image_to_string(process_img, config=configd6)
    return(masked_text, dieShape)

def main():
    sg.theme("LightGreen")
    # Define the window layout
    layout = [
        [sg.Image(filename="", key="-IMAGE-")],
        [sg.Button("Roll", size=(10, 1), key="-ROLL-")],
        [sg.Text("", size=(60, 1), justification="center", key="-c-")],
        [sg.Button("Exit", size=(10, 1))],
    ]


    # Create the window and show it without the plot
    window = sg.Window("OpenCV Final Project", layout, location=(800, 400))

    cap = cv2.VideoCapture(0)

    while True:
        event, values = window.read(timeout=20)

        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        ret, frame = cap.read()

        if event == "-ROLL-":
            dice_value = None
            shape = ''
            dice_values = []
            shapes = []
            # while ((dice_value == None)):
            #     dice_value = dieText(frame)
            #     ret, frame = cap.read()
            #     print("rolling")

            for i in range(10):
                dice_value, shape = dieText(frame)
                shapes.append(shape)
                print(dice_value)
                if (dice_value != '\x0c'):
                    dice_values.append(int(dice_value[:2]))
                ret, frame = cap.read()
            print(dice_values)
            print(shapes)
            if (len(dice_values) > 0):
                dice_value = statistics.mode(dice_values)
            print(dice_value)
            window["-c-"].update((dice_value))


        imgbytes = cv2.imencode(".png", frame)[1].tobytes()

        window["-IMAGE-"].update(data=imgbytes)


    window.close()


main()