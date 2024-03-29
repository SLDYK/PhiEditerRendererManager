# -*- coding: utf-8 -*-
import json
import contextlib
import wave
import cv2
import os
import numpy
import random
import tkinter

from win10toast_click import ToastNotifier

from tkinter import messagebox
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageTk, ImageEnhance
from lib_for_video import Trim, f2b, b2f, cut, present_floor, end_floor, score3
from lib_for_video import holdhead_fix, holdend_fix, speed_fix, score, score2
from lib_for_video import paste_hold_pos, paste_pos, effect_pos, p4
from lib_for_video import mkdir, linepos, process_video
from lib_for_audio import audio2wav, PhiAudio, video_add_audio, merge_videos
from lib_for_json import cut2
from pec2json import pec2json
import Animation

def start_rendering(Base_Data,Superior_Data):#主程序

    showframe=tkinter.Toplevel()
    showframe.title("Preview(240p)")
    showframe.geometry("400x300")
    showframe.iconbitmap("Source/R.ico")
    
    var=tkinter.StringVar()
    rand_id=random.randint(100000000,695269639)
    
    pace=tkinter.Label(showframe, textvariable=var,font=('', 10),width=300, height=5)
    pace.place(x=200,y=40,anchor=tkinter.CENTER)
    #生成随机id，防止tmp文件夹互相覆盖
    
    songName,level,width,height,fps,chartPath,Picture,audioPath,HighLight,Blur,noteSize,LineColor,sound_Level=Base_Data
    
    Back_Video_Path=Superior_Data[5]
    BV=False
    
    Combo_text=Superior_Data[3]
    
    DynamicScore=Superior_Data[9]
    
    var.set("正在转换音频格式")
    showframe.update()
    
    hitsoundoffset = 25
    combo_this_frame = 0
    score_this_frame = 0
    chart = {}
    
    
    mkdir("tmp")
    audio2wav(audioPath,str(rand_id))
    showframe.update()

    audioPath ="tmp/"+str(rand_id)+" Song.wav"
    
    with contextlib.closing(wave.open(audioPath, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        length = frames / float(rate)
        f.close()
    
    background = Trim(Image.open(Picture).convert("RGBA"), height, width,Blur)
    
    size = (width, height)
    
    fontpath = "Source/Source Han Sans & Saira Hybrid-Regular.ttf"
    text_font = ImageFont.truetype(fontpath, int(39 * height / 1080))
    combo_font1 = ImageFont.truetype(fontpath, int(72 * height / 1080))
    combo_font2 = ImageFont.truetype(fontpath, int(26 * height / 1080))
    score_font = ImageFont.truetype(fontpath, int(55 * height / 1080))
    
    Level_title = text_font.getsize(level)
    Song_title = text_font.getsize(songName)
    title = combo_font2.getsize(Combo_text)
    
    pause = Image.open("Source/Pause.png").convert("RGBA")
    pause = pause.resize((int(pause.width * height / 1080), int(pause.height * height / 1080)))
    ProgressBar=Image.open("Source/ProgressBar.png").convert("RGBA")
    ProgressBar=ProgressBar.resize((int(ProgressBar.width * width/1920), int(ProgressBar.height * width/1920)))
    tap=Image.open("Source/Tap.png").convert("RGBA")
    tap=tap.resize((int(0.2*tap.width*width/1920*noteSize),int(0.2*tap.height*width/1920*noteSize)))
    tapHL=Image.open("Source/TapHL.png").convert("RGBA")
    tapHL=tapHL.resize((int(0.2*tapHL.width*width/1920*noteSize),int(0.2*tapHL.height*width/1920*noteSize)))
    flick=Image.open("Source/Flick.png").convert("RGBA")
    flick=flick.resize((int(0.2*flick.width*width/1920*noteSize),int(0.2*flick.height*width/1920*noteSize)))
    flickHL=Image.open("Source/FlickHL.png").convert("RGBA")
    flickHL=flickHL.resize((int(0.2*flickHL.width*width/1920*noteSize),int(0.2*flickHL.height*width/1920*noteSize)))
    drag=Image.open("Source/Drag.png").convert("RGBA")
    drag=drag.resize((int(0.2*drag.width*width/1920*noteSize),int(0.2*drag.height*width/1920*noteSize)))
    dragHL=Image.open("Source/DragHL.png").convert("RGBA")
    dragHL=dragHL.resize((int(0.2*dragHL.width*width/1920*noteSize),int(0.2*dragHL.height*width/1920*noteSize)))
    hold1=Image.open("Source/HoldHead.png").convert("RGBA")
    hold1=hold1.resize((int(0.2*hold1.width*width/1920*noteSize),int(0.2*hold1.height*width/1920*noteSize)))
    hold1=holdhead_fix(hold1)
    hold1HL=Image.open("Source/HoldHeadHL.png").convert("RGBA")
    hold1HL=hold1HL.resize((int(0.2*hold1HL.width*width/1920*noteSize*1.02),int(0.2*hold1HL.height*width/1920*noteSize)))
    hold1HL=holdhead_fix(hold1HL)
    hold2=Image.open("Source/Hold.png").convert("RGBA")
    hold2=hold2.resize((int(0.2*hold2.width*width/1920*noteSize),int(0.2*hold2.height*width/1920*noteSize)))
    hold2HL=Image.open("Source/HoldHL.png").convert("RGBA")
    hold2HL=hold2HL.resize((int(0.2*hold2HL.width*width/1920*noteSize*1.02),int(0.2*hold2HL.height*width/1920*noteSize)))
    hold3=Image.open("Source/HoldEnd.png").convert("RGBA")
    hold3=hold3.resize((int(0.2*hold3.width*width/1920*noteSize),int(0.2*hold3.height*width/1920*noteSize)))
    hold3=holdend_fix(hold3)
    hit=[Image.open("Source/img-1.png").convert("RGBA"),
        Image.open("Source/img-2.png").convert("RGBA"),
        Image.open("Source/img-3.png").convert("RGBA"),
        Image.open("Source/img-4.png").convert("RGBA"),
        Image.open("Source/img-5.png").convert("RGBA"),
        Image.open("Source/img-6.png").convert("RGBA"),
        Image.open("Source/img-7.png").convert("RGBA"),
        Image.open("Source/img-8.png").convert("RGBA"),
        Image.open("Source/img-9.png").convert("RGBA"),
        Image.open("Source/img-10.png").convert("RGBA"),
        Image.open("Source/img-11.png").convert("RGBA"),
        Image.open("Source/img-12.png").convert("RGBA"),
        Image.open("Source/img-13.png").convert("RGBA"),
        Image.open("Source/img-14.png").convert("RGBA"),
        Image.open("Source/img-15.png").convert("RGBA"),
        Image.open("Source/img-16.png").convert("RGBA"),
        Image.open("Source/img-17.png").convert("RGBA"),
        Image.open("Source/img-18.png").convert("RGBA"),
        Image.open("Source/img-19.png").convert("RGBA"),
        Image.open("Source/img-20.png").convert("RGBA"),
        Image.open("Source/img-21.png").convert("RGBA"),
        Image.open("Source/img-22.png").convert("RGBA"),
        Image.open("Source/img-23.png").convert("RGBA"),
        Image.open("Source/img-24.png").convert("RGBA"),
        Image.open("Source/img-25.png").convert("RGBA"),
        Image.open("Source/img-26.png").convert("RGBA"),
        Image.open("Source/img-27.png").convert("RGBA"),
        Image.open("Source/img-28.png").convert("RGBA"),
        Image.open("Source/img-29.png").convert("RGBA"),
        Image.open("Source/img-30.png").convert("RGBA")]
    color=Image.new("RGBA",(500,500),(223,210,140,255))
    
    if HighLight == False:
        tapHL=tap
        dragHL=drag
        hold1HL=hold1
        hold2HL=hold2
        flickHL=flick
    
    for i in range(len(hit)):
        color=color.resize((hit[i].width,hit[i].height))    
        hit[i]=ImageChops.darker(color,hit[i])
        hit[i]=ImageChops.multiply(hit[i],Image.new("RGBA",(hit[i].width,hit[i].height),(230,230,230,255)))
        hit[i]=hit[i].resize((int(hit[i].width*width/1920*noteSize*1.2),int(hit[i].height*width/1920*noteSize*1.2)))

    
    particle=[]
    particle_length=[]
    particle_alpha=[]
    particle_size=[]
    ease1=18 #粒子位移缓动
    ease2=15 #粒子透明度缓动
    ease3=20 #粒子缩放缓动
    for i in range(30):
        particle_length.append(cut2(0,110,0,29,0,1,ease1,i))
    for i in range(30):
        particle_alpha.append(cut2(0,100,0,29,0,1,ease2,i))
    for i in range(30):
        particle_size.append(cut2(0,80,0,29,0,1,ease3,i))
    #particle_length=[25.603819159562036,35.90109871423002,43.58898943540673,
     #                49.88876515698588,55.27707983925666,59.999999999999986,
      #               64.20453428086074,67.98692684790379,71.4142842854285,
       #              74.53559924999298,77.38791177495933,80.0,
        #             82.39471396205516,84.59051693633013,86.60254037844386,
         #            88.44332774281067,90.1233722306385,91.6515138991168,
          #           93.03523824635242,94.28090415820634,95.39392014169457,
           #          96.37888196533973,97.23968097209881,97.97958971132712,
            #         98.60132971832694,99.10712498212337,99.498743710662,
             #        99.77753031397178,99.94442900376633,100]
    for i in range(30):
        a_particle=Image.new("RGBA",(int(0.5*particle_size[i]*1.1*width/1920),
                                     int(0.5*particle_size[i]*1.1*width/1920)),
                             (223,210,140,int((100-particle_alpha[i])*1.7)))
        particle.append(a_particle)
        
    rotgroup=[]
    for i in range(10):
        r4=[random.randint(0,360),
        random.randint(0,360),
        random.randint(0,360),
        random.randint(0,360)]
        rotgroup.append(r4)
    var.set("谱面文件预处理")
    showframe.update()
    if chartPath[-1]=="c":
        chart=pec2json(chartPath)
        
        BarPerMinute=chart["judgeLineList"][0]["bpm"]
    else:
        with open(chartPath,"r",encoding="utf_8") as t:
            chart=json.load(t)

            try:
                if(chart["formatVersion"] == 1): #解决formatver1的问题
                    for i in range(len(chart["judgeLineList"])):
                        line = chart["judgeLineList"][i]
                        for j in range(len(line["judgeLineMoveEvents"])):
                            chart["judgeLineList"][i]["judgeLineMoveEvents"][j]["start2"] = (chart["judgeLineList"][i]["judgeLineMoveEvents"][j]["start"] % 1e3) / 520
                            chart["judgeLineList"][i]["judgeLineMoveEvents"][j]["end2"] = (chart["judgeLineList"][i]["judgeLineMoveEvents"][j]["end"] % 1e3) / 520
                            chart["judgeLineList"][i]["judgeLineMoveEvents"][j]["start"] = int(chart["judgeLineList"][i]["judgeLineMoveEvents"][j]["start"] / 1000) /880
                            chart["judgeLineList"][i]["judgeLineMoveEvents"][j]["end"] = int(chart["judgeLineList"][i]["judgeLineMoveEvents"][j]["end"] / 1000) /880
                        for j in range(len(line["speedEvents"])):
                            chart["judgeLineList"][i]["speedEvents"][j]["floorPosition"] = 0
            except:
                Exception

            BarPerMinute=chart["judgeLineList"][0]["bpm"]
            for i in range(0,len(chart["judgeLineList"])):
                mult=BarPerMinute/chart["judgeLineList"][i]["bpm"]
                chart["judgeLineList"][i]["bpm"]=BarPerMinute
                for j in range(0,len(chart["judgeLineList"][i]["speedEvents"])):
                    chart["judgeLineList"][i]["speedEvents"][j]["startTime"]=chart["judgeLineList"][i]["speedEvents"][j]["startTime"]*mult
                    chart["judgeLineList"][i]["speedEvents"][j]["endTime"]=chart["judgeLineList"][i]["speedEvents"][j]["endTime"]*mult
                for j in range(0,len(chart["judgeLineList"][i]["notesBelow"])):
                    chart["judgeLineList"][i]["notesBelow"][j]["time"]=chart["judgeLineList"][i]["notesBelow"][j]["time"]*mult
                    chart["judgeLineList"][i]["notesBelow"][j]["holdTime"]=chart["judgeLineList"][i]["notesBelow"][j]["holdTime"]*mult
                for j in range(0,len(chart["judgeLineList"][i]["notesAbove"])):
                    chart["judgeLineList"][i]["notesAbove"][j]["time"]=chart["judgeLineList"][i]["notesAbove"][j]["time"]*mult
                    chart["judgeLineList"][i]["notesAbove"][j]["holdTime"]=chart["judgeLineList"][i]["notesAbove"][j]["holdTime"]*mult
                for j in range(0,len(chart["judgeLineList"][i]["judgeLineDisappearEvents"])):
                    chart["judgeLineList"][i]["judgeLineDisappearEvents"][j]["startTime"]=chart["judgeLineList"][i]["judgeLineDisappearEvents"][j]["startTime"]*mult
                    chart["judgeLineList"][i]["judgeLineDisappearEvents"][j]["endTime"]=chart["judgeLineList"][i]["judgeLineDisappearEvents"][j]["endTime"]*mult
                for j in range(0,len(chart["judgeLineList"][i]["judgeLineMoveEvents"])):
                    chart["judgeLineList"][i]["judgeLineMoveEvents"][j]["startTime"]=chart["judgeLineList"][i]["judgeLineMoveEvents"][j]["startTime"]*mult
                    chart["judgeLineList"][i]["judgeLineMoveEvents"][j]["endTime"]=chart["judgeLineList"][i]["judgeLineMoveEvents"][j]["endTime"]*mult
                for j in range(0,len(chart["judgeLineList"][i]["judgeLineRotateEvents"])):
                    chart["judgeLineList"][i]["judgeLineRotateEvents"][j]["startTime"]=chart["judgeLineList"][i]["judgeLineRotateEvents"][j]["startTime"]*mult
                    chart["judgeLineList"][i]["judgeLineRotateEvents"][j]["endTime"]=chart["judgeLineList"][i]["judgeLineRotateEvents"][j]["endTime"]*mult
            t.close()
        
    notelist=[]
    hittimelist=[]
    hitsoundlist = []
    linehight=int(9*height/1080)
    linelength=int(numpy.sqrt(height*height+width*width))
    for i in range(0,len(chart["judgeLineList"])):
        for j in range(0,len(chart["judgeLineList"][i]["notesBelow"])):
            chart["judgeLineList"][i]["notesBelow"][j].update({'HL':False})
            chart["judgeLineList"][i]["notesBelow"][j].update({'Above':False})
            if "floorPosition2" not in chart["judgeLineList"][i]["notesBelow"][j].keys():
                endfloor=end_floor(chart["judgeLineList"][i]["notesBelow"][j]["time"]+
                                    chart["judgeLineList"][i]["notesBelow"][j]["holdTime"],
                                    chart["judgeLineList"][i]["speedEvents"], BarPerMinute)
                chart["judgeLineList"][i]["notesBelow"][j].update({'floorPosition2':endfloor})
            if chart["judgeLineList"][i]["notesBelow"][j]['type']==3:
                chart["judgeLineList"][i]["notesBelow"][j]['speed']=speed_fix(chart["judgeLineList"][i]["notesBelow"][j],
                                                                            chart["judgeLineList"][i]["speedEvents"])
            
            if chart["judgeLineList"][i]["notesBelow"][j]["isFake"] != 1:
                notelist.append(chart["judgeLineList"][i]["notesBelow"][j])
                hittimelist.append(chart["judgeLineList"][i]["notesBelow"][j]["time"])
                hitsoundlist.append((chart["judgeLineList"][i]["notesBelow"][j]["time"], chart["judgeLineList"][i]["notesBelow"][j]["type"]))
            else:
                notelist.append(chart["judgeLineList"][i]["notesBelow"][j])
                hittimelist.append(chart["judgeLineList"][i]["notesBelow"][j]["time"])
                
        for j in range(0,len(chart["judgeLineList"][i]["notesAbove"])):
            chart["judgeLineList"][i]["notesAbove"][j].update({'HL':False})
            chart["judgeLineList"][i]["notesAbove"][j].update({'Above':True})
            if "floorPosition2" not in chart["judgeLineList"][i]["notesAbove"][j].keys():
                endfloor=end_floor(chart["judgeLineList"][i]["notesAbove"][j]["time"]+
                                   chart["judgeLineList"][i]["notesAbove"][j]["holdTime"],
                                   chart["judgeLineList"][i]["speedEvents"], BarPerMinute)
                chart["judgeLineList"][i]["notesAbove"][j].update({'floorPosition2':endfloor})
            if chart["judgeLineList"][i]["notesAbove"][j]['type']==3:
                chart["judgeLineList"][i]["notesAbove"][j]['speed']=speed_fix(chart["judgeLineList"][i]["notesAbove"][j],
                                                                            chart["judgeLineList"][i]["speedEvents"])

            
            if chart["judgeLineList"][i]["notesAbove"][j]["isFake"] != 1:
                notelist.append(chart["judgeLineList"][i]["notesAbove"][j])
                hittimelist.append(chart["judgeLineList"][i]["notesAbove"][j]["time"])
                hitsoundlist.append((chart["judgeLineList"][i]["notesAbove"][j]["time"], chart["judgeLineList"][i]["notesAbove"][j]["type"]))
            else:
                notelist.append(chart["judgeLineList"][i]["notesAbove"][j])###
                hittimelist.append(chart["judgeLineList"][i]["notesAbove"][j]["time"])
                
    for i in range(len(hittimelist)):
        if hittimelist.count(hittimelist[i])!=1:
            notelist[i].update({'HL':True})

    for i in range(0,len(chart["judgeLineList"])):
        for j in range(0,len(chart["judgeLineList"][i]["notesAbove"])):
            if chart["judgeLineList"][i]["notesAbove"][j]['type']==3:
                b_hold=chart["judgeLineList"][i]["notesAbove"][j]
                effect_time=range(int(b_hold['time']),int(b_hold['time']+b_hold['holdTime']),16)
                for k in effect_time:
                    a_effect={'type': 5,
                              'isFake': b_hold['isFake'],
                              'time': k,
                              'positionX': b_hold['positionX'],
                              'holdTime': 0,
                              'speed': -1.0,
                              'floorPosition': -100,
                              'Above': True,
                              'floorPosition2': -100}
                    if b_hold['isFake'] != 1:
                        chart["judgeLineList"][i]["notesAbove"].append(a_effect)
                        notelist.append(a_effect)
        for j in range(0,len(chart["judgeLineList"][i]["notesBelow"])):
            if chart["judgeLineList"][i]["notesBelow"][j]['type']==3:
                b_hold=chart["judgeLineList"][i]["notesBelow"][j]
                effect_time=range(int(b_hold['time']),int(b_hold['time']+b_hold['holdTime']),16)
                
                for k in effect_time:
                    a_effect={'type': 5,
                              'isFake': b_hold['isFake'],
                              'time': k,
                              'positionX': b_hold['positionX'],
                              'holdTime': 0,
                              'speed': -1.0,
                              'floorPosition': -100,
                              'Above': True,
                              'floorPosition2': -100}
                    if b_hold['isFake'] != 1:
                        chart["judgeLineList"][i]["notesBelow"].append(a_effect)
                        notelist.append(a_effect)
                    
    combo_frame=[]
    for i in range(len(notelist)):
        notelist[i].update({'id':i})
        PX=notelist[i]['positionX']*width/1920
        notelist[i].update({'positionX':PX})
        notelist[i].update({'hitFrame':b2f(notelist[i]['time'],fps,BarPerMinute)})
        if notelist[i]['type']!=5 and notelist[i]['isFake']!=1:
            combo_frame.append(b2f(notelist[i]['time']+notelist[i]['holdTime'],fps,BarPerMinute))

    #计算总帧数

    #totalpaint=int(length*fps)
    
    # fourcc=cv2.VideoWriter_fourcc(*'XVID')
    # videowrite=cv2.VideoWriter(savePath,fourcc,fps,size)
    # mkdir("temp")

    combo_this_frame = 0
    score_this_frame = 0
    totalcombo = chart['numOfNotes']

    vidpath = "tmp/"+str(rand_id)+" Video.avi"
    fourcc=cv2.VideoWriter_fourcc(*'XVID')
    videowrite=cv2.VideoWriter(vidpath, fourcc, fps, size)
    
    photo=ImageTk.PhotoImage(background.resize((int(200*background.width/background.height),200)))
    view=tkinter.Label(showframe,image=photo)
    view.place(x=200,y=175,anchor=tkinter.CENTER)
    
    musicoffset = chart["offset"] * 1000
    PhiAudio(audioPath, hitsoundlist, BarPerMinute, hitsoundoffset, musicoffset, length, var,showframe,sound_Level)
    
    if Back_Video_Path != "Disabled(不启用)":
        var.set("背景视频预处理")
        showframe.update()
        Background_Video_Path="tmp/"+str(rand_id)+" Background.avi"
        resolution=str(width)+"x"+str(height)
        print(Back_Video_Path, Background_Video_Path, str(fps), resolution)
        process_video(Back_Video_Path, Background_Video_Path, str(fps), resolution,var,showframe)
        cap = cv2.VideoCapture(Background_Video_Path)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        BV=True
    
    if BV:
        totalpaint=frame_count
    else:
        totalpaint=int(length*fps)
    
    APS=int(Superior_Data[6])
    
    print(combo_this_frame, totalcombo,APS)
    
    print(totalpaint)
    
    #totalpaint=100

    
    for i in range(totalpaint):
        
        
        if BV:
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, vframe = cap.read()
            cv_image = cv2.cvtColor(vframe, cv2.COLOR_BGR2RGB)
            # 将NumPy数组转换为PIL Image对象
            frame = ImageEnhance.Brightness(Image.fromarray(cv_image)).enhance(0.55)
        else:
            frame=background.copy()
        
        var.set("渲染帧数："+str(i)+"/"+str(totalpaint)+"  进度百分比："+str(round(100*i/totalpaint,2))+"%")
        while i in combo_frame:  
            combo_this_frame += 1
            combo_frame.remove(i)
        try:
            global IncreasingScore
            present_score=IncreasingScore
        except:
            present_score=0
        score_the_frame = score(combo_this_frame, totalcombo,APS)
        IncreasingScore=int(present_score+(score_the_frame-present_score)*0.5)
        score_this_frame=score2(IncreasingScore,APS)
        if DynamicScore==False:
            score_this_frame=score_the_frame
            score_this_frame=score3(score_this_frame,APS)
        
        beat = f2b(i, fps, BarPerMinute)
        #frame = background.copy()
        #把分数渲染移到了最后 防止判定线遮挡UI

        note_this_frame=[]
        hold_this_frame=[]
        effect_this_frame=[]
        for k in range(len(chart["judgeLineList"])):
            while True:
                starttime=chart["judgeLineList"][k]["judgeLineMoveEvents"][0]["startTime"]
                endtime=chart["judgeLineList"][k]["judgeLineMoveEvents"][0]["endTime"]
                if beat>=starttime and beat<endtime:
                    start=chart["judgeLineList"][k]["judgeLineMoveEvents"][0]["start"]
                    end=chart["judgeLineList"][k]["judgeLineMoveEvents"][0]["end"]
                    start2=chart["judgeLineList"][k]["judgeLineMoveEvents"][0]["start2"]
                    end2=chart["judgeLineList"][k]["judgeLineMoveEvents"][0]["end2"]
                    linex=cut(start,end,starttime,endtime,beat)
                    liney=cut(start2,end2,starttime,endtime,beat)
                    break
                else:
                    chart["judgeLineList"][k]["judgeLineMoveEvents"].pop(0)
            while True:
                starttime=chart["judgeLineList"][k]["judgeLineRotateEvents"][0]["startTime"]
                endtime=chart["judgeLineList"][k]["judgeLineRotateEvents"][0]["endTime"]
                if beat>=starttime and beat<endtime:
                    start=chart["judgeLineList"][k]["judgeLineRotateEvents"][0]["start"]
                    end=chart["judgeLineList"][k]["judgeLineRotateEvents"][0]["end"]
                    rotate=cut(start,end,starttime,endtime,beat)
                    break
                else:
                    chart["judgeLineList"][k]["judgeLineRotateEvents"].pop(0)
            while True:
                starttime=chart["judgeLineList"][k]["judgeLineDisappearEvents"][0]["startTime"]
                endtime=chart["judgeLineList"][k]["judgeLineDisappearEvents"][0]["endTime"]
                if beat>=starttime and beat<endtime:
                    start=chart["judgeLineList"][k]["judgeLineDisappearEvents"][0]["start"]
                    end=chart["judgeLineList"][k]["judgeLineDisappearEvents"][0]["end"]
                    alpha=cut(start,end,starttime,endtime,beat)
                    break
                else:
                    chart["judgeLineList"][k]["judgeLineDisappearEvents"].pop(0)
            if alpha!=0:
                if LineColor:
                    aline=Image.new("RGBA",(linelength,linehight),(237,236,176,int(alpha*255)))
                else:
                    aline=Image.new("RGBA",(linelength,linehight),(255,255,255,int(alpha*255)))
                aline=aline.rotate(rotate, expand=True)
                xp=int(linex*background.width)
                yp=int((1-liney)*background.height)
                (xp,yp,x,y)=linepos(height,width,rotate,xp,yp,aline)
                
                frame.paste(aline,(xp,yp),aline)
                
            floor_range=present_floor(beat,chart["judgeLineList"][k]["speedEvents"],BarPerMinute)
            
            for j in range(len(chart["judgeLineList"][k]["notesAbove"])):
                try:
                    if i-chart["judgeLineList"][k]["notesAbove"][j]['hitFrame']<30*fps/60 and i-chart["judgeLineList"][k]["notesAbove"][j]['hitFrame']>=0 and chart["judgeLineList"][k]["notesAbove"][j]["isFake"]!=1 :
                        effect_this_frame.append(chart["judgeLineList"][k]["notesAbove"][j])
                except:
                    if beat > chart["judgeLineList"][k]["notesAbove"][j]['time']+chart["judgeLineList"][k]["notesAbove"][j]['holdTime'] :
                        chart["judgeLineList"][k]["notesAbove"].pop(j)
                        chart["judgeLineList"][k]["notesAbove"].insert(j,"delete")
                   
            while "delete" in chart["judgeLineList"][k]["notesAbove"]:
                chart["judgeLineList"][k]["notesAbove"].remove("delete")
                
            for j in range(len(chart["judgeLineList"][k]["notesAbove"])):
                f=chart["judgeLineList"][k]["notesAbove"][j]["floorPosition"]
                f2=chart["judgeLineList"][k]["notesAbove"][j]["floorPosition2"]
                hittime=chart["judgeLineList"][k]["notesAbove"][j]["time"]
                NS=chart["judgeLineList"][k]["notesAbove"][j]["speed"]
                if f2>=floor_range[0] and f<=floor_range[1] and chart["judgeLineList"][k]["notesAbove"][j]['time']+chart["judgeLineList"][k]["notesAbove"][j]['holdTime']>=beat:
                    distance=(chart["judgeLineList"][k]["notesAbove"][j]['floorPosition']-floor_range[0])*height/1080
                    distance2=(chart["judgeLineList"][k]["notesAbove"][j]['floorPosition2']-floor_range[0])*height/1080
                   
                    chart["judgeLineList"][k]["notesAbove"][j].update({'linex':linex,
                                                                    'liney':liney,
                                                                    'rotate':rotate,
                                                                    'distance':distance,
                                                                    'distance2':distance2})
                    if chart["judgeLineList"][k]["notesAbove"][j]["type"]==3:
                        hold_this_frame.append(chart["judgeLineList"][k]["notesAbove"][j])
                    elif chart["judgeLineList"][k]["notesAbove"][j]["type"]!=5:
                        note_this_frame.append(chart["judgeLineList"][k]["notesAbove"][j])
                elif NS==0 and f2>=floor_range[0]:
                 
                    distance=(chart["judgeLineList"][k]["notesAbove"][j]['floorPosition']-floor_range[0])*height/1080
                    distance2=(chart["judgeLineList"][k]["notesAbove"][j]['floorPosition2']-floor_range[0])*height/1080
                    chart["judgeLineList"][k]["notesAbove"][j].update({'linex':linex,
                                                                    'liney':liney,
                                                                    'rotate':rotate,
                                                                    'distance':distance,
                                                                    'distance2':distance2})
                    note_this_frame.append(chart["judgeLineList"][k]["notesAbove"][j])
                #elif i-chart["judgeLineList"][k]["notesAbove"][j]['hitFrame']>30*fps/60:
                #    chart["judgeLineList"][k]["notesAbove"].pop(j)
                #    chart["judgeLineList"][k]["notesAbove"].insert(j,"delete")
                elif hittime-beat<4 and hittime-beat>=0:
                 
                    chart["judgeLineList"][k]["notesAbove"][j].update({'linex':linex,
                                                                    'liney':liney,
                                                                    'rotate':rotate})
            while "delete" in chart["judgeLineList"][k]["notesAbove"]:
                chart["judgeLineList"][k]["notesAbove"].remove("delete")
            
            for j in range(len(chart["judgeLineList"][k]["notesBelow"])):
                try:
                   if i-chart["judgeLineList"][k]["notesBelow"][j]['hitFrame']<30*fps/60 and i-chart["judgeLineList"][k]["notesBelow"][j]['hitFrame']>=0 and chart["judgeLineList"][k]["notesBelow"][j]["isFake"]!=1 :
                       effect_this_frame.append(chart["judgeLineList"][k]["notesBelow"][j])
                except:
                    if beat > chart["judgeLineList"][k]["notesBelow"][j]['time']+chart["judgeLineList"][k]["notesBelow"][j]['holdTime'] :
                        chart["judgeLineList"][k]["notesBelow"].pop(j)
                        chart["judgeLineList"][k]["notesBelow"].insert(j,"delete")
                    
            while "delete" in chart["judgeLineList"][k]["notesBelow"]:
                chart["judgeLineList"][k]["notesBelow"].remove("delete")
                
            for j in range(len(chart["judgeLineList"][k]["notesBelow"])):
                f=chart["judgeLineList"][k]["notesBelow"][j]["floorPosition"]
                f2=chart["judgeLineList"][k]["notesBelow"][j]["floorPosition2"]
                hittime=chart["judgeLineList"][k]["notesBelow"][j]["time"]
                NS=chart["judgeLineList"][k]["notesBelow"][j]["speed"]
                if f2>=floor_range[0] and f<=floor_range[1] and chart["judgeLineList"][k]["notesBelow"][j]['time']+chart["judgeLineList"][k]["notesBelow"][j]['holdTime']>=beat:
                    distance=(chart["judgeLineList"][k]["notesBelow"][j]['floorPosition']-floor_range[0])*height/1080
                    distance2=(chart["judgeLineList"][k]["notesBelow"][j]['floorPosition2']-floor_range[0])*height/1080
                    chart["judgeLineList"][k]["notesBelow"][j].update({'linex':linex,
                                                                    'liney':liney,
                                                                    'rotate':rotate,
                                                                    'distance':distance,
                                                                    'distance2':distance2})
                    if chart["judgeLineList"][k]["notesBelow"][j]["type"]==3:
                        hold_this_frame.append(chart["judgeLineList"][k]["notesBelow"][j])
                    else:
                        note_this_frame.append(chart["judgeLineList"][k]["notesBelow"][j])
                elif NS==0 and f2>=floor_range[0]:
                    distance=(chart["judgeLineList"][k]["notesBelow"][j]['floorPosition']-floor_range[0])*height/1080
                    distance2=(chart["judgeLineList"][k]["notesBelow"][j]['floorPosition2']-floor_range[0])*height/1080
                    chart["judgeLineList"][k]["notesBelow"][j].update({'linex':linex,
                                                                    'liney':liney,
                                                                    'rotate':rotate,
                                                                    'distance':distance,
                                                                    'distance2':distance2})
                    note_this_frame.append(chart["judgeLineList"][k]["notesBelow"][j])
                #elif i-chart["judgeLineList"][k]["notesBelow"][j]['hitFrame']>30*fps/60:
                #    chart["judgeLineList"][k]["notesBelow"].pop(j)
                #    chart["judgeLineList"][k]["notesBelow"].insert(j,"delete")
                elif hittime-beat<4 and hittime-beat>=0:
                    chart["judgeLineList"][k]["notesBelow"][j].update({'linex':linex,
                                                                    'liney':liney,
                                                                    'rotate':rotate})
            while "delete" in chart["judgeLineList"][k]["notesBelow"]:
                chart["judgeLineList"][k]["notesBelow"].remove("delete")
                
        for k in range(len(hold_this_frame)):
            posXY=paste_hold_pos(frame,hold_this_frame[k],f2b(i,fps,BarPerMinute))
            rot=hold_this_frame[k]["rotate"]
            if hold_this_frame[k]["Above"]==False:
                rot=hold_this_frame[k]["rotate"]+180
            if hold_this_frame[k]['HL']==True:
                if hold_this_frame[k]['time']>f2b(i,fps,BarPerMinute) and hold_this_frame[k]['distance']>=0:
                    a_hold1HL=hold1HL.rotate(rot, expand=True)
                    pos1=(int(posXY[0][0]-0.5*a_hold1HL.width),int(posXY[0][1]-0.5*a_hold1HL.height))
                    frame.paste(a_hold1HL,pos1,a_hold1HL)
                a_hold2HL=hold2HL.resize((hold2HL.width,posXY[3]+1)).rotate(rot, expand=True)
                pos2=(int(posXY[1][0]-0.5*a_hold2HL.width),int(posXY[1][1]-0.5*a_hold2HL.height))
                frame.paste(a_hold2HL,pos2,a_hold2HL)          
            else:
                if hold_this_frame[k]['time']>f2b(i,fps,BarPerMinute) and hold_this_frame[k]['distance']>=0:
                    a_hold1=hold1.rotate(rot, expand=True)
                    pos1=(int(posXY[0][0]-0.5*a_hold1.width),int(posXY[0][1]-0.5*a_hold1.height))
                    frame.paste(a_hold1,pos1,a_hold1)
                a_hold2=hold2.resize((hold2.width,posXY[3]+1)).rotate(rot, expand=True)
                pos2=(int(posXY[1][0]-0.5*a_hold2.width),int(posXY[1][1]-0.5*a_hold2.height))
                frame.paste(a_hold2,pos2,a_hold2)
            a_hold3=hold3.rotate(rot, expand=True)
            pos3=(int(posXY[2][0]-0.5*a_hold3.width),int(posXY[2][1]-0.5*a_hold3.height))
            frame.paste(a_hold3,pos3,a_hold3)

        for k in range(len(note_this_frame)):
            posXY=paste_pos(frame,note_this_frame[k])
            if note_this_frame[k]['type']==1:
                if note_this_frame[k]['HL']==True:
                    a_tapHL=tapHL.rotate(note_this_frame[k]['rotate'], expand=True)
                    pos=(int(posXY[0]-0.5*a_tapHL.width),int(posXY[1]-0.5*a_tapHL.height))
                    frame.paste(a_tapHL,pos,a_tapHL)
                else:
                    a_tap=tap.rotate(note_this_frame[k]['rotate'], expand=True)
                    pos=(int(posXY[0]-0.5*a_tap.width),int(posXY[1]-0.5*a_tap.height))
                    frame.paste(a_tap,pos,a_tap)
            elif note_this_frame[k]['type']==2:
                if note_this_frame[k]['HL']==True:
                    a_dragHL=dragHL.rotate(note_this_frame[k]['rotate'], expand=True)
                    pos=(int(posXY[0]-0.5*a_dragHL.width),int(posXY[1]-0.5*a_dragHL.height))
                    frame.paste(a_dragHL,pos,a_dragHL)
                else:
                    a_drag=drag.rotate(note_this_frame[k]['rotate'], expand=True)
                    pos=(int(posXY[0]-0.5*a_drag.width),int(posXY[1]-0.5*a_drag.height))
                    frame.paste(a_drag,pos,a_drag)
            elif note_this_frame[k]['type']==4:
                if note_this_frame[k]['HL']==True:
                    a_flickHL=flickHL.rotate(note_this_frame[k]['rotate'], expand=True)
                    pos=(int(posXY[0]-0.5*a_flickHL.width),int(posXY[1]-0.5*a_flickHL.height))
                    frame.paste(a_flickHL,pos,a_flickHL)
                else:
                    a_flick=flick.rotate(note_this_frame[k]['rotate'], expand=True)
                    pos=(int(posXY[0]-0.5*a_flick.width),int(posXY[1]-0.5*a_flick.height))
                    frame.paste(a_flick,pos,a_flick)
                    
        for k in range(len(effect_this_frame)):
            if effect_this_frame[k]['type'] != 3:    
                posXY=effect_pos(frame,effect_this_frame[k])
                pos=(int(posXY[0]-0.5*hit[int((i-effect_this_frame[k]['hitFrame'])*60/fps)].width),int(posXY[1]-0.5*hit[int((i-effect_this_frame[k]['hitFrame'])*60/fps)].height))
                frame.paste(hit[int((i-effect_this_frame[k]['hitFrame'])*60/fps)],pos,hit[int((i-effect_this_frame[k]['hitFrame'])*60/fps)])
                particle_pos=p4(rotgroup[effect_this_frame[k]['id']%10],particle_length[int((i-effect_this_frame[k]['hitFrame'])*60/fps)],width,particle[int((i-effect_this_frame[k]['hitFrame'])*60/fps)],posXY)
                frame.paste(particle[int((i-effect_this_frame[k]['hitFrame'])*60/fps)],particle_pos[0],particle[int((i-effect_this_frame[k]['hitFrame'])*60/fps)])
                frame.paste(particle[int((i-effect_this_frame[k]['hitFrame'])*60/fps)],particle_pos[1],particle[int((i-effect_this_frame[k]['hitFrame'])*60/fps)])
                frame.paste(particle[int((i-effect_this_frame[k]['hitFrame'])*60/fps)],particle_pos[2],particle[int((i-effect_this_frame[k]['hitFrame'])*60/fps)])
                frame.paste(particle[int((i-effect_this_frame[k]['hitFrame'])*60/fps)],particle_pos[3],particle[int((i-effect_this_frame[k]['hitFrame'])*60/fps)])

        draw = ImageDraw.Draw(frame)
        
        if combo_this_frame >= 3:
            
            combo_size = combo_font1.getsize(str(combo_this_frame))
            draw.text((int(0.5*background.width-0.5*title[0]),int(100*height/1080) - 8),
                    Combo_text,font=combo_font2,fill=(250,250,250))
            draw.text((int(0.5 * background.width - 0.5 * combo_size[0]),int(20 * height / 1080) - 3),
                    str(combo_this_frame) ,font=combo_font1, fill=(250,250,250))
        score_size=score_font.getsize(score_this_frame)
        draw.text((int(background.width-score_size[0]-45*height/1080) + 7,int(30*height/1080) + 2),
                score_this_frame,font=score_font,fill=(250,250,250))
       
        draw.text((int(41 * height / 1080), int(frame.height - 39 * height / 1080 - Song_title[1])),
                  songName, font=text_font, fill=(255,255,255))
        
        draw.text((int(frame.width - 41 * height / 1080 - Level_title[0]), 
                   int(frame.height - 39 * height / 1080 - Level_title[1])), level, font=text_font, fill=(255,255,255))

        frame.paste(pause, (int(60 * height / 1920), int(40 * height / 1080)), mask = pause)
        del draw
        
        #进度条
        frame.paste(ProgressBar, (int(i / totalpaint * background.width) - ProgressBar.width, 0), ProgressBar)
        
        videowrite.write(cv2.cvtColor(numpy.asarray(frame),cv2.COLOR_RGB2BGR))
        photo=ImageTk.PhotoImage(frame.resize((int(200*frame.width/frame.height),200)))

        view.config(image=photo)
        view.imgtk=photo
        showframe.update()
        
    videowrite.release()
    
    End_UI_1 = Image.new('RGBA', (width, height), (0,0,0,0))
    draw = ImageDraw.Draw(End_UI_1)
    if combo_this_frame >= 3:
        
        combo_size = combo_font1.getsize(str(combo_this_frame))
        draw.text((int(0.5 * background.width - 0.5 * combo_size[0]),int(20 * height / 1080) - 3),
                str(combo_this_frame) ,font=combo_font1, fill=(250,250,250))
    score_size=score_font.getsize(score_this_frame)
    draw.text((int(background.width-score_size[0]-45*height/1080) + 7,int(30*height/1080) + 2),
            score_this_frame,font=score_font,fill=(250,250,250))
    
    End_UI_1.paste(pause, (int(60 * height / 1920), int(40 * height / 1080)), mask = pause)
    End_UI_1.paste(ProgressBar, (int(i / totalpaint * background.width) - ProgressBar.width, 0), ProgressBar)
    del draw
    
    End_UI_3 = Image.new('RGBA', (width, height), (0,0,0,0))
    draw = ImageDraw.Draw(End_UI_3)
    if combo_this_frame >= 3:
        draw.text((int(0.5*background.width-0.5*title[0]),int(100*height/1080) - 8),
                Combo_text,font=combo_font2,fill=(250,250,250))
    del draw
    
    End_UI_2 = Image.new('RGBA', (width, height), (0,0,0,0))
    draw = ImageDraw.Draw(End_UI_2)
    
    draw.text((int(41 * height / 1080), int(frame.height - 39 * height / 1080 - Song_title[1])),
              songName, font=text_font, fill=(255,255,255))
    
    draw.text((int(frame.width - 41 * height / 1080 - Level_title[0]), 
               int(frame.height - 39 * height / 1080 - Level_title[1])), level, font=text_font, fill=(255,255,255))

    del draw
    
    End_UI_1.save("tmp/"+str(rand_id)+" UI_1.png")
    End_UI_2.save("tmp/"+str(rand_id)+" UI_2.png")
    End_UI_3.save("tmp/"+str(rand_id)+" UI_3.png")
    
    if BV:
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, vframe = cap.read()
        cv_image = cv2.cvtColor(vframe, cv2.COLOR_BGR2RGB)
        # 将NumPy数组转换为PIL Image对象
        frame = ImageEnhance.Brightness(Image.fromarray(cv_image)).enhance(0.55)
        frame.save("tmp/"+str(rand_id)+" UI_4.png")
    else:
        background.save("tmp/"+str(rand_id)+" UI_4.png")
        
    try:
        cap.release()
    except:
        pass
    
    Ani=False
    if Superior_Data[0] != "禁用":
        AST=Superior_Data[0]
        Animation_data=[songName,level,width,height,fps,rand_id,APS,totalcombo,Picture,AST]
        Animation.start(Animation_data)
        Ani=True
        
    if Superior_Data[1] != "禁用":
        AET=Superior_Data[1]
        Tier=Superior_Data[8]
        Animation_data=[songName,level,width,height,fps,rand_id,APS,totalcombo,Picture,AET,var,showframe,Tier]
        print(Animation_data)
        Animation.end(Animation_data)
        Ani=True 
        
    mkdir("export")
    var.set("正在合成音视频")
    showframe.update()
    if Ani==False:
        vidpath = os.path.abspath("tmp/"+str(rand_id)+" Video.avi")
        audpath = os.path.abspath("tmp/"+str(rand_id)+" ComposedAudio.wav")
        export_p = os.path.abspath("export")
        video_add_audio(vidpath, audpath, export_p, f"{songName}.mp4")
    else:
        try:
            vidpath = os.path.abspath("tmp/"+str(rand_id)+" Video.avi")
            audpath = os.path.abspath("tmp/"+str(rand_id)+" ComposedAudio.wav")
            export_p = os.path.abspath("tmp")
            video_add_audio(vidpath, audpath, export_p, str(rand_id)+" ComposedVideo.mp4")
            merge_videos("tmp/"+str(rand_id)+" ComposedVideo.mp4", "tmp/"+str(rand_id)+" Animation_3.mp4", "export", songName)
        except:
            pass

    
    
    def open_folder():
        current_dir = os.getcwd()
        export_dir = os.path.join(current_dir, 'export')
        export_url = 'file:///' + export_dir.replace('\\', '/')
        os.startfile(export_url)
    try:
        
        toaster = ToastNotifier()
        toaster.show_toast("生成完毕", "视频已保存至 export 文件夹", icon_path="Source/R.ico", duration=1, callback_on_click=open_folder)
    except:
        messagebox.showinfo("完成","视频已保存至 export 文件夹")
    showframe.destroy()

root=tkinter.Tk()
root.withdraw()