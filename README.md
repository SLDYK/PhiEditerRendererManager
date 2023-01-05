# Phigros自制谱面（PEC）录制器

## 如何使用？

### Win
进入QQ群695269639下载"群文件-录制器打包版"下载已打包版本或下载release中的打包版本（也许以后会有）。

解压后打开RendererUI.exe（打开速度较慢，请耐心等待，也许以后会有改善）。

<img alt="截屏" src="https://i.postimg.cc/sxrDWxFC/2023-01-03-9-06-31.png">

点击Chart renderering进入settings页面。

<img alt="截屏" src="https://i.postimg.cc/pTghXVcj/2023-01-03-8-46-50.png">

填入你的谱面信息，选择需要的帧率、分辨率并填入你的谱面文件、音频文件、曲绘文件位置,点击下一步。

<img alt="截屏" src="https://i.postimg.cc/J7kHYJt5/2023-01-03-8-47-06.png">

等待谱面渲染完成。

<img alt="截屏" src="https://i.postimg.cc/J0ZyywS2/2023-01-03-8-47-32.png">

在export文件夹获取你的文件。

详细说明见解压后的"PhiEditer_Renderer使用说明"。

### Mac/linux
Mac因未知原因，打包后无法打开

> 详见https://github.com/SLDYK/Renderer/issues/2

加上对linux的兼容性考虑，因而没有打包版，请参照"开发"板块完成配置后在终端定位到你的Renderer文件夹并依据你的python版本输入

> python RendererUI.py 或 python3 RendererUI.py

接下来的操作同Win。

## 开发

### 安装依赖

请保证你的电脑安装了Python或python3

使用"git clone"拉取仓库，使用命令行定位到到"你拉取的仓库/Renderer"，安装依赖

> pip（或pip3）install -r requirements.txt

### ffmpeg和ffprobe配置

由于程序中调用了需要ffmpeg和ffprobe的函数，请按以下方法配置

**Win**

请将"你拉取的仓库/ffmpeg配置/Win"目录下所有文件复制到"你拉取的仓库/Renderer"目录下

**Mac/linux**

请将"你拉取的仓库/ffmpeg配置/其他"目录下所有文件复制到"你拉取的仓库/Renderer"目录下

打开"你拉取的仓库/Renderer/FFM.py"

将class ffmpeg下的__init__函数参数excutable值和class ffprobe下的__init__函数参数excutable值去除".exe"并保存

<img alt="截屏" src="https://i.postimg.cc/02HcZ9qC/2023-01-05-9-18-04.png">

<img alt="截屏" src="https://i.postimg.cc/Y95mjycY/2023-01-05-9-18-22.png">

若linux用户仍无法使用，请按照以下方法进行下载和配置：

> 安装brew（已安装可以跳过），
>
> 在命令行使用
>
>> brew install ffmpeg
>
> 和
>
>> brew install ffprobe
>
> 安装ffmpeg和ffprobe（已安装可以跳过）。
>
> 安装完成后，在brew的程序包安装位置找到ffmpeg和ffprobe的可执行文件并复制到"你拉取的仓库/Renderer"目录下
>
> 如仍无法使用请加入QQ群695269639附上所有操作截图进行反馈。

### 至此

Mac/linux用户可以直接参照"如何使用"打开软件进行操作。

开发者可以打开脚本文件，开始你的编辑！