import os
from win10toast_click import ToastNotifier

def open_folder():
    os.startfile('C:\\Users\\YourName\\Documents')

toaster = ToastNotifier()
toaster.show_toast("这是一个测试消息", "点击打开文件夹", icon_path="Source/R.ico", duration=1, callback_on_click=open_folder)
