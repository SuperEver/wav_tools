#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2018 Baidu Inc. All rights reserved.
# filename : check-cfy_v2.py
# author   : Wangjianfei, Leikang
# date     : 2018-10-19

import os
import time

from Tkinter import *
import tkFileDialog
import ttk

import argparse
import logging
import ConfigParser as configparser
import pyaudio
import wave

reload(sys)
sys.getdefaultencoding()
sys.setdefaultencoding("utf8")


def play_wav(wav_path):
    # define stream chunk
    chunk = 1024
    # open a wav format music
    f = wave.open(wav_path, 'rb')
    # instantiate PyAudio
    p = pyaudio.PyAudio()
    # open stream
    stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                    channels=f.getnchannels(),
                    rate=f.getframerate(),
                    output=True)
    # read data
    data = f.readframes(chunk)

    # play stream
    while data:
        stream.write(data)
        data = f.readframes(chunk)
    # stop stream
    stream.stop_stream()
    stream.close()

    # close PyAudio
    p.terminate()

def read_conf(conf_path):
    cp = configparser.ConfigParser()
    cp.read(conf_path)
    default_section = cp.options('labels')
    label_list = []
    for str_key in default_section:
        label_list.append(cp.get('labels', str_key))
    return label_list


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--title', type=str, default="Wash Data Application")
    parser.add_argument('-ws', '--window_size', type=str, default="1500x1000")
    parser.add_argument('-ld', '--log_dir', type=str, default="log")
    parser.add_argument('--config', type=str, default='config.ini')
    args = parser.parse_args()
    return args

def getWavList(path):
    wl=[]
    for root, dirs, files in os.walk(path):
        files.sort()
        for f in files:
            if f.split(".")[-1] == "wav":
                wl.append(f)
    return wl

def addWavPath():
    global gWavList
    global gWavNum
    global gPath

    gPath = tkFileDialog.askdirectory()
    e.delete(0, END)
    e.insert(0, gPath)
    gWavList = getWavList(gPath)
    gWavNum = len(gWavList)

    for x in range(0, gWavNum):
        lb.insert(END, str(x) + "--" + gWavList[x])
    lb.bind('<ButtonRelease-1>', play)

def modified_text(event):
    log_txtbx['state'] = 'normal'
    log_txtbx.see(END)
    log_txtbx['state'] = 'disabled'

def start():
    global gWavList
    global gWavNum
    global gWav
    global gLog
    global gLogger
    log_txtbx['state'] = 'normal'

    # 配置日志文件
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(message)s",\
            datefmt='%d %b %Y %H:%M:%S', filename=gLog, filemode='a')
    gLogger = logging.getLogger(__name__)

    # 加载第一首歌曲, 和下一首歌
    if gWavNum == 0:
        log_txtbx.insert(END, "请先输入音频文件\n")
        log_txtbx.see(END)
        log_txtbx['state'] = 'disabled'
        return
    elif gWavNum == 1:
        gWav=gWavList[0]
    else:
        gWav=gWavList[0]

    log_txtbx.insert(END, "歌曲加载成功，请开始\n")
    log_txtbx.see(END)
    log_txtbx['state'] = 'disabled'

def play(event):
    global gPath
    global gWav
    global gLogger
    global gWavList
    log_txtbx['state'] = 'normal'

    if gLogger == "":
        log_txtbx.insert(END, "请先按<开始>按钮\n")
        log_txtbx.see(END)
        log_txtbx['state'] = 'disabled'
        return

    n = int(lb.curselection()[0])
    gWav = gWavList[n]
    #gWav = re.search(r"\w(.*?)",lb.get(lb.curselection())).group(1)

    log_txtbx.insert(END, ("play " + gWav + "\n"))
    log_txtbx.see(END)
    wav_abs = os.path.join(gPath, gWav)
    play_wav(wav_abs)
    log_txtbx['state'] = 'disabled'


def on_label(str_label1):
    global gWav
    global gLogCache
    global gLogger

    if gWavNum == 0 or gWav == '':
        return start()

    log_txtbx['state'] = 'normal'

    if gLogger == "":
        log_txtbx.insert(END, "请先按<开始>按钮\n")
        log_txtbx.see(END)
        log_txtbx['state'] = 'disabled'
        return

    gLogCache[gWav]=str_label1
    for wav, label in gLogCache.items():
        gLogger.info("WAV:%s LAB:%s" % (wav, label))
    gLogCache.clear()
    log_txtbx.insert(END, "%s : %s\n" % (str_label1, gWav))
    log_txtbx.see(END)
    log_txtbx['state'] = 'disabled'


if __name__ == "__main__":
    # 获得当前时间
    ticks = time.time()
    localtime = time.localtime(ticks)
    date = time.strftime("%Y%m%d-%H%M%S", localtime)

    # 读取参数配置
    args = parse_arguments()

    label_list = read_conf(args.config)

    # 全局变量
    gPath = os.getcwd() #音频存放位置
    gPath = gPath + '/log/'
    if not os.path.exists(gPath):
        os.makedirs(gPath)

    gWavList = [] #记录输入音频的list
    gWavNum = 0 #记录输入音频的数值
    gWav = "" # 当前音频
    gLog=os.path.join(gPath,date+".log")
    gLogCache={}
    gLogger=""

    # 进入消息循环
    root = Tk()
    root.title(args.title)
    root.geometry(args.window_size)
    ttk.Style().configure('red/black.TButton', foreground='red', background='black', font=('Helvetica', 20))
    ttk.Style().configure('blue/black.TButton', foreground='blue', background='black', font=('Helvetica', 16))


    # 输入框Frame
    frame = Frame(root)#, height=400, width=400)
    frmT = Frame(root, bd=2, height=2, width=40)#, width=400, height=10)
    frmB = Frame(root, bd=2)#, width=400, height=390)
    frmT.grid(row=0, column=0, padx=20, pady=20, sticky=NSEW)
    frmB.grid(row=1, column=0, padx=20, pady=20, sticky=NSEW)


    input_frame = frmT

    var = StringVar()
    e = Entry(input_frame, textvariable = var, width=40)
    var.set("请输入音频地址")
    e.grid(row=0, column=0, padx=0, pady=0, sticky=NSEW)
    bt_choose = ttk.Button(input_frame, text="选择音频", command = addWavPath, style='red/black.TButton')
    bt_choose.grid(row=0, column=1, padx=0, pady=0, sticky=NSEW)


    # 三列: 文件列表，标注按钮，日志显示
    fm1 = Frame(frmB, bd=2,height=800,width=350)#, relief="solid")#, width=180, height=390)
    fm2 = Frame(frmB, bd=2,height=800,width=50)#, width=80, height=390)
    fm3 = Frame(frmB, bd=2,height=800,width=350, relief="solid")#, relief="solid")#, width=180, height=390)
    Grid.columnconfigure(fm3, 0, weight=1)

    fm1.grid(row=0, column=0, padx=0, pady=0, sticky=NSEW)
    fm2.grid(row=0, column=1, padx=0, pady=0)
    fm3.grid(row=0, column=2, padx=50, pady=0, sticky=NSEW)

    fm11 = Frame(fm1)#, width=180, height=20)
    fm12 = Frame(fm1)#, width=180, height=360)
    fm11.grid(row=0, column=0, padx=0, pady=0, sticky=NW)
    fm12.grid(row=1, column=0, padx=0, pady=0, sticky=NW)

    fm21 = Frame(fm2)#, width=80, height=20)
    fm22 = Frame(fm2, bd=2, relief="solid")#, width=80, height=360)
    fm21.grid(row=0, column=0, padx=0, pady=0, sticky=NW)
    fm22.grid(row=1, column=0, padx=0, pady=0)

    fm31 = Frame(fm3)#, width=180, height=20)
    fm32 = Frame(fm3, relief="solid")#, width=180, height=360)
    fm31.grid(row=0, column=0, padx=0, pady=0, sticky=NW)
    fm32.grid(row=1, column=0, padx=0, pady=0, sticky=S)


    list_label = Label(fm11, justify='left', text="列表栏：").grid(row=0, column=0, padx=0, pady=0, sticky=NW)
    button_ok = ttk.Button(fm11, text="开始", width=10, command=start, style='red/black.TButton')
    #button_ok = Button(fm11, text="开始", width=10, command=start)
    button_ok.grid(row=0, column=1, padx=0, pady=0)

    var2 = StringVar()
    lb = Listbox(fm12,  listvariable = var2, height=35, width=40)

    scrl = Scrollbar(fm1)
    lb.configure(yscrollcommand = scrl.set)
    lb.grid(row=0, column=0, padx=20, pady=0)
    scrl.grid(row=0, column=1, padx=20, pady=0)
    scrl['command'] = lb.yview

    # 按钮
    btn_label = Label(fm21, justify='left', text="标注：").grid(row=0, column=0, padx=0, pady=0, sticky=NW)
    for i, str_label in enumerate(label_list):
        bt = ttk.Button(fm22, text=str_label, width=10, command= lambda arg1=str_label: on_label(arg1),
                    style='blue/black.TButton')
        bt.grid(row=i, column=0, padx=0, pady=10)

    # 状态显示
    Label(fm31, text="状态栏：").grid(row=0, column=0, padx=0, pady=0)
    log_txtbx = Text(fm32, height=35, width=40, state=NORMAL, relief='solid')

    scrl2 = Scrollbar(fm3)

    log_txtbx.configure(yscrollcommand = scrl2.set)
    scrl2['command'] = log_txtbx.yview
    log_txtbx.bind('<<Modified>>', modified_text)

    log_txtbx.grid(row=0, column=0, padx=20, pady=0, sticky=NSEW)
    scrl2.grid(row=0, column=1, padx=20, pady=0, sticky=NSEW)
    log_txtbx.insert(END, '你好\n')
    log_txtbx['state']= 'disabled'

    root.mainloop()

