# -*- coding: utf-8 -*-
from PIL import Image, ImageEnhance

from config import CAPTCHA_DIR, COMPONENT_DIR, CAPTCHA_COUNT


max_width = 0
component_name = ""

for num in xrange(CAPTCHA_COUNT):
    im = Image.open("%s/%d.gif" % (CAPTCHA_DIR, num))
    print im.format, im.size, im.mode

    crop_im = im.crop((0, 0, 50, 25))

    # convert mode 'P' to 'RGB'
    im_rgb = im.convert("RGB")
    enh = ImageEnhance.Color(im_rgb)
    im_rgb = enh.enhance(10)

    # convert mode 'RGB' to 'L'
    im_l = im_rgb.convert("L")
    im_l = im_l.point(lambda i: 0 if i < 200 else 255)

    pixels = im_l.load()
    start_col = None
    parts = []

    # devide the whole image into small parts
    for col in range(im_l.size[0]):         # for every column
        column = []
        for row in range(im_l.size[1]):     # for every row
            column.append(pixels[col, row])
        if 0 in column and start_col is None:
            start_col = col
        if 0 not in column and start_col:
            end_col = col
            parts.append((start_col, end_col))
            start_col = None

    # save into component directory
    for i, p in enumerate(parts):
        letter = im_l.crop((p[0], 0, p[1], 25))
        if len(parts) == 4:
            letter.save("%s/%d-%d.gif" % (COMPONENT_DIR, num, i))
            # record the maximum width letter 
            width = p[1] - p[0]
            if max_width < width:
                max_width = width
                component_name = "%d-%d.gif" % (num, i)
        else:
            letter.save("%s/m-%d-%d.gif" % (COMPONENT_DIR, num, i))

    # TODO: need to close image file manually

print max_width, component_name
