# -*- coding: utf-8 -*-
import json
import cv2
import numpy
import random
import tkinter
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageTk, ImageFilter, ImageEnhance
from tkinter import filedialog
from tkinter import ttk   

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
    


def start(data):
    pass

def end(data):
    
    [songName,level,width,hight,fps,rand_id,APS,totalcombo,Picture_Path,AET]=data
    
    size = (width, hight)
    vidpath = "tmp/"+str(rand_id)+" Animation_2.avi"
    fourcc=cv2.VideoWriter_fourcc(*'XVID')
    videowrite=cv2.VideoWriter(vidpath, fourcc, fps, size)
    
    background=Image.open("tmp/"+str(rand_id)+" UI_3.png").convert("RGBA")
    Picture=Blur_background(Image.open(Picture_Path).convert("RGBA"),hight,width,70)
    
    UI_1=Image.open("tmp/"+str(rand_id)+" UI_1.png").convert("RGBA")
    UI_2=Image.open("tmp/"+str(rand_id)+" UI_2.png").convert("RGBA")
    
    
    num_frames=fps*AET
    #时间轴
    for i in range(num_frames):
        Current=i/fps
        #stage1
        if Current<1:
            alpha = i / fps
            output = Image.blend(background, Picture, alpha)
            output.paste(UI_1,(0,int(Current*hight*(-0.15))),mask=UI_1)
            output.paste(UI_2,(0,int(Current*hight*(0.15))),mask=UI_2)
            
            videowrite.write(cv2.cvtColor(numpy.asarray(output),cv2.COLOR_RGB2BGR))
            
    videowrite.release()

    
    #Animation_data=[songName,level,width,height,fps,rand_id,APS,totalcombo,Picture]
    
    #fontpath="Source/Source Han Sans & Saira Hybrid-Regular.ttf"
    #shadow="Source/shadow.png"
    #初始设置
    #hight=2160
    #width=3840
    #fps=60
    #Blur=70
    #songName="Pseudosphere"
    #level="IN Lv.14"
    
    #rand_id=123
    #long=10
    
    #Picwidth=int(0.5*width)
    #Pichight=int(Picwidth*1240/1980)
    
    #img=Image.open("test.png").convert("RGBA")
    #shadow=Image.open(shadow).convert("RGBA")
    #background=Image.new('RGBA',(width,hight),(0,255,0,255))
    
    
    
    #Picture=Blur_background(img,hight,width,Blur)
    #Illustrate=Parallel(Trim(img,Pichight,Picwidth))
    #shadow=shadow.resize((Illustrate.width,Illustrate.height))
    #Illustrate=ImageChops.multiply(Illustrate,shadow)
    #text_font=ImageFont.truetype(fontpath,int(Illustrate.height/10))
    #level_font=ImageFont.truetype(fontpath, int(Illustrate.height/25))
    
    #draw=ImageDraw.Draw(Illustrate)
    
    #title=text_font.getsize(songName)
    #draw.text((int(Illustrate.width/20),int(Illustrate.height-Illustrate.height/25-title[1])),songName,font=text_font,fill=(255,255,255))
    #title=level_font.getsize(level)
    #draw.text((int(Illustrate.width-Illustrate.width/5.5-title[0]),int(Illustrate.height-Illustrate.height/25-title[1])),level,font=level_font,fill=(255,255,255))
    
    #Illustrate.show()
    #绘制左侧大图
    
    
    #结算动画
    
    
    
    





















