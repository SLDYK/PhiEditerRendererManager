# -*- coding: utf-8 -*-
import math
import os
from PIL import Image, ImageFilter, ImageChops, ImageEnhance
from FPY import FfmpegProgress
import subprocess


def Trim(img,hight,width,Blur):
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
    Tr=Tr.filter(ImageFilter.GaussianBlur(radius=Blur*hight/1080))
    Tr=ImageChops.multiply(Tr,Image.new("RGBA",(Tr.width,Tr.height),(200,200,200,255)))
    Tr = ImageEnhance.Brightness(Tr).enhance(0.55) #亮度调整
    return Tr

def f2b(i,fps,BPM):
    s=32*BPM*(i/fps)/60
    return s

def b2f(s,fps,BPM):
    i=60*fps*s/32/BPM
    return int(i)

def cut(start,end,starttime,endtime,point):
    aim=(point-starttime)/(endtime-starttime)
    result=start+(end-start)*aim    
    return result

def present_floor(beat,speed,BPM):
    for i in range(len(speed)):
        if beat>=speed[i]["startTime"] and beat<speed[i]["endTime"]:
            floorstart=speed[i]['floorPosition']
            starttime=speed[i]["startTime"]
            floor=floorstart+(beat-starttime)/32/BPM*60*speed[i]["value"]
            break
    return [floor-0.001,floor+3.333]

def end_floor(beat,speed,BPM):
    for i in range(len(speed)):
        if beat>=speed[i]["startTime"] and beat<speed[i]["endTime"]:
            floorstart=speed[i]['floorPosition']
            starttime=speed[i]["startTime"]
            floor=floorstart+(beat-starttime)/32/BPM*60*speed[i]["value"]
            break
        else:
            floor=0
    return floor

def holdhead_fix(img):
    layer=Image.new("RGBA",(img.width,int(2*img.height)),(0,0,0,0))
    layer.paste(img,(0,img.height))
    return layer

def holdend_fix(img):
    layer=Image.new("RGBA",(img.width,int(2*img.height)),(0,0,0,0))
    layer.paste(img,(0,0))
    return layer

def speed_fix(note,speed):
    value=note['speed']
    beat=note['time']
    for i in range(len(speed)):
        if beat>=speed[i]["startTime"] and beat<speed[i]["endTime"]:
            try:
                value=value/speed[i]["value"]
            except:
                value=0
            break
    return value

def paste_pos(frame,note):
    x1=frame.width*note['linex']
    y1=frame.height*(1-note['liney'])
    x2=x1+320/3*note['positionX']*math.cos(note['rotate']/180*math.pi)
    y2=y1-320/3*note['positionX']*math.sin(note['rotate']/180*math.pi)
    distance=note['distance']*650*note["speed"]
    if note['Above']:
        x3=x2+distance*math.cos((note['rotate']+90)/180*math.pi)
        y3=y2-distance*math.sin((note['rotate']+90)/180*math.pi)
    else:
        x3=x2-distance*math.cos((note['rotate']+90)/180*math.pi)
        y3=y2+distance*math.sin((note['rotate']+90)/180*math.pi)
    return [x3,y3]

def effect_pos(frame,note):
    # print(note)
    try:
        x1=frame.width*note['linex']
    except:
        print(note)
    y1=frame.height*(1-note['liney'])
    x2=x1+320/3*note['positionX']*math.cos(note['rotate']/180*math.pi)
    y2=y1-320/3*note['positionX']*math.sin(note['rotate']/180*math.pi)
    return [x2,y2]

def paste_hold_pos(frame,hold,beat):
    x1=frame.width*hold['linex']
    y1=frame.height*(1-hold['liney'])
    x2=x1+320/3*hold['positionX']*math.cos(hold['rotate']/180*math.pi)
    y2=y1-320/3*hold['positionX']*math.sin(hold['rotate']/180*math.pi)
    distance=hold['distance']*650*hold["speed"]
    distance2=hold['distance2']*650*hold["speed"]
    if hold['Above']:
        xhead=x2+distance*math.cos((hold['rotate']+90)/180*math.pi)
        yhead=y2-distance*math.sin((hold['rotate']+90)/180*math.pi)
        xend=x2+distance2*math.cos((hold['rotate']+90)/180*math.pi)
        yend=y2-distance2*math.sin((hold['rotate']+90)/180*math.pi)
    else:
        xhead=x2-distance*math.cos((hold['rotate']+90)/180*math.pi)
        yhead=y2+distance*math.sin((hold['rotate']+90)/180*math.pi)
        xend=x2-distance2*math.cos((hold['rotate']+90)/180*math.pi)
        yend=y2+distance2*math.sin((hold['rotate']+90)/180*math.pi)
    if distance>=0 and hold['time']>=beat:
        xbody=0.5*(xhead+xend)
        ybody=0.5*(yhead+yend)
        length=distance2-distance
    else:
        xbody=0.5*(x2+xend)
        ybody=0.5*(y2+yend)
        length=distance2
    if length<=1:
        length=1
    return [[xhead,yhead],[xbody,ybody],[xend,yend],int(length)]

def p4(rotgroup,length,width,img,pos):
    length=length*width/1920*3
    x1=int(pos[0]-(math.cos(rotgroup[0]/180*math.pi)*length+0.5*img.width))
    y1=int(pos[1]-(math.sin(rotgroup[0]/180*math.pi)*length+0.5*img.height))
    x2=int(pos[0]-(math.cos(rotgroup[1]/180*math.pi)*length+0.5*img.width))
    y2=int(pos[1]-(math.sin(rotgroup[1]/180*math.pi)*length+0.5*img.height))
    x3=int(pos[0]-(math.cos(rotgroup[2]/180*math.pi)*length+0.5*img.width))
    y3=int(pos[1]-(math.sin(rotgroup[2]/180*math.pi)*length+0.5*img.height))
    x4=int(pos[0]-(math.cos(rotgroup[3]/180*math.pi)*length+0.5*img.width))
    y4=int(pos[1]-(math.sin(rotgroup[3]/180*math.pi)*length+0.5*img.height))
    return [(x1,y1),(x2,y2),(x3,y3),(x4,y4)]

def linepos(hight,width,rotate,xp,yp,aline):
    x0=0.5*width
    y0=0.5*hight
    k=math.tan((-rotate%180)*math.pi/180)
    if k==0:
        y=yp
        x=x0
    elif rotate%90==0:
        y=y0
        x=xp
    else:
        x=(x0/k+y0+k*xp-yp)/(1/k+k)
        y=k*x-k*xp+yp
    return (int(x-0.5*aline.width),int(y-0.5*aline.height),int(x),int(y))
    
def score(combo,total,APS):
    s=int(APS*combo/total)
    return s

def score2(s,APS):
    if s!=0:
        s=s+1
    t=str(10**int(math.log(APS+0.5)/math.log(10)+1)+s)
    return t[1:]

def score3(s,APS):
    t=str(10**int(math.log(APS+0.5)/math.log(10)+1)+s)
    return t[1:]

def beat2msec(s, bpm, hitsoundoffset):
    return 60 * s / 32 / bpm * 1000 + hitsoundoffset

def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False
    
def process_video(input_file, output_file, frame_rate, resolution,var,showframe):
    cmd = [
    'ffmpeg',
    '-i', input_file,
    '-c:v', 'libxvid',
    '-vf', f'scale={resolution}, crop=ih*{resolution.split("x")[0]}/{resolution.split("x")[1]}:ih',
    '-r', str(frame_rate),
    '-b:v', '30M',
    output_file]
    ff = FfmpegProgress(cmd, creationflags=subprocess.CREATE_NO_WINDOW)
    #for progress in ffmpeg_progress_yield.run(cmd):
    for progress in ff.run_command_with_progress():
        var.set(f'背景视频预处理: {progress:.2f}%')
        showframe.update()
    
#def process_video(input_file, output_file, frame_rate, resolution):
#    codec = 'libxvid' # 设定编码格式
#    width, height = map(int, resolution.split('x'))
#    aspect_ratio = width / height

#    ff = ffmpy.FFmpeg(
#        inputs={input_file: None},
#        outputs={'pipe:': '-vf "crop=ih*{aspect_ratio}/1:ih" -f null -'}
#    )
#    stdout, stderr = ff.run(stderr=subprocess.PIPE)
#    crop_line = next((line for line in stderr.decode().split('\n') if 'Parsed_crop' in line), None)
#    
#    if crop_line:
#        w_in, h_in = map(int,re.search(r'w:(\d+) h:(\d+)', crop_line).groups())
#        aspect_ratio_in = w_in / h_in
#        if aspect_ratio != aspect_ratio_in:
#            filter_str = f'-vf "crop=ih*{aspect_ratio}/1:ih,scale={resolution}"'
#        else:
#            filter_str = f'-vf scale={resolution}'
#    else:
#        filter_str = f'-vf scale={resolution}'

#    ff = ffmpy.FFmpeg(
#        inputs={input_file: None},
#        outputs={output_file: f'{filter_str} -r {frame_rate} -vcodec {codec}'}
#    )
#    ff.run()