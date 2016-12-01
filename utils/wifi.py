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

import logging
import subprocess

logger = logging.getLogger(__name__)


class Wifi(object):

    def __init__(self, device, access_point="blake_drone"):
        self.device = device
        self.access_point = access_point
        self.connected = False

    @property
    def signal_strength(self):
        command_parts = ["iw", "dev", self.device, "link", "|", "grep", "signal", "|", "xargs", "|", "awk", "'{print $2}'"]
        command = " ".join(command_parts)

        #proc = subprocess.Popen(command_parts, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #out, err = proc.communicate()

        #retcode = proc.returncode

        return int(subprocess.check_output(command, shell=True).strip())

    def connect(self, access_point=None):
        access_point = access_point if access_point else self.access_point

        if access_point is None:
            raise("Must specify access point")

        self.access_point = access_point

        netctl = True if subprocess.call(["which", "netctl"]) == 0 else False
        nm = True if subprocess.call(["which", "nmcli"]) == 0 else False

        if netctl:
            ret = self._netctl_connect(access_point)
        elif nm:
            ret = self._nm_connect(access_point)
        else:
            raise("Could not find method to connect to access point")

        return ret

    def _netctl_connect(self, access_point):
        result =  subprocess.call("netctl start {}".format(access_point), shell=True)
        self.connected = True if result == 0 else False
        return self.connected

    def _nm_connect(self, access_point):
        result =  subprocess.call("nmcli c up {}".format(access_point), shell=True)
        self.connected = True if result == 0 else False
        return self.connected

    def disconnect(self):
        raise("Not implemented")
