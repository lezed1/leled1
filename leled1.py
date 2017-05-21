#!/usr/bin/env python3

from collections import namedtuple
import colorsys
import itertools
from multiprocessing.pool import ThreadPool
import time


import gizeh
import numpy as np
from scipy import misc
from scipy import ndimage

from razer_keyboard.color import Color
from razer_keyboard.keyboard import Keyboard, create_color_store
from razer_keyboard.maps import *

try:
    import pynput
except:
    pass

keyboard = Keyboard()

def set_image(image):
    image = image.transpose()
    image = misc.imresize(image, (736, 274))
    for key, ((ulx, uly), (brx, bry)) in location_map.items():
        avg = np.mean(image[ulx:brx, uly:bry], axis=(0, 1), dtype=np.int)[:3]
        set_key(key, Color(*avg))


def get_image():
    surface = gizeh.Surface(width=736, height=274)

    for key, ((ulx, uly), (brx, bry)) in location_map.items():
        gizeh.rectangle(lx=(brx - ulx), ly=(bry - uly), xy=((ulx + brx) / 2, (uly + bry) / 2), fill=keyboard.get_key(key).get_floats()).draw(surface)

    surface.write_to_png("out.png")

# image = ndimage.imread("/home/zander/Downloads/rainbowbars.jpg")
# # image = ndimage.imread("/home/zander/Downloads/prop.png")

# image = misc.imresize(image, (1000, 1000))
# keyboard.set_image(image)
# keyboard.write_keys()

# pool = ThreadPool()
# images = pool.map(lambda i: keyboard.set_image(ndimage.interpolation.rotate(image, i, reshape=False), create_color_store()), range(0, 361, 5))

# for img in itertools.cycle(images):
#     keyboard.set_store(img)
#     keyboard.write_keys()
#     get_image()

#     time.sleep(1 / 60)


# keyboard.set_key('j', Color(255, 0, 255))
# keyboard.set_key('c', Color(255, 255, 0))
# keyboard.set_key('b', Color(255, 128, 0))
# keyboard.write_keys()


for i, k in enumerate(keymap):
    keyboard.set_key(k, Color(i * 2, i, 255 - i * 2))
keyboard.write_keys()

# while True:
#     for i in range(0, 256, 5):
#         for r in range(6):
#             for c in range(16):
#                 rgb = colorsys.hsv_to_rgb(c / 15 + i/255, 1 - r / 20, 1)
#                 keyboard.set_key_rc(r, c, Color(*map(lambda x: int(x * 255), rgb)))

#         keyboard.write_keys()
#         print("Written {}".format(i))
#         time.sleep(1 / 60)


width = 500
center = {"x": 736 / 2, "y": 274 / 2}

def on_press(key):
    # print(key)
    try:
        # print('alphanumeric key {0} pressed'.format(key.char))
        k = key.char
        
    except AttributeError:
        # print('special key {0} pressed'.format(key))
        k = key.name

    (l, t), (r, b) = location_map[pynput_to_keymap[k]]

    center["x"], center["y"] = (l + r) / 2, (t + b) / 2

try:
    listener = pynput.keyboard.Listener(on_press=on_press)
    print(listener)
    # print(help(listener))
except:
    pass

while True:
    for i in range(0, width, 5):
        ii = (width - i)
        for key, ((l, t), (r, b)) in location_map.items():
            x = (l + r) / 2
            y = (t + b) / 2

            rad = ((center["x"] - x) ** 2 + (center["y"] - y) ** 2) ** 0.5

            rgb = colorsys.hsv_to_rgb((rad * 1.5 + ii) / width, 1, 1)
            r, c = keymap[key]
            keyboard.set_key_rc(r, c, Color(*map(lambda x: int(x * 255), rgb)))

        # asdf()

        keyboard.write_keys()
        # get_image()
        print("Written {}".format(i))
        time.sleep(1 / 60)
