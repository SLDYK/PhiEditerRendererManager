# -*- coding: utf-8 -*-
import json
import cv2
import numpy
import random
import tkinter
from tkinter import messagebox
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageTk, ImageFilter, ImageEnhance

def Trim(img,hight,width):
    scale=hight/width
    imgscale=img.height/img.width
    if scale>=imgscale:
        start=int((img.width-(img.height/scale))/2)
        end=int(start+(img.height/scale))
        Tr=img.crop((start,0,end,img.height))
    else:
        start=int((img.height-(img.width*scale))/2)
        end=int(start+(img.width*scale))
        Tr=img.crop((0,start,img.width,end))
    Tr=Tr.resize((width,hight))
    
    return Tr

def Blur_background(img,hight,width,Blur):
    Tr=Trim(img,hight,width)
    Tr=Tr.filter(ImageFilter.GaussianBlur(radius=Blur*hight/1080))
    Tr=ImageChops.multiply(Tr,Image.new("RGBA",(Tr.width,Tr.height),(200,200,200,255)))
    Tr = ImageEnhance.Brightness(Tr).enhance(0.55) #亮度调整
    return Tr

def Parallel(img):
    Pic_rot=img.rotate(15,expand=True)
    gauge1=int(img.height*numpy.sin(numpy.pi/12))
    gauge2=Pic_rot.width-gauge1
    cut1=Pic_rot.crop((gauge1,0,gauge2,Pic_rot.height))
    Pic_rotback=cut1.rotate(-15,expand=True)
    gauge3=int(Pic_rotback.height/2-img.height/2)
    gauge4=Pic_rotback.height-gauge3
    final=Pic_rotback.crop((0,gauge3,Pic_rotback.width,gauge4))
    return final
    
    
hight=3840
width=2160
fps=60
Blur=70

songName="Pseudosphere"
level="IN Lv.14"

fontpath="Source/Source Han Sans & Saira Hybrid-Regular.ttf"
shadow="Source/shadow.png"

Picwidth=int(0.5*width)
Pichight=int(Picwidth*1240/1980)

img=Image.open("test.png").convert("RGBA")
shadow=Image.open(shadow).convert("RGBA")

shadow=shadow.resize((img.width,img.height))
img=ImageChops.multiply(img,shadow)


Picture=Blur_background(img,hight,width,Blur)
Illustrate=Parallel(Trim(img,Pichight,Picwidth))

text_font=ImageFont.truetype(fontpath,int(Illustrate.height/10))
level_font=ImageFont.truetype(fontpath, int(Illustrate.height/25))

draw=ImageDraw.Draw(Illustrate)

title=text_font.getsize(songName)
draw.text((int(Illustrate.width/20),int(Illustrate.height-Illustrate.height/25-title[1])),songName,font=text_font,fill=(255,255,255))
title=level_font.getsize(level)
draw.text((int(Illustrate.width-Illustrate.width/5.5-title[0]),int(Illustrate.height-Illustrate.height/25-title[1])),level,font=level_font,fill=(255,255,255))

Illustrate.show()























