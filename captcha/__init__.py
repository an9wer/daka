# -*- coding: utf-8 -*-

import os
import sys
from PIL import Image, ImageEnhance

from config import LETTER_DIR, LETTER_CLS_DIR, SOURCE_DIR

class Captcha(object):

    # initialize class attribute `__template`
    __template = {}
    for letter in os.listdir(LETTER_CLS_DIR):
        subdir = "%s/%s" % (LETTER_CLS_DIR, letter)
        for pic_name in os.listdir(subdir):
            im = Image.open("%s/%s" % (LETTER_DIR, pic_name))
            im_l = im.convert("L")

            pixels = im_l.load()
            pic = tuple()
            for col in range(im_l.size[0]):         # for every column
                column = tuple()
                for row in range(im_l.size[1]):     # for every row
                    column += (pixels[col, row],)
                pic += (column,)
            __template[pic] = (im_l.size[0], letter)
    print len(__template)
    for key, value in __template.items():
        if value == "t":
            print len(key)

    def __init__(self):
        self.result = ""

    def __identify_component(self, captcha):
        """
        :param captcha: an image object
        """
        #captcha.show()
        start_col = None
        process_col = 0
        template = self.__template.copy()
        pixels = captcha.load()

        for col in range(captcha.size[0]):         # for every column
            column = tuple()
            for row in range(captcha.size[1]):     # for every row
                column += (pixels[col, row],)

            letters = set([])
            if 0 in column:
                #print 'process_col', process_col
                if start_col is None:
                    start_col = col
                    print 'start_col', start_col
                for pic in template.copy():
                    if pic[process_col] == column:
                        letters.add(template[pic])
                        #print letters
                    else:
                        template.pop(pic, None)
                if len(letters) == 0:
                    print 2222222222
                    letter = None
                    break
                if len(letters) == 1 and len(set(t[0] for t in template)) == 1:
                    letter = ''.join(i[1] for i in letters)
                    #print letter
                    self.result += letter
                    break
                #if len(letters) == 2 and letters.keys[0][1] == letters[1][1]:
                #    pass
                process_col += 1

            # 如果不能识别某个字母
            if 0 not in column and start_col:
                #print 111111111111
                #print 'len template', len(template)
                #print template.values()
                letter = None
                break

        if (start_col and letter) is not None:
            print 33333333
            #print letter
            #print letters[letter]
            #start = start_col + len(letters[letter][0])
            #print 'len template', len(template)
            if len(template.keys()) >= 1:
                start = start_col + template[template.keys()[0]][0]
                end = captcha.size[0]
                #print start, end
                self.__identify_component(captcha.crop((start, 0, end, 25)))

    def identify(self, path):
        #path = "%s/21.gif" % SOURCE_DIR
        #path = "%s/9899.gif" % SOURCE_DIR

        self.result = ""
        #print sys.getsizeof(self.__template)
        im = Image.open(path)

        # convert mode 'P' to 'RGB'
        im_rgb = im.convert("RGB")
        enh = ImageEnhance.Color(im_rgb)
        im_rgb = enh.enhance(10)

        # convert mode 'RGB' to 'L'
        im_l = im_rgb.convert("L")
        im_l = im_l.point(lambda i: 0 if i < 200 else 255)

        self.__identify_component(im_l)

        return self.result


if __name__ == "__main__":
    c = Captcha()
    for i in range(100):
        c.identify("%s/%s.gif" % (SOURCE_DIR, i))
        print 'result', c.result

    #print Captcha().identify(0)
    #print Captcha.__dict__.keys()
    #print Captcha().__dict__.keys()
