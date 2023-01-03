# Phigros自制谱面（PEC）录制器

## 如何使用？

### Win
进入qq群695269639下载群文件-录制器本体下载已打包版本或下载release中的打包版本（也许以后会有）
<img alt="截屏" src="https://i.postimg.cc/sxrDWxFC/2023-01-03-9-06-31.png">

解压后打开RendererUI.exe（打开速度较慢，请耐心等待，也许以后会有改善）

<img alt="截屏" src="https://i.postimg.cc/pTghXVcj/2023-01-03-8-46-50.png">

点击Chart renderering进入settings页面，填入你的谱面信息，选择需要的帧率、分辨率并填入你的谱面文件、音频文件、曲绘文件位置

<img alt="截屏" src="https://i.postimg.cc/J7kHYJt5/2023-01-03-8-47-06.png">

点击下一步，等待谱面渲染完成。

<img alt="截屏" src="https://i.postimg.cc/J0ZyywS2/2023-01-03-8-47-32.png">

在export文件夹获取你的文件

详见解压后的"PhiEditer_Renderer使用说明"

### Mac
Mac因未知原因，打包后无法打开

> 详见https://github.com/SLDYK/Renderer/issue/2

因而没有打包版，请参照"开发"板块完成依赖安装后在终端定位到你的Renderer文件夹并依据你的python版本输入

> python RendererUI.py 或 python3 RendererUI.py

接下来的操作同Win。

## 开发
请保证你的电脑安装了Python或python3
使用"git clone"拉取仓库，使用命令行定位到到你拉取的仓库/Renderer，使用安装依赖

> pip（或pip3）install -r requirements.txt

Mac用户可以直接参照"如何使用"打开软件进行操作。
开发者可以打开脚本文件，开始你的编辑！