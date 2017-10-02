# -*- coding: utf-8 -*-

import stbt
import sys

try:
    stbt.wait_for_motion()
except MotionTimeout:
    print(">STBT motionDetection - timeout detected<")
    sys.exit(0)
else:
    print(">STBT motionDetection - motion detected<")
    sys.exit(1)


