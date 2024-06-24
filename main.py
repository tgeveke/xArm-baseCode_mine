#!/usr/bin/env python3
# Arm startup code
# Don't touch this!
import sys
import math
import time
import datetime
import random
import traceback
import threading
import requests
import transformer
from upgradedArm import upgradedArm
from motion_tracking import Motion_tracking
import sys, time, traceback, transformer
from upgradedArm import upgradedArm

try:
    from xarm.tools import utils
except:
    pass
from xarm import version
from xarm.wrapper import XArmAPI

def pprint(*args, **kwargs):
    try:
        stack_tuple = traceback.extract_stack(limit=2)[0]
        print('[{}][{}] {}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), stack_tuple[1], ' '.join(map(str, args))))
    except:
        print(*args, **kwargs)
pprint('xArm-Python-SDK Version:{}'.format(version.__version__))

arm = upgradedArm('192.168.1.207', baud_checkset = False)
arm.clean_warn()
arm.clean_error()
arm.motion_enable(True)
arm.set_mode(0)
arm.set_state(0)

# Arm setup complete
try:
    trackingObject = Motion_tracking()
    print('Success creating tracking object')
except:
    print('Error opening tracking object')
    sys.exit()

distance = trackingObject.getDistance()
print(distance)

arm.move_gohome(speed=100, wait=True)
arm.set_gripper_enable(True)
arm.set_gripper_position(850)
printerPos = {"x": 50.2, "y": 352.6, "z": 50, "rZ": 90} # relative to base

targetPosInFrame = {"x": 150, "y": 0, "z": 50, "rX": 180, "rZ": 90}

goToPos = transformer.appendCoords(printerPos, targetPosInFrame)

print(goToPos)
arm.set_position(200, 0, 300, 180, 0, 0, speed=100, wait=True)

arm.set_pose(goToPos, speed=100, wait=True)
