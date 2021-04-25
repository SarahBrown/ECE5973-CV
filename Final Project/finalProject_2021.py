from cv2 import cv2
import numpy as np
import imutils
import pytesseract
import PySimpleGUI as sg

config = '--oem 3 --psm 6 outputbase digits'

def nothing(x):
    pass

sg.Window(title="Hello World", layout=[[]], margins=(100,50)).read()