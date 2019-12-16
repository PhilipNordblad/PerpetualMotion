# ////////////////////////////////////////////////////////////////
# //                     IMPORT STATEMENTS                      //
# ////////////////////////////////////////////////////////////////

import math
import sys
import time
import threading

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import *
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.animation import Animation
from functools import partial
from kivy.config import Config
from kivy.core.window import Window
from pidev.kivy import DPEAButton
from pidev.kivy import PauseScreen
from time import sleep
import RPi.GPIO as GPIO 
from pidev.stepper import stepper
from pidev.Cyprus_Commands import Cyprus_Commands_RPi as cyprus


# ////////////////////////////////////////////////////////////////
# //                      GLOBAL VARIABLES                      //
# //                         CONSTANTS                          //
# ////////////////////////////////////////////////////////////////
ON = False
OFF = True
HOME = True
TOP = False
OPEN = False
CLOSE = True
YELLOW = .180, 0.188, 0.980, 1
BLUE = 0.917, 0.796, 0.380, 1
DEBOUNCE = 0.1
INIT_RAMP_SPEED = 150
RAMP_LENGTH = 725


# ////////////////////////////////////////////////////////////////
# //            DECLARE APP CLASS AND SCREENMANAGER             //
# //                     LOAD KIVY FILE                         //
# ////////////////////////////////////////////////////////////////
class MyApp(App):
    def build(self):
        self.title = "Perpetual Motion"
        return sm

Builder.load_file('main.kv')
Window.clearcolor = (.1, .1,.1, 1) # (WHITE)

cyprus.open_spi()

# ////////////////////////////////////////////////////////////////
# //                    SLUSH/HARDWARE SETUP                    //
# ////////////////////////////////////////////////////////////////
sm = ScreenManager()
ramp = stepper(port = 0, speed = INIT_RAMP_SPEED)
cyprus.initialize()
cyprus.setup_servo(1)

# ////////////////////////////////////////////////////////////////
# //                       MAIN FUNCTIONS                       //
# //             SHOULD INTERACT DIRECTLY WITH HARDWARE         //
# ////////////////////////////////////////////////////////////////
	
# ////////////////////////////////////////////////////////////////
# //        DEFINE MAINSCREEN CLASS THAT KIVY RECOGNIZES        //
# //                                                            //
# //   KIVY UI CAN INTERACT DIRECTLY W/ THE FUNCTIONS DEFINED   //
# //     CORRESPONDS TO BUTTON/SLIDER/WIDGET "on_release"       //
# //                                                            //
# //   SHOULD REFERENCE MAIN FUNCTIONS WITHIN THESE FUNCTIONS   //
# //      SHOULD NOT INTERACT DIRECTLY WITH THE HARDWARE        //
# ////////////////////////////////////////////////////////////////
class MainScreen(Screen):
    version = cyprus.read_firmware_version()
    staircaseSpeedText = '0'
    rampSpeed = INIT_RAMP_SPEED
    staircaseSpeed = 40
    staircase = False
    staircase_speed = 10000

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.initialize()


    def toggleGate(self):


        print("Open and Close gate here")

    def toggleStaircase(self):

        self.staircase = not self.staircase

        if self.staircase:
            print(self.staircase)
            cyprus.set_pwm_values(1, period_value = 100000, compare_value = self.staircase_speed, compare_mode = cyprus.LESS_THAN_OR_EQUAL)

        else:
            print(self.staircase)
            cyprus.set_pwm_values(1, period_value = 100000, compare_value = 0, compare_mode = cyprus.LESS_THAN_OR_EQUAL)

        print("Turn on and off staircase here")

    def toggleRamp(self):


        print("Move ramp up and down here")
        
    def auto(self):
        print("Run through one cycle of the perpetual motion machine")
        
    def setRampSpeed(self, speed):
        print("Set the ramp speed and update slider text")
        
    def setStaircaseSpeed(self, speed):

        self.staircase_speed = 100 * speed
        self.ids.StaircaseSpeed.text = "Staircase Speed: " + str(self.staircase_speed)
        if self.staircase:
            cyprus.set_pwm_values(1,period_value= 1000, compare_value= 100 * speed, compare_mode= cyprus.LESS_THAN_OR_EQUAL)

        print("Set the staircase speed and update slider text")
        
    def initialize(self):

        cyprus.setup_servo(1)


        print("Close gate, stop staircase and home ramp here")

    def resetColors(self):
        self.ids.gate.color = YELLOW
        self.ids.staircase.color = YELLOW
        self.ids.ramp.color = YELLOW
        self.ids.auto.color = BLUE
    
    def quit(self):
        print("Exit")
        MyApp().stop()

sm.add_widget(MainScreen(name = 'main'))

# ////////////////////////////////////////////////////////////////
# //                          RUN APP                           //
# ////////////////////////////////////////////////////////////////

MyApp().run()
cyprus.close_spi()
