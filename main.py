import kivy
from datetime import datetime
from kivy.app import App
import threading
import time

from kivy.core.window import Window
Window.size=(500,800)
Window.clearcolor = (0/255,0/255,0/255,1)

from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager,Screen

text_count=0
text_dict={}
dply=0

class PigeonApp(App):
    def initialize(self,d):
        global dply
        dply=d

    def clear_chat(self):
        dply.clear_widgets()

    def clock(self,wd):
        global dply
        while True:
            wd.text=wd.text[:-8]+str(datetime.now())[-15:-7]
            time.sleep(1)

    def send(self,t):
        global text_count
        global text_dict
        global curr_time
        text_count=text_count+1
        tx=t.text
        if tx=="":
            return
        ssize=len(tx)*0.02+0.008
        p_id="text_"+str(text_count)
        text_dict[str(datetime.now())[:-7]]=tx
        b=BoxLayout(orientation="vertical", spacing=5,size_hint=(1,None),size=(450,50),pos_hint={'right':1, 'top':1})
        b.add_widget(Label(text="You", font_size=11,size_hint=(None,None),size=("30dp","10dp"),pos_hint={'right':1, 'top':1} ))
        b.add_widget(Button(text=tx,background_color=(235/255.0,125/255.0,103/255.0,1),font_size=18,size_hint=(ssize,None),size=(ssize,"40dp"),pos_hint={'right':1, 'top':1}))
        dply.add_widget(b)
        t.text=""

    def send2(self,t):
        tx=t.text
        if tx=="":
            return
        ssize=len(tx)*0.02+0.008
        b=BoxLayout(orientation="vertical", spacing=5,size_hint=(1,None),size=(450,50),pos_hint={'left':1, 'top':1})
        b.add_widget(Label(text="Them", font_size=11,size_hint=(None,None),size=("30dp","10dp"),pos_hint={'left':1, 'top':1} ))
        b.add_widget(Button(text=tx,background_color=(245/255.0,224/255.0,66/255.0,1),font_size=18,size_hint=(ssize,None),size=(ssize,"40dp"),pos_hint={'left':1, 'top':1}))
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
