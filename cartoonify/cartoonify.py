import cv2
import easygui
import numpy as np
import imageio
import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk


def upload(): 
    ImagePath = easygui.fileopenbox()
    cartoonify(ImagePath)
    
def cartoonify(ImagePath):
    originalImage = cv2.imread(ImagePath)
    originalImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2rgb)
    
    if originalImage is None:
        print ("No original image")
        sys.exit()
        
    Resized1 = cv2.resize(originalImage, (960, 540))
    
    grayScalImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2gray)
    Resized2 =  cv2.resize(grayScalImage, (960, 540))
    smoothGrayScalImage = cv2.medianBlur(grayScalImage, 5)
    Resized3 = cv2.resize(smoothgrayScalImage, (960,540))
    
    getEdge = cv2.adaptiveThreshold(smoothGrayScalImage, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    RESIZED4 = cv2.resize(getEdge, (960, 540))
    
    colorImage = cv2.bilateralFilter(originalImage, 9, 300, 300)
    Resized5 = cv2.resize(colorImage, (960, 540))
    
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)
    Resized6 = cv2.resize(cartoonImage, (960, 540))
    
    images=[Resized1,Resized2,Resized3,Resized4,Resized5,Resized6]
    fig, axes = plt.subplots(3,2 , figsize=(8,8), subplot_kw = {'xticks': [], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')
        
    plt.show()
    
    def save(Resized6, ImagePath):
        newname = "cartoonified_Image"
        path1 = os.path.dirname(ImagePath)
        extensions = os.path.splitext(ImagePath)[1]
        path2 = os.path.join(path1, newname + extensions)
        cv2.imwrite(path, cv2.cvtColor(Resized6, cv2.COLOR_RGB2BGR))
        I = "Image saved by name" + newname + "at " + path
        tk.messageBox.showinfo(title=None, message=I)
        