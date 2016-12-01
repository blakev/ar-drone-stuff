#! /usr/bin/env python
# -*- coding: utf-8 -*-
# >>
#     Copyright (c) 2016, Blake VandeMerwe
#
#       Permission is hereby granted, free of charge, to any person obtaining
#       a copy of this software and associated documentation files
#       (the "Software"), to deal in the Software without restriction,
#       including without limitation the rights to use, copy, modify, merge,
#       publish, distribute, sublicense, and/or sell copies of the Software,
#       and to permit persons to whom the Software is furnished to do so, subject
#       to the following conditions: The above copyright notice and this permission
#       notice shall be included in all copies or substantial portions
#       of the Software.
#
#     ar-drone-stuff, 2016
# <<

import os

import numpy as np
from matplotlib import pyplot as plt

from utils import cv2

path = os.path.join(os.getcwd(), 'resources', 'images')

# for f in os.listdir(training_data_path):
#     if not f.startswith('carpet'):
#         continue
#
#     f = os.path.join(training_data_path, f)

imga = cv2.imread(path + '/carpet_001.jpg', cv2.CV_LOAD_IMAGE_GRAYSCALE)
imgb = cv2.imread(path + '/carpet_002.jpg', cv2.CV_LOAD_IMAGE_GRAYSCALE)

orb = cv2.ORB()

kp1, des1 = orb.detectAndCompute(imga, None)
kp2, des2 = orb.detectAndCompute(imgb, None)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(des1, des2)
matches = sorted(matches, key=lambda x: x.distance)
img3 = cv2.drawMatches(imga, kp1, imgb, kp2, matches[:10], flags=2)
plt.imshow(img3)
plt.show()

print


