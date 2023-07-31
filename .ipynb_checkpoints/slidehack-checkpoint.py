print("hello")
import matplotlib.pyplot as plt
import pandas as pd
from pprint import pprint
import PySimpleGUI as sg
import cv2
from PIL import Image

picturewidth = 1000
pictureheight = 1000

finalwidth = 5000
finalheight = 5000


ospath = r'c:\Users\cmv025\Documents\openslide-win64-20230414\bin'

import os
print(os.listdir(ospath))
with os.add_dll_directory(ospath):
        import openslide


slidepath = r'Z:\3Dhistech\POROKERATOSIS VRRUCOUS DP19-13251.mrxs'
        
slide = openslide.OpenSlide(slidepath)

#print(slide.dimensions)
#print(slide.level_count)
#print(slide.level_dimensions)
#pprint(dict(slide.properties))
slidedict = dict(slide.properties)

regionx:float = 0.0
regiony:float = 0.0
previewlevel:int = 5
step = 1000
fullwidth = int( slidedict["openslide.level[5].width"])
fullheight =int( slidedict["openslide.level[5].height"])
fullsample =int( slidedict["openslide.level[5].downsample"])
fullratio = fullwidth / fullheight

rotate = 0

regionxs:float = 0.0
regionys:float = 0.0

zerowidth = int( slidedict["openslide.level[0].width"])
zeroheight = int( slidedict["openslide.level[0].height"])

filename = './current.png'

elements = [
       # [sg.Image(key="-IMAGE-", filename=filename)],
        [
            sg.Input(size=(25, 1), key="-STEP-"),
            sg.Button("Rotate")
        ], [
              sg.Button("Photo")  ],
    ]

window = sg.Window("Image Viewer", elements, keep_on_top=True )

def click_event(event, x, y, flags, params):
        global regionx, regiony
# checking for left mouse clicks
        if event == cv2.EVENT_LBUTTONDOWN:
                print(x, ' ', y)
                regionx = x / (400  * fullratio  )
                regiony = y /400

                fullImg = cv2.imread('full.png')

                fullImg = cv2.rectangle(fullImg,
                                        (x, y),
                                        (x + int(200 * picturewidth / fullwidth),
                                         y + int(200 * picturewidth / fullwidth)),
                                        (255, 0, 0),
                                        5)
                
                cv2.imshow('map', fullImg)
                
                update()

def click_event_second(event, x, y, flags, params):
        global regionx, regiony, regionxs, regionys
        if event == cv2.EVENT_LBUTTONDOWN:
                print(x, ' ', y)
                regionxs = x / picturewidth
                regionys = y /pictureheight
                print(regionxs, ' ', regionys)

                img = cv2.imread('compare.jpg', 1)
                img = cv2.rectangle(img,
                                        (x , y ),
                                        (x + int(picturewidth / 4), y + int( picturewidth / 4)),
                                        (255, 0, 0),
                                        5)
                
                cv2.imshow('preview', img)
                
                updates()

def getfull():
        global regionx, regiony
        print("fetching..." )
        region = (int(regionx * zerowidth), int(regiony * zeroheight))
        print(region)
        level = previewlevel - 2
        size = (picturewidth * 4 * 2, pictureheight * 4 * 2)
        region = slide.read_region(region, level, size)
        region = region.rotate(rotate, resample=Image.BICUBIC)
        region = region.crop((picturewidth * 2 , pictureheight * 2 , int(6 * picturewidth), int(6 * pictureheight) ))
        
        jp = region.convert("RGB")
        jp.save("full.jpg")
        print("done")

        #img = cv2.imread('currentthumb.png', 1)
        #cv2.imshow('image', img)


basex = 0
basey = 0
def update():
        global regionx, regiony, basex, basey
        print("fetching large..." )
        x = int( regionx * zerowidth) - int( picturewidth * float(2 ** int(previewlevel )) / 2 )
        y = int(regiony * zeroheight) - int( picturewidth * float(2 ** int(previewlevel )) / 2)
        basex = int( regionx * zerowidth)
        basey = int(regiony * zeroheight)
        region = (x,y)
        print(region)
        level = previewlevel
        size = (picturewidth * 2, pictureheight * 2)
        region = slide.read_region(region, level, size)
        region = region.rotate(rotate, resample=Image.BICUBIC)
        region = region.crop((picturewidth / 2, pictureheight / 2, int(1.5 * picturewidth), int(1.5 * pictureheight) ))
        
        jp = region.convert("RGB")
        jp.save("large.jpg")
        print("done")
        #window["-IMAGE-"].update(filename="./current.png")
        img = cv2.imread('large.jpg', 1)
        cv2.imshow('large', img)
        cv2.setMouseCallback('large', click_event_second)
         
def updates():
        global regionx, regiony, regionxs, regionys, basex, basey
        print("fetching small..." )
        zeropdim = picturewidth * float(2 ** int(previewlevel  ))
        smallerx = int( regionxs * zeropdim) 
        smallery = int( regionys * zeropdim) 
        region = (basex + smallerx - int(zeropdim / 8),
                  basey + smallery - int(zeropdim / 8))
        
        level = previewlevel - 2
        size = (picturewidth * 2, pictureheight * 2)
        region = slide.read_region(region, level, size)
        region = region.rotate(rotate, resample=Image.BICUBIC)
        region = region.crop((picturewidth / 2, pictureheight / 2, int(1.5 * picturewidth), int(1.5 * pictureheight) ))
        
        jp = region.convert("RGB")
        jp.save("small.jpg")
        print("done")
        img = cv2.imread('small.jpg', 1)
        
        cv2.imshow('previews', img)

def rotate_large():
        
        img = cv2.imread('large.jpg', 1)
        img = img.rotate(rotate)
        cv2.imshow('large', img)


fulregion = slide.read_region((0,0), 5, (fullwidth, fullheight))
fulregion.thumbnail((400, 400))
fulregion.save('full.png')
fullImg = cv2.imread('full.png')
cv2.imshow('map', fullImg)
cv2.setMouseCallback('map', click_event)

# Create an event loop
while True:
        event, values = window.read()
        if event == "OK" or event == sg.WIN_CLOSED:
                break
        elif event == "Rotate":
            stepnow = values["-STEP-"]
            rotate = int(stepnow)
            update()
        elif event == "Photo":
                getfull()

window.close()
