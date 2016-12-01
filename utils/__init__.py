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
import sys
import imp
import logging

logger = logging.getLogger(__name__)

this_folder = os.path.dirname(os.path.abspath(__file__))
submodules_folder = os.path.abspath(os.path.join(this_folder, os.pardir, 'bin'))

submodules = [
    'ardrone'
]

# we need to add this for distribution-packages, like opencv2
sys.path.insert(1, '/usr/lib/python2.7/dist-packages')

# add our submodules to our path
for m in submodules:
    sys.path.insert(1, os.path.join(submodules_folder, m))


try:
    import libardrone
    import arnetwork
    import arvideo
except ImportError:
    print 'are you missing the submodules git repositories?'
    raise


try:
    import cv2
except ImportError:
    print 'have you installed opencv from your distribution?'
    raise


from utils import (
    drone, imaging, wifi
)

__all__ = [
    'drone',
    'imaging',
    'wifi',
    # ~~~~
    'cv2',
    'arnetwork',
    'arvideo',
    'libardrone'
]
