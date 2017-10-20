# -*- coding: utf-8 -*-

import os
import sys
from PIL import Image, ImageEnhance

from config import LETTER_DIR, LETTER_CLS_DIR, SOURCE_DIR

class Captcha(object):

    # initialize class attribute `__template`
    def __init__(self):
        self.__template = {}
        for letter in os.listdir(LETTER_CLS_DIR):
            subdir = "%s/%s" % (LETTER_CLS_DIR, letter)
            for pic_name in os.listdir(subdir):
                im = Image.open("%s/%s" % (LETTER_DIR, pic_name))
                im_l = im.convert("L")

                pixels = im_l.load()
                pic = tuple()
                for col in range(im_l.size[0]):         # for every column
                    for row in range(im_l.size[1]):     # for every row
                        pic += (pixels[col, row],)
                self.__template[pic] = letter

    def identify(self, path):
        #print sys.getsizeof(self.__template)
        im = Image.open(path)

        # convert mode 'P' to 'RGB'
        im_rgb = im.convert("RGB")
        enh = ImageEnhance.Color(im_rgb)
        im_rgb = enh.enhance(10)

        # convert mode 'RGB' to 'L'
        im_l = im_rgb.convert("L")
        im_l = im_l.point(lambda i: 0 if i < 200 else 255)

        pixels = im_l.load()
        component = tuple()
        components = []
        for col in range(im_l.size[0]):         # for every column
            column = tuple()
            for row in range(im_l.size[1]):     # for every row
                column += (pixels[col, row],)
            if 0 in column:
                component += column
            if 0 not in column and component:
                components.append(component)
                component = tuple()

        res = ""
        if len(components) == 4:
            for component in components:
                res += self.__template[component]

        return res or None


if __name__ == "__main__":
    c = Captcha()
    for i in range(100):
        print 'result', c.identify("%s/%s.gif" % (SOURCE_DIR, i))
