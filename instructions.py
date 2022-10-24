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
            arm.set_position(x=x_i, y=y_i, z=z_i-distance, roll=roll_i, pitch=pitch_i, yaw=yaw_i, speed=50, wait=True)
    else:
        print('Error with distance:', distance)
        sys.exit()


def captureImage():
    # Read video
    if camera is None:
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
    arm.reset()


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
    'get front distance': getFrontDistance

}

# filename = sys.argv[2]
filename = 'instructions.txt'
file = open(filename)
for instruction in file.readlines():
    if '#' not in instruction:  # Skips 'commented out' lines of instruction
        print(instruction)
        options[instruction.strip()]()

arm.disconnect()
