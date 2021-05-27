import kivy
from datetime import datetime
import threading
import time
import socket
import base64

from kivy.config import Config
Config.set('graphics', 'resizable', False)
#Config.set('kivy', 'window_icon', 'Icons/top_icon.png')

from kivy.core.window import Window
from kivy.app import App
from kivy.graphics import Color,RoundedRectangle
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager,Screen

Window.size=(500,800)
Window.clearcolor = (0/255,0/255,0/255,1)

#things to change
id=0                #0 or 1 depending on person one and two. One should be 0 other 1
#things to change
sel_adr=(socket.gethostbyname(socket.gethostname()),10000)
oth_adr=(socket.gethostbyname(socket.gethostname()),10005)

if id==1:
    oth_adr=(socket.gethostbyname(socket.gethostname()),10000)
    sel_adr=(socket.gethostbyname(socket.gethostname()),10005)

cp=0
addr=0
s=socket.socket()
s.bind(sel_adr)
s.listen(1)
o=socket.socket()

text_count=0
text_dict={}
dply=0
turn=0
cp,addr=(0,0)

def connect():
    global cp
    global addr
    global o

    if id%2==0:
        print("Connecting...")
        cp,addr=s.accept()
        print("Connection accepted with "+addr[0])
        o.connect(oth_adr)
    else :
        print("Connecting...")
        o.connect(oth_adr)
        cp,addr=s.accept()
        print("Connection accepted with "+addr[0])
    print("Outgoing and incoming established with "+addr[0]+" !")
    thread1=threading.Thread(target=ronly, daemon=True)
    thread1.start()
    print("Chatting Enabled!! (!q-QUITS !c-Clear Screen)")

def ronly():
    global turn
    global text_count
    global text_dict
    global curr_time
    global dply
    global cp

    mes="asa"
    while True:
        mes=cp.recv(1024).decode()
        if mes!="!im":
            tx=mes
            text_count=text_count+1
            if tx=="":
                continue
            text_dict[str(datetime.now())[:-7]]=tx
            ssize=len(tx)*0.018+0.0012
            b=BoxLayout(orientation="vertical",spacing=2,padding=2,size_hint=(1,None),size=(450,50),pos_hint={'left':1, 'top':1})
            if turn!=2:
                b.add_widget(Label(text="Them", font_size=11,size_hint=(None,None),size=("30dp","10dp"),pos_hint={'left':1, 'top':1} ))
            b.add_widget(text_their(tx,ssize))
            dply.add_widget(b)
            turn=2
        else :
            print("Waiting for image!")
            lab="Media/"+(str(datetime.now())[-15:-7]).replace(":","_")+".jpg"
            with open(lab, "wb") as im:
                while True:
                    dat=cp.recv(1024)
                    if dat!=b'eof':
                        im.write(dat)
                    else:
                        break
                im.close()
            print("Received Image!")
            time.sleep(0.3)
            #show_r_im(lab)

def show_r_im(sr):
    b=BoxLayout(orientation="vertical", spacing=5,size_hint=(1,None),size=(450,215),pos_hint={'left':1, 'top':1})
    b.add_widget(Label(text="Them", font_size=11,size_hint=(None,None),size=("30dp","10dp"),pos_hint={'left':1, 'top':1} ))
    b.add_widget(Image(source=sr,size_hint=(None,None),size=("300dp","200dp"),pos_hint={'left':1, 'top':1}))
    dply.add_widget(b)

def sonly(tx,*f):
    global turn
    global text_count
    global text_dict
    global curr_time
    global dply
    global o

    if tx=="":
        return

    if tx!="!im":
        o.send(tx.encode())
        if tx=="eof":
            return
        ssize=len(tx)*0.018+0.0012
        text_dict[str(datetime.now())[:-7]]=tx
        b=BoxLayout(orientation="vertical",spacing=2,padding=2,size_hint=(1,None),size=(450,50),pos_hint={'right':1, 'top':1})
        if turn!=1:
            b.add_widget(Label(text="You", font_size=11,size_hint=(None,None),size=("30dp","10dp"),pos_hint={'right':1, 'top':1} ))
        b.add_widget(text_your(tx,ssize))
        dply.add_widget(b)
    elif tx=="!im":
        print("Sending Image!")
        o.send(tx.encode())
        file=open(f[0],"rb")
        chunk=file.read(1024)
        while (chunk):
            #print(chunk)
            o.send(chunk)
            chunk=file.read(1024)
        time.sleep(0.2)
        sonly("eof")
        print("Sent Image!")
    turn=1

class text_their(Button):
    def __init__(self,tx,ssize,**kwargs):
        super(text_their,self).__init__(**kwargs)
        self.text=tx
        self.background_normal='Icons/ch2.png'
        self.background_down='Icons/ch2.png'
        self.font_size=16
        self.size_hint=(ssize,None)
        self.size=(ssize,"45dp")
        self.pos_hint={'left':1, 'top':1}

class text_your(Button):
    def __init__(self,tx,ssize,**kwargs):
        super(text_your,self).__init__(**kwargs)
        self.text=tx
        self.background_normal='Icons/ch1.png'
        self.background_down='Icons/ch1.png'
        self.font_size=16
        self.size_hint=(ssize,None)
        self.size=(ssize,"45dp")
        self.pos_hint={'right':1, 'top':1}

class PigeonApp(App):
    def exit(self):
        Window.close()

    def initialize(self,d):
        global dply
        dply=d

    def con(self,t):
        global oth_adr
        global id
        if id==0:
            oth_adr=(t.text,10005)
        else :
            oth_adr=(t.text,10000)
        connect()

    def clear_chat(self):
        dply.clear_widgets()

    def clock(self,wd):
        global dply
        while True:
            wd.text=str(datetime.now())[-15:-7]
            time.sleep(1)
    
    def send(self,t):
        tx=t.text
        sonly(tx)
        t.text=""

    def send_selected(self,f):
        print(f[0])
        b=BoxLayout(orientation="vertical", spacing=5,size_hint=(1,None),size=(450,215),pos_hint={'right':1, 'top':1})
        b.add_widget(Label(text="You", font_size=11,size_hint=(None,None),size=("30dp","10dp"),pos_hint={'right':1, 'top':1} ))
        b.add_widget(Image(source=f[0],size_hint=(None,None),size=("300dp","200dp"),pos_hint={'right':1, 'top':1}))
        dply.add_widget(b)
        st=""
        #with open(f[0], "rb") as im:
            #st=base64.b64encode(im.read())
            #print(len(st))
        sonly("!im",f[0])
        print("Here Also!")

    def build(self):
        return Builder.load_file("design.kv")

PigeonApp().run()
print("Exitted!")
