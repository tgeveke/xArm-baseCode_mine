import sys
from time import sleep
from xarm.wrapper import XArmAPI
from cameraClass import Camera

ip = '192.168.1.207'
arm = XArmAPI(ip)
global_speed = 125
plane = 'top'


def grab():
    arm.set_gripper_enable(True)
    arm.set_gripper_position(800, wait=False)
    arm.set_servo_angle(servo_id=6, angle=190, speed=50, is_radian=False, wait=True)
    arm.set_position(z=-50, relative=True)
    sleep(1)
    arm.set_gripper_position(175, wait=True)


def smartGrab():
    print('WIP')


def smartGrab_failed():
    # I don't think this will work :-(
    arm.set_gripper_enable(True)
    val = 800  # Initializes start value
    arm.set_gripper_position(val, speed=100, wait=False)

    import timeit
    lastTime = 100
    factor = 1.2
    stepSize = 3  # Decreases each step
    threshold = 600

    while val > threshold:
        startTime = timeit.default_timer()
        val = val - stepSize
        arm.set_gripper_position(val, speed=10000, wait=True)
        time = timeit.default_timer() - startTime
        print(time)
        if time > (lastTime * factor):
            print('overtime')
            # sys.exit()
        lastTime = time


def move2target():
    distance = 125  # getDistance()
    if 0 < distance < 200:  # Reasonable values
        print('Distance to target:', distance)
        if plane == 'front':
            arm.set_position(x=distance, speed=50, relative=True, wait=True)
        elif plane == 'top':
            [x_i, y_i, z_i, roll_i, pitch_i, yaw_i] = locations['topPrinter']
            arm.set_position(x=x_i, y=y_i, z=z_i - distance, roll=roll_i, pitch=pitch_i, yaw=yaw_i, speed=50, wait=True)
    else:
        print('Error with distance:', distance)
        sys.exit()


def captureImage():
    # Read video
    camera = Camera()  # Runs init() function
    return camera.getDistance()  # rgb_array, depth_array


def getDistanceLine():
    # centerX = depth_array.shape[0] // 2
    depth_array = captureImage()[1]
    centerY = depth_array.shape[1] // 2
    return depth_array[:, centerY]


def getFrontDistance():
    distance_line = getDistanceLine()
    print(distance_line)
    minDistance = min(distance_line)


locations = {
    # [x, y, z, roll, pitch, yaw]
    'frontPrinter': [50, 400, 50, -90, 90, 90],
    'topPrinter': [-100, 400, 250, -180, 0, 0]
}


def view_frontPrinter():
    setPlane('front')

    location_values = locations['frontPrinter']
    [x_i, y_i, z_i, roll_i, pitch_i, yaw_i] = location_values
    arm.set_position(x=x_i, y=y_i, z=z_i, roll=roll_i, pitch=90, yaw=yaw_i, speed=global_speed, wait=True)


def view_topPrinter():
    setPlane('top')

    location_values = locations['topPrinter']
    [x_i, y_i, z_i, roll_i, pitch_i, yaw_i] = location_values
    arm.set_position(x=x_i, y=y_i, z=z_i, roll=roll_i, pitch=pitch_i, yaw=yaw_i, speed=global_speed, wait=True)


def viewObjectTop():
    setPlane('top')


def setPlane(current_plane):
    global plane
    plane = current_plane


def wait():
    sleep(10)


def home():
    arm.move_gohome(speed=50)


def reset():
    arm.clean_warn()
    arm.clean_gripper_error()
    arm.clean_error()
    sleep(1)
    arm.reset()


def scan():
    from ScanFolder import sphericalScan
    from math import degrees

    arm.set_position(z=200, relative=True, speed=25, wait=True)
    arm.set_servo_angle(servo_id=1, angle=-90, speed=25, wait=True)
    arm.set_position(y=-200, relative=True, speed=25, wait=True)


    points = sphericalScan.createPoints(plot=True, k=-0.8, j=0.2, radius=0.3, degreesToScan=60, numCurves=4, pointsPerCurve=10, scale=500)
    print(len(points))

    for point in points:
        [x_i, y_i, z_i, roll_i, pitch_i, yaw_i] = point
        x_i = int(x_i)
        y_i = int(y_i)
        z_i = int(z_i)
        roll_i = int(degrees(roll_i))
        pitch_i = int(degrees(pitch_i))
        yaw_i = int(degrees(yaw_i))
        print(x_i, y_i, z_i, roll_i, pitch_i, yaw_i)
        if x_i not in range(-700, 700):
            print('X too high')
            continue
        if y_i not in range(-700, 700):
            print('Y too high')
            continue
        if z_i not in range(-400, 950):
            print('Z too high')
            continue
        if roll_i not in range(-180, 180):
            print('X Angle too high')
            continue
        if roll_i not in range(-180, 180):
            print('Y Angle too high')
            continue
        if roll_i not in range(-180, 180):
            print('Z Angle too high')
            continue
        else:
            print('good')
            arm.set_position(x=x_i, y=y_i, z=z_i, wait=True, relative=False) #, roll=roll_i, pitch=pitch_i, yaw=yaw_i, is_radian=False, speed=25, mvacc=250, wait=True)
        sleep(1)


def otherScan():
    start = locations['topPrinter']
    start[1] = start[1] + 100
    # end = start
    # end[1] = start[1] - 100
    end = locations['frontPrinter']
    arm.move_circle(start, end, percent=90, is_radian=False)


options = {
    'wait': wait,
    'reset': reset,
    'go home': home,
    'view front printer': view_frontPrinter,
    'view top printer': view_topPrinter,
    'capture image': captureImage,
    'move to target position': move2target,
    'grab': grab,
    'smart grab': smartGrab,
    'view object top': viewObjectTop,
    'get front distance': getFrontDistance,
    'scan': scan
}

# filename = sys.argv[2]
filename = 'instructions.txt'
file = open(filename)
for instruction in file.readlines():
    if '#' not in instruction:  # Skips 'commented out' lines of instruction
        print(instruction)
        options[instruction.strip()]()

arm.disconnect()
