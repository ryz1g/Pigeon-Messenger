import kivy
from datetime import datetime
import threading
import time

from kivy.config import Config
Config.set('graphics', 'resizable', False)

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

text_count=0
text_dict={}
dply=0

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

    def clear_chat(self):
        dply.clear_widgets()

    def clock(self,wd):
        global dply
        while True:
            wd.text=str(datetime.now())[-15:-7]
            time.sleep(1)
    """
    def tb_press(self,ind):
        global text_dict
        self.ids.t_input=text_dict[ind]

    def show_texts(self):
        global text_dict
        print(text_dict)

    def ycam_press(self):
        c=self.ids.your_cam
        if c.play:
            c.play=False
            #c.texture="images/im1.jpg"
        else:
            c.play=True
            #c.source=""
    """
    def send(self,t):
        global text_count
        global text_dict
        global curr_time
        text_count=text_count+1
        tx=t.text
        if tx=="":
            return
        ssize=len(tx)*0.018+0.0012
        text_dict[str(datetime.now())[:-7]]=tx
        b=BoxLayout(orientation="vertical", spacing=2,size_hint=(1,None),size=(450,50),pos_hint={'right':1, 'top':1})
        b.add_widget(Label(text="You", font_size=11,size_hint=(None,None),size=("30dp","10dp"),pos_hint={'right':1, 'top':1} ))
        b.add_widget(text_your(tx,ssize))
        dply.add_widget(b)
        t.text=""

    def send2(self,t):
        global text_count
        global text_dict
        global curr_time
        text_count=text_count+1
        tx=t.text
        if tx=="":
            return
        text_dict[str(datetime.now())[:-7]]=tx
        ssize=len(tx)*0.018+0.0012
        b=BoxLayout(orientation="vertical", spacing=2,size_hint=(1,None),size=(450,50),pos_hint={'left':1, 'top':1})
        b.add_widget(Label(text="Them", font_size=11,size_hint=(None,None),size=("30dp","10dp"),pos_hint={'left':1, 'top':1} ))
        b.add_widget(text_their(tx,ssize))
        dply.add_widget(b)
        t.text=""

    def send_selected(self,f):
        print(f[0])
        b=BoxLayout(orientation="vertical", spacing=5,size_hint=(1,None),size=(450,215),pos_hint={'right':1, 'top':1})
        b.add_widget(Label(text="You", font_size=11,size_hint=(None,None),size=("30dp","10dp"),pos_hint={'right':1, 'top':1} ))
        b.add_widget(Image(source=f[0],size_hint=(None,None),size=("300dp","200dp"),pos_hint={'right':1, 'top':1}))
        dply.add_widget(b)
        print("Here Also!")

    def build(self):
        return Builder.load_file("design.kv")

PigeonApp().run()
