# -*- coding: utf-8 -*-
from tkinter import filedialog
from tkinter import ttk
import traceback
import tkinter
from video_maker import start_rendering
from pec2json import chartify
import os
import sys
import random

def renderer(item,Path):
    
    def init():#谱面基本信息框
    
        def infoed():#点击“下一步”后执行
        
            try:#检查数据可用性
            #if True:
                name=enName.get()
                level=enLevel.get()
                specs=enSpecs.get()
                width=int(specs.split()[0].split("x")[0])
                hight=int(specs.split()[0].split("x")[1])
                fps=int(specs.split()[2].replace("fps",""))
                chart=enChartPath.get()
                picture=enPicturePath.get()
                song=enSongPath.get()
                blur=int(enBlur.get().split()[0])
                    
                if enHighLight.get()=="开启":
                    Highlight=True
                else:
                    Highlight=False
                    
                if enLineColor.get()=="黄":
                    LineColor=True
                else:
                    LineColor=False
                    
                if enDynamicScore.get()=="开启":
                    DynamicScore=True
                else:
                    DynamicScore=False
                    
                notesize=float(enNoteSize.get().split()[0])
                sound_Level=float(enSound.get().split()[0])
                AST=enStartAnimation.get()
                if AST=="启用":
                    AST=10
                AET=enEndAnimation.get()
                if AET=="启用":
                    AET=10
                LOM=enLevelOver.get().split()[0]
                
                Base_Data=[name,level,width,hight,fps,chart,picture,song,Highlight,blur,notesize,LineColor,sound_Level]
                Superior_Data=[AST,AET,enPlayerName.get(),enComboText.get(),
                               enUserIcon.get(),enVideoBackground.get(),enAPS.get(),LOM,enLevelOver.get(),DynamicScore]
                
                
                base.destroy()
                #print([name,level,width,hight,fps,chart,picture,song,Highlight,blur,notesize,LineColor,sound_Level,Superior_Data])
                start_rendering(Base_Data,Superior_Data)
                
                
            except :#不可用则报错
                with open("ErrorsLog.txt","a",encoding="utf_8") as t:
                    traceback.print_exc(file=t)
                    t.close()
                
        def Select(var):#文件选择框
            if var==1:
                filePath=filedialog.askopenfilename(filetypes=[('谱面文件','.json .pec')])
                enChartPath.delete(0, 'end')
                enChartPath.insert(0,filePath)
            elif var==2:
                filePath=filedialog.askopenfilename(filetypes=[('图片文件','.jpg .png')])
                enPicturePath.delete(0, 'end')
                enPicturePath.insert(0,filePath)
            elif var==3:
                filePath=filedialog.askopenfilename(filetypes=[('音频文件','.mp3 .wav .m4a .ogg .aac')])
                enSongPath.delete(0, 'end')
                enSongPath.insert(0,filePath)
            elif var==4:
                filePath=filedialog.askopenfilename(filetypes=[('图片文件','.jpg .png')])
                enUserIcon.delete(0, 'end')
                enUserIcon.insert(0,filePath)
            elif var==5:
                filePath=filedialog.askopenfilename(filetypes=[('视频文件','.mp4 .avi .mkv .flv .rmvb')])
                enVideoBackground.delete(0, 'end')
                enVideoBackground.insert(0,filePath)
            elif var=="Rand":
                with open("Source/Tips.txt","r",encoding="utf_8") as t:
                    Tips=t.readlines()
                    enTip.delete(0, 'end')
                    a_Tip=Tips[random.randint(0,len(Tips)-1)]
                    enTip.insert(0,a_Tip)
                    t.close()
        
        PEdata=Path.rstrip('\n')
        
        base=tkinter.Tk()
        base.title("Settings")
        base.iconbitmap("Source/R.ico")
        base.geometry("600x425")
        
        notebook = ttk.Notebook(base)
        setinfo = tkinter.Frame(base)
        subtitle=tkinter.Label(setinfo,text="基本视频设置",font=('',12),width=30,height=1)
        subtitle.place(x=300,y=30,anchor=tkinter.CENTER)
        
        Var1=tkinter.StringVar(base)
        Var2=tkinter.StringVar(base)
        Var3=tkinter.StringVar(base)
        Var4=tkinter.StringVar(base)
        Var5=tkinter.StringVar(base)
        Var6=tkinter.StringVar(base)
        Var7=tkinter.StringVar(base)
        
        Name=tkinter.Label(setinfo, text='曲名:',font=('',10),width=10,height=1)
        Name.place(x=100,y=80,anchor="e")
        enName=tkinter.Entry(setinfo,show=None,width=23)
        enName.insert(0,"")
        enName.place(x=100,y=80,anchor="w")
        
        Level=tkinter.Label(setinfo,text='等级:',font=('',10),width=10,height=1)
        Level.place(x=100,y=130,anchor="e")
        enLevel=tkinter.Entry(setinfo,show=None,width=23)
        enLevel.insert(0,"")
        enLevel.place(x=100,y=130,anchor="w")
        
        Specs=tkinter.Label(setinfo,text='规格:',font=('',10),width=10,height=1)
        Specs.place(x=100,y=180,anchor="e")
        
        Var1.set("1920x1080 16:9 60fps")
        
        enSpecs=ttk.Combobox(setinfo,width=20,textvariable=Var1,state="readonly")
        enSpecs['values']=("1920x1080 16:9 60fps",
                           "1440x1080 4:3  60fps",
                           "1580x1080 PE   60fps",
                           "3840x2160 16:9 60fps",
                           "2880x2160 4:3  60fps",
                           "3240x2160 PE   60fps",
                           "1920x1080 16:9 120fps",
                           "1440x1080 4:3  120fps",
                           "1620x1080 PE   120fps",
                           "3840x2160 16:9 120fps",
                           "2880x2160 4:3  120fps",
                           "3160x2160 PE   120fps")
        enSpecs.place(x=100,y=180,anchor="w") 
        
        ChartPath=tkinter.Label(setinfo,text='谱面文件:',font=('',10),width=10,height=1)
        ChartPath.place(x=100,y=230,anchor="e")
        enChartPath=tkinter.Entry(setinfo,show=None,width=46)
        enChartPath.insert(0,"")
        enChartPath.place(x=100,y=230,anchor="w")
        Select1=tkinter.Button(setinfo,text='选择谱面',font=('',10),width=15,height=1,
                            command=lambda:Select(1))
        Select1.place(x=560,y=230,anchor="e")
        
        PicturePath=tkinter.Label(setinfo,text='曲绘文件:',font=('',10),width=10,height=1)
        PicturePath.place(x=100,y=280,anchor="e")
        enPicturePath=tkinter.Entry(setinfo,show=None,width=46)
        enPicturePath.insert(0,"")
        enPicturePath.place(x=100,y=280,anchor="w")
        Select2=tkinter.Button(setinfo,text='选择曲绘',font=('',10),width=15,height=1,
                            command=lambda:Select(2))
        Select2.place(x=560,y=280,anchor="e")
        
        SongPath=tkinter.Label(setinfo,text='音频文件:',font=('',10),width=10,height=1)
        SongPath.place(x=100,y=330,anchor="e")
        enSongPath=tkinter.Entry(setinfo,show=None,width=46)
        enSongPath.insert(0,"")
        enSongPath.place(x=100,y=330,anchor="w")
        Select3=tkinter.Button(setinfo,text='选择音频',font=('',10),width=15,height=1,
                            command=lambda:Select(3))
        Select3.place(x=560,y=330,anchor="e")
        
        HighLight=tkinter.Label(setinfo, text='双押高亮:',font=('',10),width=10,height=1)
        HighLight.place(x=350,y=80,anchor="e")
        
        Var2.set("开启")
        
        enHighLight=ttk.Combobox(setinfo,width=5,textvariable=Var2,state="readonly")
        enHighLight['values']=("开启",
                          "关闭")
        enHighLight.place(x=350,y=80,anchor="w")
        
        LineColor=tkinter.Label(setinfo, text='判定线颜色:',font=('',10),width=10,height=1)
        LineColor.place(x=490,y=80,anchor="e")
        
        Var3.set("黄")
        
        enLineColor=ttk.Combobox(setinfo,width=5,textvariable=Var3,state="readonly")
        enLineColor['values']=("黄",
                          "白")
        enLineColor.place(x=490,y=80,anchor="w")
        
        NoteSize=tkinter.Label(setinfo, text='Note大小:',font=('',10),width=10,height=1)
        NoteSize.place(x=350,y=130,anchor="e")
        enNoteSize=tkinter.Entry(setinfo,show=None,width=8)
        enNoteSize.insert(0,"1.4 #推荐")
        enNoteSize.place(x=350,y=130,anchor="w")
        
        Blur=tkinter.Label(setinfo, text='曲绘模糊:',font=('',10),width=10,height=1)
        Blur.place(x=350,y=180,anchor="e")
        enBlur=tkinter.Entry(setinfo,show=None,width=23)
        enBlur.insert(0,"70 #推荐")
        enBlur.place(x=350,y=180,anchor="w")
        
        Sound=tkinter.Label(setinfo, text='打击音量:',font=('',10),width=10,height=1)
        Sound.place(x=490,y=130,anchor="e")
        enSound=tkinter.Entry(setinfo,show=None,width=8)
        enSound.insert(0,"35 #默认")
        enSound.place(x=490,y=130,anchor="w")
        
        done=tkinter.Button(setinfo,text='下一步',font=('',10),width=22,height=1,
                            command=lambda:infoed())
        done.place(x=300,y=370,anchor=tkinter.CENTER)
        
        superior = tkinter.Frame(base)
        
        subtitle2=tkinter.Label(superior,text="高级视频设置",font=('',12),width=30,height=1)
        subtitle2.place(x=300,y=30,anchor=tkinter.CENTER)
        
        StartAnimation=tkinter.Label(superior, text='开场动画:',font=('',10),width=10,height=1)
        StartAnimation.place(x=100,y=80,anchor="e")
        
        Var4.set("禁用")
        
        enStartAnimation=ttk.Combobox(superior,width=20,textvariable=Var4,state="readonly")
        enStartAnimation['values']=("禁用")
        enStartAnimation.place(x=100,y=80,anchor="w")
        
        EndAnimation=tkinter.Label(superior, text='结算动画:',font=('',10),width=10,height=1)
        EndAnimation.place(x=100,y=130,anchor="e")
        
        
        Var5.set("启用")
        
        enEndAnimation=ttk.Combobox(superior,width=20,textvariable=Var5,state="readonly")
        enEndAnimation['values']=("禁用","启用")
        enEndAnimation.place(x=100,y=130,anchor="w")
        
        LevelOver=tkinter.Label(superior, text='结算音乐:',font=('',10),width=10,height=1)
        LevelOver.place(x=350,y=80,anchor="e")
        
        Var6.set("IN")
        
        enLevelOver=ttk.Combobox(superior,width=5,textvariable=Var6,state="readonly")
        enLevelOver['values']=("EZ","HD","IN","AT")
        enLevelOver.place(x=350,y=80,anchor="w")
        
        DynamicScore=tkinter.Label(superior, text='动态分数:',font=('',10),width=10,height=1)
        DynamicScore.place(x=490,y=80,anchor="e")
        
        Var7.set("关闭")
        
        enDynamicScore=ttk.Combobox(superior,width=5,textvariable=Var7,state="readonly")
        enDynamicScore['values']=("开启","关闭")
        enDynamicScore.place(x=490,y=80,anchor="w")
        
        PlayerName=tkinter.Label(superior, text='玩家名称:',font=('',10),width=10,height=1)
        PlayerName.place(x=350,y=180,anchor="e")
        
        enPlayerName=tkinter.Entry(superior,show=None,width=23)
        enPlayerName.insert(0,"#玩家框还没做")
        enPlayerName.place(x=350,y=180,anchor="w")
        
        ComboText=tkinter.Label(superior, text='连击字段:',font=('',10),width=10,height=1)
        ComboText.place(x=100,y=180,anchor="e")
        
        enComboText=tkinter.Entry(superior,show=None,width=23)
        enComboText.insert(0,"COMBO")
        enComboText.place(x=100,y=180,anchor="w")
        
        APS=tkinter.Label(superior, text='理论值:',font=('',10),width=10,height=1)
        APS.place(x=350,y=130,anchor="e")
        
        enAPS=tkinter.Entry(superior,show=None,width=23)
        enAPS.insert(0,"1000000")
        enAPS.place(x=350,y=130,anchor="w")
        
        Tip=tkinter.Label(superior, text='Tip字段:',font=('',10),width=10,height=1)
        Tip.place(x=100,y=230,anchor="e")
                
        enTip=tkinter.Entry(superior,show=None,width=46)
        enTip.insert(0,"")
        enTip.place(x=100,y=230,anchor="w")
        
        Rand=tkinter.Button(superior,text='随机填充',font=('',10),width=15,height=1,
                            command=lambda:Select("Rand"))
        Rand.place(x=560,y=230,anchor="e")
        
        Select("Rand")
        
        UserIcon=tkinter.Label(superior, text='玩家头像:',font=('',10),width=10,height=1)
        UserIcon.place(x=100,y=280,anchor="e")
        
        enUserIcon=tkinter.Entry(superior,show=None,width=46)
        enUserIcon.insert(0,"Source/UserIcon.png")
        enUserIcon.place(x=100,y=280,anchor="w")
        
        Select4=tkinter.Button(superior,text='选择图片',font=('',10),width=15,height=1,
                            command=lambda:Select(4))
        Select4.place(x=560,y=280,anchor="e")
        
        VideoBackground=tkinter.Label(superior, text='视频背景:',font=('',10),width=10,height=1)
        VideoBackground.place(x=100,y=330,anchor="e")
        
        enVideoBackground=tkinter.Entry(superior,show=None,width=46)
        enVideoBackground.insert(0,"Disabled(不启用)")
        enVideoBackground.place(x=100,y=330,anchor="w")
        
        Select5=tkinter.Button(superior,text='选择视频',font=('',10),width=15,height=1,
                            command=lambda:Select(5))
        Select5.place(x=560,y=330,anchor="e")
        
        done2=tkinter.Button(superior,text='下一步',font=('',10),width=22,height=1,
                            command=lambda:infoed())
        done2.place(x=300,y=370,anchor=tkinter.CENTER)
        
        notebook.add(setinfo, text="基本视频信息")
        notebook.add(superior, text="高级视频信息")
        notebook.pack()
        notebook.configure(width=600, height=400)
        
        if item == "":
            pass
        else:
            enName.insert(0,item[0])
            enLevel.insert(0,item[4])
            enChartPath.insert(0,PEdata+item[3])
            enPicturePath.insert(0,PEdata+"Resources/"+item[2])
            enSongPath.insert(0,PEdata+"Resources/"+item[1])
        
        base.mainloop()
    
    init()
    
if __name__ == "__main__":  
    Path = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(Path)
    root=tkinter.Tk()
    root.title("PE/json Chart Renderer")
    root.geometry("400x300")
    title1=tkinter.Label(root, text='PE/json Chart Renderer 0.2.3',font=('',12),width=30,height=2)
    title1.place(relx=0.5,rely=0.1,anchor=tkinter.CENTER)
    botton1=tkinter.Button(root,text='Chart rendering',font=('',10),width=20,height=2,command=lambda:renderer("",""))
    botton1.place(relx=0.5,rely=0.33,anchor=tkinter.CENTER)
    botton2=tkinter.Button(root,text='Convert pec to json',font=('',10),width=20,height=2,command=chartify)
    botton2.place(relx=0.5,rely=0.55,anchor=tkinter.CENTER)
    title2=tkinter.Label(root, text='注：支持PE0.1.9.2的pec格式\nformatVersion3的官谱json格式',font=('',12),width=100,height=3)
    title2.place(relx=0.5,rely=0.85,anchor=tkinter.CENTER)
    root.mainloop()
