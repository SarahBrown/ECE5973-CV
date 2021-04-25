import PySimpleGUI as sg
from cv2 import cv2
import numpy as np
import imutils
import pytesseract

config = '--oem 3 --psm 6 outputbase digits -c tessedit_char_whitelist=0123456789'
#config = '--psm 6'


def filter(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgNoise = cv2.medianBlur(imgGray,3)
    imgBlur = cv2.GaussianBlur(imgNoise,(5,5),0)
    imgCanny = cv2.Canny(imgBlur, 0, 255,(7,7))
    return(imgCanny)


def dieText(img):
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

            cv2.drawContours(mask,[approx],-1,(255,255,255),15)
            #cv2.drawContours(mask, [cnt], -1, (255,255,255),5)

    maskNot = cv2.bitwise_not(mask)
    masked = cv2.bitwise_and(firstPass, firstPass, mask=maskNot)
    masked = cv2.dilate(masked, (9,9))
    masked = 255 - masked

    masked_text = pytesseract.image_to_string(masked, config=config)
    process_img_text = pytesseract.image_to_string(process_img, config=config)
    return(masked_text)

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

    cap = cv2.VideoCapture(2)

    while True:
        event, values = window.read(timeout=20)

        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        ret, frame = cap.read()

        if event == "-ROLL-":
            dice_value = None
            dice_values = []
            # while ((dice_value == None)):
            #     dice_value = dieText(frame)
            #     ret, frame = cap.read()
            #     print("rolling")

            for i in range(10):
                dice_value = dieText(frame)
                dice_values.append((dice_value))
                ret, frame = cap.read()
                print("rolling")
            print(dice_values)
            print(str(dice_values))
            window["-c-"].update((dice_value))


        imgbytes = cv2.imencode(".png", frame)[1].tobytes()

        window["-IMAGE-"].update(data=imgbytes)


    window.close()


main()