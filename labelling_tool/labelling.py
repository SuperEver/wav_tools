#!/usr/bin/env python
# coding: utf-8
import os
import time

from Tkinter import *
import tkFileDialog
import tkMessageBox
import ttk

import argparse
import logging
import ConfigParser as configparser
import pyaudio
import wave
import threading

reload(sys)
sys.getdefaultencoding()
sys.setdefaultencoding("utf8")


class Player(threading.Thread): #The timer class is derived from the class threading.Thread
    def __init__(self, wav_path):
        threading.Thread.__init__(self)
        self._wav_path = wav_path
        self._play = True

    def run(self): #Overwrite run() method, put what you want the thread do here
        # define stream chunk
        chunk = 1024
        # open a wav format music
        f = wave.open(self._wav_path, 'rb')
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
        while data and self._play:
            stream.write(data)
            data = f.readframes(chunk)
        # stop stream
        stream.stop_stream()
        stream.close()
        # close PyAudio
        p.terminate()

    def stop(self):
        self._play = False


def read_conf(conf_path):
    if not os.path.exists(conf_path):
        tkMessageBox.showinfo(message='%s not found' % conf_path)
        sys.exit(1)
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
    parser.add_argument('-ws', '--window_size', type=str, default="1200x800")
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

def set_wav_path():
    global g_wav_list
    global g_wav_folder
    global g_wav_fn
    global logger

    wav_listbox.delete(0, END)
    path_entry.delete(0, END)
    g_wav_fn = ''
    g_wav_folder = tkFileDialog.askdirectory()
    path_entry.insert(0, g_wav_folder)
    g_wav_list = getWavList(g_wav_folder)

    if len(g_wav_list) == 0:
        tkMessageBox.showinfo(message='No wav files found')
        return

    for x in range(0, len(g_wav_list)):
        wav_listbox.insert(END, str(x) + "--" + g_wav_list[x])
    wav_listbox.bind('<ButtonRelease-1>', play)

    log_txtbx['state'] = 'normal'
    # 加载第一首歌曲, 和下一首歌
    g_wav_fn=g_wav_list[0]
    log_txtbx.insert(END, "音频加载完成\n")
    log_txtbx.see(END)
    log_txtbx['state'] = 'disabled'

def modified_text(event):
    log_txtbx['state'] = 'normal'
    log_txtbx.see(END)
    log_txtbx['state'] = 'disabled'


def play(event):
    global g_wav_folder
    global g_wav_fn
    global logger
    global g_wav_list
    global g_player

    n = int(wav_listbox.curselection()[0])
    g_wav_fn = g_wav_list[n]

    wav_abs = os.path.join(g_wav_folder, g_wav_fn)
    if g_player is not None:
        g_player.stop()
        g_player.join()
    g_player = Player(wav_abs)
    g_player.start()


def on_label(str_label1):
    global g_wav_fn
    global logger
    global g_player

    if g_player is not None:
        g_player.stop()
        g_player.join()
        g_player = None

    if g_wav_fn == '':
        tkMessageBox.showinfo(message='No wav selected')
        return

    log_txtbx['state'] = 'normal'
    logger.info("WAV:%s LAB:%s" % (g_wav_fn, str_label1))
    log_txtbx.insert(END, "%s : %s\n" % (str_label1, g_wav_fn))
    log_txtbx.see(END)
    log_txtbx['state'] = 'disabled'


if __name__ == "__main__":
    # 获得当前时间
    ticks = time.time()
    localtime = time.localtime(ticks)
    str_date = time.strftime("%Y%m%d-%H%M%S", localtime)

    # 全局变量
    path_cwd = os.getcwd()
    pos_st = path_cwd.find('labelling.app/Contents/Resources')
    if pos_st > 0:
        path_cwd = path_cwd[0:pos_st]
    g_log_folder = os.path.join(path_cwd, 'log')
    if not os.path.exists(g_log_folder):
        os.makedirs(g_log_folder)
    g_wav_list = [] #记录输入音频的list
    g_wav_fn = "" # 当前音频
    gLog=os.path.join(g_log_folder, str_date + ".log")
    # 配置日志文件
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(message)s",\
            datefmt='%d %b %Y %H:%M:%S', filename=gLog, filemode='a')
    logger = logging.getLogger(__name__)

    # 读取参数配置
    args = parse_arguments()
    label_list = read_conf(os.path.join(path_cwd, args.config))
    # player
    g_player = None

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
    path_entry = Entry(input_frame, textvariable = var, width=40)
    var.set("请输入音频地址")
    path_entry.grid(row=0, column=0, padx=0, pady=0, sticky=NSEW)
    bt_choose = ttk.Button(input_frame, text="选择音频目录", command = set_wav_path, style='red/black.TButton')
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
    #button_ok = ttk.Button(fm11, text="开始", width=10, command=start, style='red/black.TButton')
    #button_ok = Button(fm11, text="开始", width=10, command=start)
    #button_ok.grid(row=0, column=1, padx=0, pady=0)

    var2 = StringVar()
    wav_listbox = Listbox(fm12,  listvariable = var2, height=35, width=40)

    scrl = Scrollbar(fm1)
    wav_listbox.configure(yscrollcommand = scrl.set)
    wav_listbox.grid(row=0, column=0, padx=20, pady=0)
    scrl.grid(row=0, column=1, padx=20, pady=0)
    scrl['command'] = wav_listbox.yview

    # 按钮
    btn_label = Label(fm21, justify='left', text="标注：").grid(row=0, column=0, padx=0, pady=0, sticky=NW)
    for i, str_label in enumerate(label_list):
        bt = ttk.Button(fm22, text=str_label, width=10, command= lambda arg1=str_label: on_label(arg1),
                    style='blue/black.TButton')
        bt.grid(row=i, column=0, padx=0, pady=10)

    # 状态显示
    Label(fm31, text="日志：").grid(row=0, column=0, padx=0, pady=0)
    log_txtbx = Text(fm32, height=35, width=40, state=NORMAL, relief='solid')

    scrl2 = Scrollbar(fm3)

    log_txtbx.configure(yscrollcommand = scrl2.set)
    scrl2['command'] = log_txtbx.yview
    log_txtbx.bind('<<Modified>>', modified_text)

    log_txtbx.grid(row=0, column=0, padx=20, pady=0, sticky=NSEW)
    scrl2.grid(row=0, column=1, padx=20, pady=0, sticky=NSEW)
    log_txtbx['state']= 'disabled'

    root.mainloop()

