# -*- coding: utf-8 -*-


import subprocess
from Config import Env


def motionDetection():
    if (subprocess.call(["stbt", "run", "NewTvTesting/StbtTestLive.py"])) == 1:
        return True
    else:
        return False


def screenshot(file):
    return runStbtProcess(["stbt", "screenshot", file])

def runStbtProcess(params):
    if (subprocess.call(params)) == 0:
        return True
    else:
        #restart grabber
        subprocess.call([Env.STB_GRABBER_RESET])
        #single retry
        if (subprocess.call(params)) == 0:
            return True
        else:
            return False