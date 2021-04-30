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

def filter(img):

def detectShape(cnt):

def detectTextd4():

def detectTextd6():

def detectTextd8():

def detectTextMisc():

main():

main()