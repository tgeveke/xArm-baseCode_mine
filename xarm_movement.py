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
import keyboard
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

arm = upgradedArm('192.168.1.207', baud_checkset=False)
arm.clean_warn()
arm.clean_error()
arm.motion_enable(True)
arm.set_mode(0)
arm.set_state(0)

#To start the command of Xarm
# what does that = mean, or I just need to enter arm.set?
# how does this command related with the transformer.py?

code = arm.set_position(x=300, y=0, z=200, roll=-3.14, pitch=0, yaw=0, is_radian=True)
# code will a 0 or 1 to return the status