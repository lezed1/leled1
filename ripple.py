from collections import defaultdict
import colorsys
from random import randint, randrange, random

from pynput import keyboard

from razer_keyboard.color import Color
from razer_keyboard.keyboard import Keyboard
import maps


razerBoard = Keyboard()

keys = (k for k in maps.keymap.keys())
ck = keys.__next__()
nkeys = defaultdict(list)

def on_press(key):
    # print(key)
    global ck
    try:
        # print('alphanumeric key {0} pressed'.format(key.char))
        k = key.char
        
    except AttributeError:
        # print('special key {0} pressed'.format(key))
        k = key.name
        if k == "enter":
            try:
                # ck = keys.__next__()
                print("###")
                print(ck)
            except:
                print(nkeys)
                return False
        # return


    print("'{}'".format(k))
    nkeys[ck].append(k)

    c = Color(*map(lambda x: int(x * 255), colorsys.hsv_to_rgb(random(), 1, 1)))
    razerBoard.set_key(maps.pynput_to_keymap[k], c)
    razerBoard.write_keys()


def on_release(key):
    try:
        # print('alphanumeric key {0} pressed'.format(key.char))
        k = key.char
        
    except AttributeError:
        # print('special key {0} pressed'.format(key))
        k = key.name

    razerBoard.set_key(maps.pynput_to_keymap[k], Color(0, 0, 0))
    razerBoard.write_keys()
    # print('{0} released'.format(key))
    # if key == keyboard.Key.esc:
    #     # Stop listener
    #     return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    print(ck)
    listener.join()