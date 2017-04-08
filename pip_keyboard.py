import colorsys
from random import random

import keyboard

from razer_keyboard.color import Color
from razer_keyboard.keyboard import Keyboard, create_color_store
from razer_keyboard.maps import *



razerBoard = Keyboard()

def on_press(event):
    c = Color(*map(lambda x: int(x * 255), colorsys.hsv_to_rgb(random(), 1, 1)))
    razerBoard.set_key(pip_keyboard_to_keymap[event.scan_code], c)
    razerBoard.write_keys()

def on_release(event):
    razerBoard.set_key(pip_keyboard_to_keymap[event.scan_code], Color(0, 0, 0))
    razerBoard.write_keys()

keyboard.on_press(on_press)
keyboard.on_release(on_release)

import time

time.sleep(100000)