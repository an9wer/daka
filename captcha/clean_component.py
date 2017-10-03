# -*- coding: utf-8 -*-

import os
import sys
from PIL import Image

from config import COMPONENT_DIR, LETTER_DIR


cleaned_letters = set([])

# remove duplicate components
for im_name in os.listdir(COMPONENT_DIR):
    if not im_name.startswith('m'):
        im = Image.open("%s/%s" % (COMPONENT_DIR, im_name))
        # convert mode 'P' to 'L'
        im = im.convert("L")
        letter_info = (im.mode, im.size, im.tobytes())
        cleaned_letters.add(letter_info)

print 'size:', sys.getsizeof(cleaned_letters)
print 'len:', len(cleaned_letters)

# save letters into `letter` directory
for i, letter in enumerate(cleaned_letters):
    im = Image.frombytes(letter[0], letter[1], letter[2])
    im.save("%s/%d.gif" % (LETTER_DIR, i))
