import PySimpleGUI as sg
from cv2 import cv2
import numpy as np
import imutils
import pytesseract
import statistics

configd4 = '--oem 3 --psm 6 outputbase digits -c tessedit_char_whitelist=1234'
configd6 = '--oem 3 --psm 6 outputbase digits -c tessedit_char_whitelist=123456'
configd8 = '--oem 3 --psm 6 outputbase digits -c tessedit_char_whitelist=12345678'
configMisc = '--oem 3 --psm 6 outputbase digits -c tessedit_char_whitelist=0123456789'

CAMERA = 2

def filter(img):
    imgReturn = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgReturn = cv2.medianBlur(imgReturn,3)
    imgReturn = cv2.GaussianBlur(imgReturn,(3,3),5)
    imgCanny = cv2.Canny(imgReturn, 0, 255,(7,7))
    imgReturn = cv2.GaussianBlur(imgCanny,(5,5),5)

    return(imgReturn, imgCanny)

def detectShape(process_img):
    shape = 'unknown'; sides = None 
    mask = np.zeros(process_img.shape[:2], dtype="uint8")

    cnts = cv2.findContours(process_img.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for cnt in cnts:
        if cv2.arcLength(cnt,False) > 500:
            accuracy = 0.02*cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt, accuracy, True)
            sides = len(approx) 

            cv2.drawContours(mask,[approx],-1,(255,255,255),15)
            
    if (sides == 3): 
        shape='d4' 
    elif(sides==4): 
        shape='d6'
    elif(sides==7): 
        shape='d12' 
    else:
        shape='circle' 

    return shape, mask

def detectTextd4(img, mask):
    maskNot = cv2.bitwise_not(mask)
    masked = cv2.bitwise_and(img, img, mask=maskNot)
    masked = cv2.dilate(masked, (3,3), iterations=2)
    masked = cv2.GaussianBlur(masked,(3,3),5)
    masked = 255 - masked

    masked_text = pytesseract.image_to_string(masked, config=configd4)
    return(masked_text)

def detectTextd6(img, mask):
    maskNot = cv2.bitwise_not(mask)
    masked = cv2.bitwise_and(img, img, mask=maskNot)
    masked = cv2.dilate(masked, (3,3), iterations=2)
    masked = cv2.GaussianBlur(masked,(3,3),5)
    masked = 255 - masked

    masked_text = pytesseract.image_to_string(masked, config=configd6)
    return(masked_text)

def detectTextd8(img, mask):
    maskNot = cv2.bitwise_not(mask)
    masked = cv2.bitwise_and(img, img, mask=maskNot)
    masked = cv2.dilate(masked, (3,3), iterations=2)
    masked = cv2.GaussianBlur(masked,(3,3),5)
    masked = 255 - masked

    masked_text = pytesseract.image_to_string(masked, config=configd8)
    return(masked_text)

def detectTextMisc(img, mask):
    maskNot = cv2.bitwise_not(mask)
    masked = cv2.bitwise_and(img, img, mask=maskNot)
    masked = cv2.dilate(masked, (3,3), iterations=2)
    masked = cv2.GaussianBlur(masked,(3,3),5)
    masked = 255 - masked

    masked_text = pytesseract.image_to_string(masked, config=configMisc)
    return(masked_text)

def createWindow():
    sg.theme("LightGreen")
    # Define the window layout
    layout = [
        [sg.Image(filename="", key="-IMAGE-")],
        [sg.Button("Roll", size=(10, 1), key="-ROLL-")],
        [[sg.Text("", size=(60, 1), justification="left", key="-c-")],
        [sg.Text("", size=(60, 1), justification="left", key="-shape-")]],
        [sg.Button("Exit", size=(10, 1))],
    ]

    # Create the window and show it
    window = sg.Window("OpenCV Final Project", layout, location=(800, 400))
    return window

def main():
    window = createWindow()

    cap = cv2.VideoCapture(CAMERA)

    while True:
        event, values = window.read(timeout=20)

        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        ret, frame = cap.read()

        if event == "-ROLL-":
            dice_value = None; die_shape = ''; dice_values = []; shapes = []

            for i in range(10):
                process_img, process_canny = filter(frame)
                die_shape, mask = detectShape(process_img)
                print(die_shape)
                if(die_shape == 'd4'):
                   dice_value = detectTextd4(process_canny, mask)
                elif (die_shape == 'd6'):
                    dice_value = detectTextd6(process_canny, mask)
                elif(die_shape == 'd8'):
                    dice_value = detectTextd8(process_canny, mask)
                else:
                    dice_value = detectTextMisc(process_canny, mask)

                shapes.append(die_shape)
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