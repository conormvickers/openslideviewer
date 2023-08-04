print("hello")

import glymur
import cv2
import numpy as np
from PIL import Image
import time
import os

ospath = r'c:\Users\cmv025\Documents\openslide-win64-20230414\bin'
with os.add_dll_directory(ospath):
        import openslide
# xx = 11
# yy = 5
# col = []
# for j in range( xx - 1, xx + 2, 1):
#         row = []
#         for i in range(yy - 1, yy + 2, 1):
#                 pathim = "tiles/" + str(i) + '_' + str(j) + '_full.jpg'
#                 if os.path.exists(pathim):
#                         a = cv2.imread(pathim)
#                 else:
#                         a =  np.zeros((5000,5000,3), np.uint8)
                        
#                 row.append(a)
#         c = cv2.hconcat(row)
#         col.append(c)
# cc = cv2.vconcat(col)
# cv2.imwrite("normal.jpg", cc)



tic = time.perf_counter()
slidepath = r'Z:\3Dhistech\POROKERATOSIS VRRUCOUS DP19-13251.mrxs'
        
slide = openslide.OpenSlide(slidepath)
slidedict = dict(slide.properties)
fullwidth = int( slidedict["openslide.level[1].width"])
fullheight =int( slidedict["openslide.level[1].height"])

toc = time.perf_counter()

print(f"Slided opened in {toc - tic:0.4f} seconds")

asdf = slide.read_region((0, int(fullheight * 2 / 3)), 
                           1, 
                           (int(fullwidth  /4), int(fullheight  / 4)))

print(f"Buffer collected in {toc - tic:0.4f} seconds")

jp2 = glymur.Jp2k('hundolargest.jp2', data=np.array(asdf), cratios=[100])

print(f"Saved in {toc - tic:0.4f} seconds")

j2kfile = glymur.data.goodstuff()
j2k = glymur.Jp2k("secondlargest.jp2")
print("start load...")
fullres = j2k[::-1, ::-1]
print("done")
print(j2k.shape)
print(fullres.shape)

cv2.imshow("test", fullres)
# cv2.resizeWindow('test', 600,600)

downboi = False
computing = False
def jp2click(event, x, y, flags, params):
       global downboi, computing
       if event == cv2.EVENT_LBUTTONDOWN:
                print("down") 
                downboi = True
       elif event == cv2.EVENT_LBUTTONUP:
              print('up')
              downboi = False
       elif event == cv2.EVENT_MOUSEMOVE:
           if not computing and downboi:
                computing = True
                px = x / fullres.shape[0]
                py = y / fullres.shape[1]
                ipx = int(px * j2k.shape[0])
                ipy = int(py * j2k.shape[1])
                print(str(ipx) + " - " + str(ipy))
                if ipx - 500 < 0 or ipy - 500 < 0:
                        print("low overflow")
                        return 1
                if ipx + 500 > j2k.shape[0] or ipy + 500 > j2k.shape[0]:
                        print("high overflow")
                        return 0
                section = j2k[ipy - 500:ipy + 500, ipx - 500:ipx + 500]
                cv2.imshow("section", section)
                computing = False


cv2.moveWindow('test', 40,30)
cv2.setMouseCallback('test', jp2click)

cv2.waitKey(0)


import matplotlib.pyplot as plt

import pandas as pd
from pprint import pprint
import PySimpleGUI as sg


picturewidth = 1000
pictureheight = 1000

finalwidth = 5000
finalheight = 5000



step = 5000
lowestlvl = 1

slidedict = dict(slide.properties)

regionx:float = 0.0
regiony:float = 0.0
previewlevel:int = 5
fullwidth = int( slidedict["openslide.level[5].width"])
fullheight =int( slidedict["openslide.level[5].height"])
fullsample =int( slidedict["openslide.level[5].downsample"])
fullratio = fullwidth / fullheight

rotate = 0

regionxs:float = 0.0
regionys:float = 0.0

zerowidth = int( slidedict["openslide.level[0].width"])
zeroheight = int( slidedict["openslide.level[0].height"])

chunkswidth = int(zerowidth / (step * pow(2, lowestlvl  )))
chunksheight = int(zeroheight / (step * pow(2, lowestlvl  )))

filename = './current.png'

elements = [
       [sg.Button("New File", key="Browse")],
        [
            sg.Input(size=(25, 1), key="-STEP-"),
            sg.Button("Rotate"), 
            sg.Slider((0, 360), 0, 5, 5, key="slider", enable_events=True )
        ], [
              sg.Button("Photo")  ],
    ]

window = sg.Window("Image Viewer", elements, keep_on_top=True )
mode = "dev"
def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result




def click_event(event, x, y, flags, params):
        global regionx, regiony
# checking for left mouse clicks
        if event == cv2.EVENT_LBUTTONDOWN:
                if mode == "dev":
                        print(x, ' ', y)
                        regionx = x / (400  * fullratio  )
                        regiony = y /400
                        w = chunkswidth
                        h = chunksheight
                        hp = int(h * regiony)
                        wp = int(w * regionx)
                        print(wp)
                        print(hp)
                        display(hp, wp)

                       
                else:
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

                img = cv2.imread('large.jpg', 1)
                img = cv2.rectangle(img,
                                        (x +  int(picturewidth / 2), y  + int(picturewidth / 2) ),
                                        (x +  int(picturewidth / 2) + int(picturewidth / 4), y +  int(picturewidth / 2) + int( picturewidth / 4)),
                                        (255, 0, 0),
                                        5)
                cv2.imwrite('large.jpg', img)
                # cv2.imshow('preview', img)
                rotate_large()
                
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
        
        
        jp = region.convert("RGB")
        jp.save("large.jpg")
        print("done")
        rotate_large()
        cv2.setMouseCallback('large', click_event_second)
        #window["-IMAGE-"].update(filename="./current.png")
        # img = cv2.imread('large.jpg', 1)
        # cv2.imshow('large', img)
        # cv2.setMouseCallback('large', click_event_second)
         
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
        
        region = cv2.imread('large.jpg')
        region = rotate_image(region, rotate)
        region = region[int(picturewidth / 2) :int(1.5 * picturewidth) , int(pictureheight / 2) : int(1.5 * pictureheight) ]
        
        cv2.imshow('large', region)

def showpreview():
        if not os.path.exists("full.png"):
                fulregion = slide.read_region((0,0), 5, (fullwidth, fullheight))
                # fulregion = fulregion.convert('RGB')
                fulregion.thumbnail((400, 400))
                fulregion.save('full.png')
        fff = cv2.imread('full.png')
        cv2.imshow('map', fff)
        cv2.moveWindow('map', 40,30)
        cv2.setMouseCallback('map', click_event)
        

def convert():
        for j in range(0, int(zeroheight / (step * pow(2, lowestlvl  )) + 1)):
                for i in range(0, int(zerowidth / (step * pow(2, lowestlvl ) )) + 1):
                        print(f"starting {j} {i}...")
                        fulregion = slide.read_region((i * step * (1 + lowestlvl), j * step * (1 + lowestlvl)), lowestlvl, (step, step))
                        extrema = fulregion.convert("L").getextrema()
                        if extrema == (0, 0):
                                print("blank section")
                                
                        else:
                                fulregion = fulregion.convert('RGB')
                                fulregion.save("tiles/" + str(i) + '_' + str(j) + '_full.jpg', quality=50)

def display(xx, yy):
       
       col = []
       for j in range( xx - 1, xx + 2, 1):
                row = []
                for i in range(yy - 1, yy + 2, 1):
                        pathim = "tiles/" + str(i) + '_' + str(j) + '_full.jpg'
                        if os.path.exists(pathim):
                               a = cv2.imread(pathim)
                        else:
                               a =  np.zeros((step,step,3), np.uint8)
                               
                        row.append(a)
                c = cv2.hconcat(row)
                col.append(c)
       cc = cv2.vconcat(col)

       cv2.namedWindow('Horizontal', cv2.WINDOW_KEEPRATIO)
       cv2.imshow('Horizontal', cc)

       cv2.resizeWindow("Horizontal", 400, 400)
       cv2.waitKey(0)

def show_controls():
       while True:
        event, values = window.read()
        print(event)
        if event == "OK" or event == sg.WIN_CLOSED:
                break
        elif event == "Rotate":
            stepnow = values["-STEP-"]
            if len(stepnow) > 0:
                
                rotate = int(stepnow)
                update()
        elif event == "Photo":
                getfull()
        elif event == "slider":
                rotate = values["slider"]
                rotate_large()
        elif event == "Browse":
                filename = sg.popup_get_file('Enter the file you wish to process')
                sg.popup('You entered', filename)         

        window.close()

# showpreview()
# show_controls()
# convert()
# Create an event loop

