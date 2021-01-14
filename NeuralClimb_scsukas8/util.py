#Utility file with convenient functions

import matplotlib as plt
import cv2 as cv
from PIL import Image
import tkinter as tk
from tkinter import constants, filedialog


def openFile():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

def openImage(file_path=None):
    # If no file path given, open dialog
    if file_path is None:
        file_path = openFile()
    
    # If stil no file path chosen, quit
    if file_path == None:
        return None

    image = cv2imread(file_path,1)
    return image

def resize(image, y = 0, x = 0):
    if y == 0:
        return image
    if x == 0:
        r, c, _ = image.shape
        x = y * c / r;
    image = cv.resize(image, (y,x))
    return image