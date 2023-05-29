# -*- coding: utf-8 -*-
import cv2
import numpy
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import FFM as ffmpy
from pydub import AudioSegment

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
    
def change_opacity(image, opacity):
    alpha = image.split()[-1]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    image.putalpha(alpha)
    return image

def Draw_1(songName,level,width,Picture_Path):
    
    Picwidth=int(0.5*width)
    Pichight=int(Picwidth*1240/1980)
    img=Image.open(Picture_Path).convert("RGBA")
    shadow=Image.open("Source/shadow.png").convert("RGBA")
    Illustrate=Parallel(Trim(img,Pichight,Picwidth))
    shadow=shadow.resize((Illustrate.width,Illustrate.height))
    Illustrate=ImageChops.multiply(Illustrate,shadow)
    text_font=ImageFont.truetype("Source/Source Han Sans & Saira Hybrid-Regular.ttf",int(Illustrate.height/10))
    level_font=ImageFont.truetype("Source/Source Han Sans & Saira Hybrid-Regular.ttf", int(Illustrate.height/20))
    draw=ImageDraw.Draw(Illustrate)
    title=text_font.getsize(songName)
    draw.text((int(Illustrate.width/20),int(Illustrate.height-Illustrate.height/25-title[1])),songName,font=text_font,fill=(255,255,255))
    title=level_font.getsize(level)
    draw.text((int(Illustrate.width-Illustrate.width/5.5-title[0]),int(Illustrate.height-Illustrate.height/25-title[1])),level,font=level_font,fill=(255,255,255))
    del draw
    #Illustrate.show()
    return Illustrate

def Draw_2(width):
    Picwidth=int(0.5*width)
    Pichight=int(Picwidth*1240/1980*0.5)
    img=Image.open("Source/Parallelogram_2.png").convert("RGBA")
    Pa_1=img.resize((int(Pichight/img.height*img.width),Pichight))
    return Pa_1

def Draw_3(width):
    Picwidth=int(0.5*width)
    Pichight=int(Picwidth*1240/1980*0.18)
    img=Image.open("Source/Parallelogram_1.png").convert("RGBA")
    Pa_2=img.resize((int(Pichight/img.height*img.width),Pichight))
    return Pa_2

def result_1(width,APS):
    result_1=Draw_2(width)
    Picwidth=result_1.width
    Pichight=result_1.height
    fontpath="Source/Source Han Sans & Saira Hybrid-Regular.ttf"
    font = ImageFont.truetype(fontpath, int(0.25*Pichight))
    
    draw = ImageDraw.Draw(result_1)
    draw.text((int(0.09*Picwidth),int(0.55*Pichight)),APS,font=font,fill=(250,250,250))
    del draw
    return result_1

def result_2(width,combo):
    Picwidth=int(0.5*width)
    Pichight=int(Picwidth*1240/1980*0.18)
    img=Image.open("Source/result_1.png").convert("RGBA")
    result_2=img.resize((int(Pichight/img.height*img.width),Pichight))
    
    fontpath="Source/Source Han Sans & Saira Hybrid-Regular.ttf"
    font = ImageFont.truetype(fontpath, int(0.5*Pichight))
    
    draw = ImageDraw.Draw(result_2)
    size=font.getsize(combo)
    draw.text((int(0.11*Picwidth-0.5*size[0]),int(0.1*Pichight)),combo,font=font,fill=(250,250,250))
    del draw
    return result_2

def result_3(width,combo):
    Picwidth=int(0.5*width)
    Pichight=int(Picwidth*1240/1980*0.18)
    img=Image.open("Source/result_2.png").convert("RGBA")
    result_3=img.resize((int(Pichight/img.height*img.width),Pichight))
    
    fontpath="Source/Source Han Sans & Saira Hybrid-Regular.ttf"
    font = ImageFont.truetype(fontpath, int(0.39*Pichight))
    
    draw = ImageDraw.Draw(result_3)
    size=font.getsize(combo)
    draw.text((int(0.095*Picwidth-0.5*size[0]),int(0.22*Pichight)),combo,font=font,fill=(250,250,250))
    del draw
    return result_3

def Para_1(t,s,e,p):
    if t<0.4:
        return s
    elif t<0.7:
        alpha = (t-0.4) / 0.3
        output = Image.blend(s, e, alpha)
        return output
    elif t<1.5:
        return e
    elif t<2:
        if t>1.7: 
            p=p.resize((int((0.7+((2-t)*10/3)**0.4*0.2)*s.height/p.height*p.width),int((0.7+((2-t)*10/3)**0.4*0.2)*s.height)))
            alpha=1
        else:
            p=p.resize((int(0.9*s.height/p.height*p.width),int(0.9*s.height)))
            alpha=((t-1.5)*5)**0.3
        x=change_opacity(p, alpha)
        y=e.copy()
        y.paste(x,(int(0.75*e.width-0.5*x.width),int(0.5*e.height-0.5*x.height)),mask=x)
        return y
    else:
        p=p.resize((int(s.height*0.7/p.height*p.width),int(s.height*0.7)))
        y=e.copy()
        y.paste(p,(int(0.75*e.width-0.5*p.width),int(0.5*e.height-0.5*p.height)),mask=p)
        return y

def Para_2(t,s,e):
    if t<0.7:
        return s
    elif t<1:
        alpha = (t-0.7) / 0.3
        output = Image.blend(s, e, alpha)
        return output
    else:
        return e

def Para_3(t,s,e):
    if t<1.0:
        return s
    elif t<1.3:
        alpha = (t-1) / 0.3
        output = Image.blend(s, e, alpha)
        return output
    else:
        return e
    
def start(data):
    pass

def end(data):
     
    [songName,level,width,hight,fps,rand_id,APS,totalcombo,Picture_Path,AET,var,showframe,Tier]=data
    
    size = (width, hight)
    vidpath = "tmp/"+str(rand_id)+" Animation_2.avi"
    fourcc=cv2.VideoWriter_fourcc(*'XVID')
    videowrite=cv2.VideoWriter(vidpath, fourcc, fps, size)
    
    background=Image.open("tmp/"+str(rand_id)+" UI_4.png").convert("RGBA")
    Picture=Blur_background(Image.open(Picture_Path).convert("RGBA"),hight,width,70)
    
    UI_1=Image.open("tmp/"+str(rand_id)+" UI_1.png").convert("RGBA")
    UI_2=Image.open("tmp/"+str(rand_id)+" UI_2.png").convert("RGBA")
    UI_3=Image.open("tmp/"+str(rand_id)+" UI_3.png").convert("RGBA")
    
    Phi=Image.open("Source/Phi.png").convert("RGBA")
    
    Ctn=Image.open("Source/Continue.png").convert("RGBA")
    Ctn=Ctn.resize((int(0.15*width),int(0.15*width/Ctn.width*Ctn.height)))
    
    Rt=Image.open("Source/Retry.png").convert("RGBA")
    Rt=Rt.resize((int(0.15*width),int(0.15*width/Rt.width*Rt.height)))
    
    Illustrate=Draw_1(songName,level,width,Picture_Path)
    Pa_1=Draw_2(width)
    Pa_2=Draw_3(width)
    Pa_3=Draw_3(width)
    Re_1=result_1(width,str(APS))
    Re_2=result_2(width,str(totalcombo))
    Re_3=result_3(width,str(totalcombo))
    num_frames=fps*AET
    empty=Image.new('RGBA', size, (0, 0, 0, 0))
    empty_shadow=Image.new('RGBA', size, (0, 0, 0, 200))
    
    #时间轴
    Fin=True
    for i in range(num_frames):
        Current=i/fps
        #stage1
        if Current<1:
            alpha = i / fps
            output = Image.blend(background, Picture, alpha)
            output.paste(UI_1,(0,int(Current*hight*(-0.15))),mask=UI_1)
            output.paste(UI_2,(0,int(Current*hight*(0.15))),mask=UI_2)
            UI_3_a=change_opacity(UI_3.copy(), 1-Current*2)
            output.paste(UI_3_a,(0,int(Current*hight*(-0.15))),mask=UI_3_a)
        elif Current<3:
            output=Picture
        elif Fin:
            Current=Current-3
            output_1=empty.copy()
            #左侧大图
            if Current<1:
                output_1.paste(Illustrate,(int(0.071*Picture.width+((1-Current)**5)*Picture.width),
                                         int(0.5*Picture.height-0.5*Illustrate.height)),mask=Illustrate)
            else:
                output_1.paste(Illustrate,(int(0.071*Picture.width),int(0.5*Picture.height-0.5*Illustrate.height)),mask=Illustrate)
            #信息框1
            if Current<0.1:
                pass
            elif Current<1.1:
                output_1.paste(Para_1(Current,Pa_1,Re_1,Phi),(int(0.938*Picture.width-Pa_1.width+((1.1-Current)**5)*Picture.width),
                                         int(0.5*Picture.height-Pa_1.height)),mask=Para_1(Current,Pa_1,Re_1,Phi))
            else:
                output_1.paste(Para_1(Current,Pa_1,Re_1,Phi),(int(0.938*Picture.width-Pa_1.width),
                                         int(0.5*Picture.height-Pa_1.height)),mask=Para_1(Current,Pa_1,Re_1,Phi))
            #信息框2
            if Current<1:
                output_1.paste(Para_2(Current,Pa_2,Re_2),(int(0.893*Picture.width-Pa_2.width+((1-Current)**3)*Picture.width),
                                         int(0.5*Picture.height+Pa_1.height-Pa_2.height-0.5*Pa_1.height)),mask=Para_2(Current,Pa_2,Re_2))
            else:
                output_1.paste(Para_2(Current,Pa_2,Re_2),(int(0.893*Picture.width-Pa_2.width),int(0.5*Picture.height+Pa_1.height-Pa_2.height-0.5*Pa_1.height)),mask=Para_2(Current,Pa_2,Re_2))
            #信息框3
            if Current<1.2:
                output_1.paste(Para_3(Current,Pa_3,Re_3),(int(0.872*Picture.width-Pa_3.width+((1.2-Current)**4)*Picture.width),
                                         int(0.5*Picture.height+Pa_1.height-Pa_3.height)),mask=Para_3(Current,Pa_3,Re_3))
            else:
                output_1.paste(Para_3(Current,Pa_3,Re_3),(int(0.872*Picture.width-Pa_3.width),int(0.5*Picture.height+Pa_1.height-Pa_3.height)),mask=Para_3(Current,Pa_3,Re_3))
                
            if Current<0.7:
                pass
            elif Current<2.1:
                output_1.paste(Ctn,(int(0.9*Picture.width+((2-Current)/1.4)**5*Picture.width/10),
                                         int(0.99*Picture.height-Ctn.height)),mask=Ctn)
                output_1.paste(Rt,(int(-0.05*Picture.width+((Current-2)/1.4)**5*Picture.width/10),
                                         int(0.01*Picture.height)),mask=Rt)
            else:
                output_1.paste(Ctn,(int(0.9*Picture.width),
                                         int(0.99*Picture.height-Ctn.height)),mask=Ctn)
                output_1.paste(Rt,(int(-0.05*Picture.width),
                                         int(0.01*Picture.height)),mask=Rt)
                Fin=False
            output_2=empty.copy()
            output_2.paste(empty_shadow,(0,0),mask=output_1)
            output_2=output_2.filter(ImageFilter.GaussianBlur(radius=10*hight/1080))
            output=Picture.copy()
            output.paste(output_2,(0,0),mask=output_2)
            output.paste(output_1,(0,0),mask=output_1)
            #头像框
            #finish
            
        videowrite.write(cv2.cvtColor(numpy.asarray(output),cv2.COLOR_RGB2BGR))
        var.set("正在生成结算动画: "+str(i)+"/"+str(num_frames)+"  进度百分比："+str(round(100*i/num_frames,2))+"%")
        showframe.update()
    input_video = vidpath
    if Tier=="EZ" :
        input_audio = 'Source/LevelSound/EZ.wav'
    elif Tier=="HD" :
        input_audio = 'Source/LevelSound/HD.wav'
    elif Tier=="IN" or Tier=="IN #默认":
        input_audio = 'Source/LevelSound/IN.wav'
    elif Tier=="AT" :
        input_audio = 'Source/LevelSound/AT.wav'
    output_video = "tmp/"+str(rand_id)+" Animation_3.mp4"
    music = AudioSegment.from_wav(input_audio)
    audio = AudioSegment.silent(duration=AET * 1000)
    audio = audio.overlay(music, position=3000)
    audio.export("tmp/"+str(rand_id)+" tmp_3.wav", format="wav")
    input_audio="tmp/"+str(rand_id)+" tmp_3.wav"
    ff = ffmpy.FFmpeg(
        inputs={input_video: None, input_audio: None},
        outputs={output_video: '-map 0:v -map 1:a -c:v copy -c:a {} -y'.format("aac")})
    ff.run()
    videowrite.release()
    
    
