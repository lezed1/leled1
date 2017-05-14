class Color:
    """docstring for Color"""
    def __init__(self, red=0, green=0, blue=0):
        self.red = red
        self.green = green
        self.blue = blue
        

    def get_floats(self, alpha=False):
        if alpha:
            return (self.red / 255, self.green / 255, self.blue / 255, 255)
        else:
            return (self.red / 255, self.green / 255, self.blue / 255)
        

    def get_ints(self):
        return (self.red, self.green, self.blue)

    def get_bytes(self):
        return bytes(self.get_ints())
