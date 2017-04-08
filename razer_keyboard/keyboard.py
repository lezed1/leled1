from .color import Color
from .maps import *

import numpy as np
from scipy import misc
from scipy import ndimage

driver_base = "/sys/bus/hid/drivers/razerkbd/0003:1532:0220.0003"
colour_file = '{}/matrix_custom_frame'
custom_mode_file = '{}/matrix_effect_custom'


def create_color_store():
    return [[Color() for _ in range(16)] for _ in range(6)]


class Keyboard:
    """docstring for Keyboard"""
    def __init__(self, driver_base=driver_base):
        self.colour_file = '{}/matrix_custom_frame'.format(driver_base)
        self.custom_mode_file = '{}/matrix_effect_custom'.format(driver_base)

        self.colors = create_color_store()

    def write_keys(self):
        with open(self.custom_mode_file, 'wb') as custom_mode_file:
            with open(self.colour_file, 'wb') as row_file:
                for r in range(6):
                    row_bytes = bytes((r, 0x00, 0x0F))
                    row_bytes += b''.join(map(Color.get_bytes, self.colors[r]))
                    row_file.write(row_bytes)
                    custom_mode_file.write(bytes('1', 'ascii'))


    def set_key_rc(self, r: int, c: int, color=Color(0, 0, 0), store=None):
        if store == None:
            store = self.colors
        store[r][c] = color


    def set_key(self, key: str, color=Color(0, 0, 0), store=None):
        if store == None:
            store = self.colors
        r, c = keymap[key]
        self.set_key_rc(r, c, color, store)


    def get_key_rc(self, r: int, c: int, store=None) -> Color:
        if store == None:
            store = self.colors
        return store[r][c]


    def get_key(self, key: str, store=None) -> Color:
        if store == None:
            store = self.colors
        r, c = keymap[key]
        return self.get_key_rc(r, c, store)


    def set_image(self, image, store=None):
        if store == None:
            store = self.colors
        image = misc.imresize(image, (274, 736))

        for key, ((uly, ulx), (bry, brx)) in location_map.items():
            avg = np.mean(image[ulx:brx, uly:bry], axis=(0, 1), dtype=np.int)[:3]
            self.set_key(key, Color(*avg), store)

        return store


    def get_store(self):
        return self.colors


    def set_store(self, store):
        self.colors = store

