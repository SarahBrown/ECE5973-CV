import PySimpleGUI as sg
from cv2 import cv2
import numpy as np
import imutils
import pytesseract
import statistics

configd6 = '--oem 3 --psm 6 outputbase digits -c tessedit_char_whitelist=123456'

def filter(img):
    imgReturn = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgReturn = cv2.medianBlur(imgReturn,3)
    imgReturn = cv2.GaussianBlur(imgReturn,(3,3),5)
    imgCanny = cv2.Canny(imgReturn, 0, 255,(7,7))
    imgReturn = cv2.GaussianBlur(imgCanny,(5,5),5)

    return(imgReturn, imgCanny)


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

def dieText(img):
    dieShape = ''
    mask = np.zeros(img.shape[:2], dtype="uint8")
    process_img, process_canny = filter(img)

    cnts = cv2.findContours(process_img.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for cnt in cnts:
        if cv2.arcLength(cnt,False) > 500:
            accuracy = 0.03*cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt, accuracy, True)
            dieShape=detectShape(approx) 

            cv2.drawContours(mask,[approx],-1,(255,255,255),15)


    maskNot = cv2.bitwise_not(mask)
    masked = cv2.bitwise_and(process_canny, process_canny, mask=maskNot)
    masked = cv2.dilate(masked, (3,3), iterations=2)
    masked = cv2.GaussianBlur(masked,(3,3),5)
    masked = 255 - masked

    masked_text = pytesseract.image_to_string(masked, config=configd6)
    return(masked_text, dieShape)

def main():
    sg.theme("LightGreen")
    layout = [
        [sg.Image(filename="", key="-IMAGE-")],
        [sg.Button("Roll", size=(10, 1), key="-ROLL-")],
        [[sg.Text("", size=(60, 1), justification="left", key="-c-")],
        [sg.Text("", size=(60, 1), justification="left", key="-shape-")]],
        [sg.Button("Exit", size=(10, 1))],
    ]

    window = sg.Window("OpenCV Final Project", layout, location=(800, 400))

    cap = cv2.VideoCapture(2)

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
            window["-shape-"].update((shapes[0]))


        imgbytes = cv2.imencode(".png", frame)[1].tobytes()

        window["-IMAGE-"].update(data=imgbytes)


    window.close()


main()