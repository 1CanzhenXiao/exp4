import wave
import pyaudio
from aip import AipSpeech
from tkinter import *

APP_ID = '29011682'
API_KEY = 'fn97LkBQZNfVVrBaNvotwfM0'
SECRET_KEY = 'YUp4TGc2TyyNIv6Y84Etybva9mWS9QoU'
CHUNK = 1024
FORMAT = pyaudio.paInt16 # 16位深
CHANNELS = 1 #1是单声道，2是双声道。
RATE = 16000 # 采样率，调用API一般为8000或16000
RECORD_SECONDS = 4 # 录制时间4s
filepath = 'resources/temp.wav'
root = Tk()
root.resizable(width=False, height=False)
root.title('语音识别控制风扇开关')
closeF = [PhotoImage(file='resources/fan.gif', format='gif -index %i' % 0)]
openF = [PhotoImage(file='resources/fan1.gif', format='gif -index %i' % 0)]

def save_wave_file(pa, filepath, data):
    wf = wave.open(filepath, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pa.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(data))
    wf.close()

def get_audio(filepath):
    with open(filepath, 'rb') as fp:
        return fp.read()

def create_audio(filepath):
    pa = pyaudio.PyAudio()
    stream = pa.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)  # 读取chunk个字节 保存到data中
        frames.append(data)  # 向列表frames中添加数据data
    stream.stop_stream()
    stream.close()  # 停止数据流
    pa.terminate()  # 关闭PyAudio
    save_wave_file(pa, filepath, frames) #写入录音文件

    # 开始识别
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result = client.asr(get_audio(filepath), 'wav', 16000, {'dev_pid': 1537, })
    if result and result['err_no'] == 0:
        r = result['result'][0]
        print(result)
        if r in ["开机。", "开启风扇。", "启动。", "开始。", "开。", "打开。"]:
            label.configure(image=openF[0])
            print()
        elif r in ["关机。", "关闭风扇。", "结束。", "关。", "关风扇。", "关闭。"]:
            label.configure(image=closeF[0])
            print()
        else:
             print('请重新输入语音')
    else:
        print('请重新输入语音')

label = Label(root)
label.configure(image=closeF[0])
label.pack()
buttons = Frame(root, height=40)
buttons.pack(side='bottom')
Button(buttons, text='输入语音并识别', width=20, command= lambda : create_audio(filepath)).pack(side='left', padx=100)
root.mainloop()