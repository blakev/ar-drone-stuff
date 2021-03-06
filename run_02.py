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

import time
import logging

from utils.wifi import Wifi
from utils.drone import Drone

logger = logging.getLogger(__name__)

fi = Wifi('wlx000f60010344', 'blake_drone')

# while True:
#     print fi.signal_strength
#     time.sleep(1)


d = Drone(fi)
d.reset()
d.land()
d.halt()

