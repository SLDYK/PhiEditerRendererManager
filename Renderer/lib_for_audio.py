# -*- coding: utf-8 -*-
import os
from pydub import AudioSegment
from lib_for_video import beat2msec
import FFM as ffmpy
 
cur_path = os.path.dirname(__file__)

def audio2wav(path: str,songName):
    extension = os.path.splitext(path)[1].replace(".","")
    audio = AudioSegment.from_file(path, format=extension)
    # 保存为 WAV 格式
    export_path ="tmp/"+songName+" Song.wav"
    audio.export(export_path, format="wav")
    
def PhiAudio(audioPath, hitsoundlist, bpm, hitsoundoffset, musicoffset, length,var,showframe,sound_Level):
    musicoffset = -musicoffset
    output = AudioSegment.silent(duration=length * 1000)
    music = AudioSegment.from_wav(audioPath)
    
    tap = AudioSegment.from_wav('Source/hitsound/HitSong0.wav')
    drag = AudioSegment.from_wav('Source/hitsound/HitSong1.wav')
    flick = AudioSegment.from_wav('Source/hitsound/HitSong2.wav')
    
    # print(hitsoundlist)
    for i in range(0, len(hitsoundlist)):
        var.set("正在生成音频 "+str(round(100*i/len(hitsoundlist),2))+"%")
        showframe.update()
        currentNote = hitsoundlist[i][1]
        currentBeat = hitsoundlist[i][0]
        if currentNote == 1 or currentNote == 3:
            sound = tap.apply_gain((sound_Level-50)/2)
        elif(currentNote == 2):
            sound = drag.apply_gain((sound_Level-50)/2)
        else:
            sound = flick.apply_gain((sound_Level-50)/2)
        output = output.overlay(sound, position=beat2msec(currentBeat, bpm, hitsoundoffset))
    
    print("音频生成成功")
    export_path = audioPath[0:-8]+"HitSound.wav"
    
    output.export(export_path, format="wav")  # 保存文件
    if(musicoffset < 0):
        music = music[-musicoffset: length * 1000]
        output = output.overlay(music, position=0)
    else:
        output = output.overlay(music, position=musicoffset)
    export_path = audioPath[0:-8]+"ComposedAudio.wav"
        
    output.export(export_path, format="wav")
# =============================================================================
# def video_add_audio(video_path: str, audio_path: str, output_dir: str, videoname: str):
# 
#     _ext_audio = os.path.basename(audio_path).strip().split('.')[-1]
#     if _ext_audio not in ['mp3', 'wav']:
#         raise Exception('audio format not support')
#     _codec = 'copy'
#     if _ext_audio == 'wav':
#         _codec = 'aac'
#     result = os.path.join(output_dir, videoname)
#     ff = ffmpy.FFmpeg(
#         inputs={video_path: None, audio_path: None},
#         outputs={result: '-map 0:v -map 1:a -c:v copy -c:a {} -y'.format(_codec)})
#     ff.run()
#     return result
# =============================================================================

def video_add_audio(video_path: str, audio_path: str, output_dir: str, videoname: str):
    _ext_audio = os.path.basename(audio_path).strip().split('.')[-1]
    if _ext_audio not in ['mp3', 'wav']:
        raise Exception('audio format not support')
    _codec = 'copy'
    if _ext_audio == 'wav':
        _codec = 'aac'
    result = os.path.join(output_dir, videoname)
    ff = ffmpy.FFmpeg(
        inputs={video_path: None, audio_path: None},
        outputs={result: '-map 0:v -map 1:a -c:v copy -c:a {} -b:a 320k -y'.format(_codec)})
    ff.run()
    return result


def merge_videos(video1_path:str, video2_path:str, export_folder:str, export_name:str):
    ff = ffmpy.FFmpeg(
        inputs={video1_path: None, video2_path: None},
        outputs={f"{export_folder}/{export_name}.mp4": "-filter_complex '[0:v] [0:a] [1:v] [1:a] concat=n=2:v=1:a=1' -f mp4 -q:v 0 -preset ultrafast"}
    )
    import subprocess
    ff.run(stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#def video_add_audio(video_path: str, audio_path: str, output_dir: str, videoname: str, progress_var: tkinter.StringVar):

#    _ext_audio = os.path.basename(audio_path).strip().split('.')[-1]
#    if _ext_audio not in ['mp3', 'wav']:
#        raise Exception('audio format not support')
#    _codec = 'copy'
#    if _ext_audio == 'wav':
#        _codec = 'aac'
#    result = os.path.join(output_dir, videoname)
#    
#    ff = FfmpegProgress(
#        inputs={video_path: None, audio_path: None},
#        outputs={result: '-map 0:v -map 1:a -c:v copy -c:a {} -y'.format(_codec)})
#    
#    for progress in ff.run_command_with_progress():
#        progress_var.set(progress)
    
#    return result
