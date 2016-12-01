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
import math
import logging
import datetime
import threading
import Queue

from easydict import EasyDict

from utils import libardrone
from utils.wifi import Wifi

logger = logging.getLogger(__name__)


class Drone(libardrone.ARDrone):
    def __init__(self, wifi, clear_emergency=True, save_navdata=True, save_navdata_interval=0.5):
        super(Drone, self).__init__()

        self._wifi = wifi

        self.created = datetime.datetime.now()
        self._t_takeoff = None
        self._t_landing = None

        self._threads = []
        self._threads_running = False

        self._vectors = []
        self._nav_data = Queue.Queue()

        if save_navdata:
            def poll_navdata(interval):
                while self._threads_running:
                    self._nav_data.put(self.navdata)
                    time.sleep(interval)

            t = threading.Thread(target=poll_navdata, args=(0.15,))
            t.setDaemon(True)
            t.start()
            self._threads.append(t)

        while not self.navdata:
            time.sleep(0.25)

        if self.drone_state.emergency_mask and clear_emergency:
            self.reset()

        if self._threads:
            self._threads_running = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val:
            self.emergency()
        self.stop_flight()

    @property
    def battery(self):
        return self.navdata.get('0', {}).get('battery', -1)

    @property
    def battery_low(self):
        return self.drone_state.vbat_low

    @property
    def connection_strength(self):
        x = self.wifi.signal_strength
        return round(1.0 / (1.0 + math.pow(abs(x) / 60.51246, 7.41392)), 4)

    @property
    def drone_state(self):
        d = {k: bool(v) for k, v in self.navdata.get('drone_state', {}).items()}
        return EasyDict(d)

    @property
    def has_vision(self):
        return bool(self.navdata.get('vision_flag', 0))

    @property
    def is_emergency(self):
        return self.drone_state.emergency_mask

    @property
    def is_flying(self):
        return self.drone_state.fly_mask

    @property
    def wifi(self):
        return self._wifi

    def emergency(self):
        self.land()
        self.halt()

    def set_speed(self, speed):
        super(Drone, self).set_speed(max(0, min(speed, 1)))

    def stop_flight(self):
        self._threads_running = False
        for t in self._threads:
            t.join()
        while not self._nav_data.empty():
            print self._nav_data.get()
        self.land()
        self.halt()
