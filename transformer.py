
# These should both be installed by default, otherwise something is very wrong with your python install
import math
import numpy as np

# Euler Format: Python dict structure with fields:
"""
x
y
z
rX
rY
rZ
"""
# Rotation coordinates are in degrees, position coordinates are in whatever unit you prefer,
# just keep it consistent

# Matrix format (numpy 4x4 matrix)
"""
|xx| |xy| |xz| |xPos|
|yx| |yy| |yz| |yPos|
|zx| |zy| |zz| |zPos|
 0    0    0    1
"""


def appendCoords(originCoords, localCoords):
    """
    Append (add) coordinates (in Euler format).
    Either of the 2 can have entries ("x", "rY", etc.) omitted as all values default to zero
    :param originCoords: (dict[str | num]): Euler-formatted coordinates to append to
    :param localCoords: (dict[str | num]): Euler-formatted coordinates to append
    :return: (dict[str|num]): Euler-formatted appended coordinates
    """

    originMatrix = pose2Transform(originCoords)
    localMatrix = pose2Transform(localCoords)
    worldMatrix = np.matmul(originMatrix, localMatrix)
    worldCoords = transform2Pose(worldMatrix)

    return worldCoords


def rotateVector(vect, axis, angle):
    """
    Rotates a vector around an axis by a specified angle in degrees
    :param vect: (Array[num]]): The vector to rotate
    :param axis: (str, either "x", "y", or "z"): The axis to rotate around
    :param angle: (num): The angle in degrees to rotate
    :return: (array[num]): The rotated vector
    """
    newVect = [0, 0, 0]
    if axis == "x":
        newVect[1] = vect[1] * math.cos(math.radians(angle)) - vect[2] * math.sin(math.radians(angle))
        newVect[2] = vect[1] * math.sin(math.radians(angle)) + vect[2] * math.cos(math.radians(angle))
        newVect[0] = vect[0]
    elif axis == "y":
        newVect[2] = vect[2] * math.cos(math.radians(angle)) - vect[0] * math.sin(math.radians(angle))
        newVect[0] = vect[2] * math.sin(math.radians(angle)) + vect[0] * math.cos(math.radians(angle))
        newVect[1] = vect[1]
    else:
        newVect[0] = vect[0] * math.cos(math.radians(angle)) - vect[1] * math.sin(math.radians(angle))
        newVect[1] = vect[0] * math.sin(math.radians(angle)) + vect[1] * math.cos(math.radians(angle))
        newVect[2] = vect[2]
    return newVect


def transform2Pose(transform):
    """
    Changes a transformation matrix to Euler coordinates
    :param transform: (numpy array[num]): The matrix to transform
    :return: (dict[str|num]): The Euler pose
    """
    x = transform[0, 3]
    y = transform[1, 3]
    z = transform[2, 3]

    [r11, r12, r13] = transform[0, 0], transform[1, 0], transform[2, 0]
    [r21, r22, r23] = transform[0, 1], transform[1, 1], transform[2, 1]
    [r31, r32, r33] = transform[0, 2], transform[1, 2], transform[2, 2]

    rY = math.degrees(math.atan2(r13, math.sqrt(1 - (r13 * r13))))

    if r13 != 1 or -1:
        rX = math.degrees(math.atan2(r23, r33))
        rZ = - math.degrees(math.atan2(r12, r11))
    else:
        rX = math.degrees(math.atan2(r21, r31))
        rZ = 0
    return {"x": x, "y": y, "z": z, "rX": rX, "rY": rY, "rZ": rZ}


def pose2Transform(pose=None, x=0, y=0, z=0, rX=0, rY=0, rZ=0, overWritePose=None):
    """
     Forms a coordinate frame from a pose, fed either the parameters x, y, z, rX, rY, and rZ, or a dict (pose) containing them.
     If both are provided defaults to using pose parameters, then falls back on the direct inputs for any missing params.
     Parameter names called out in optional overWritePose will force the function to always use the direct input version.
    :param pose: (dict[str|num]): Optional. An Euler pose
    :param x: (num): Optional. Raw X coordinate
    :param y: (num): Optional. Raw Y coordinate
    :param z: (num): Optional. Raw Z coordinate
    :param rX: (num): Optional. Euler rX coordinate
    :param rY: (num): Optional. Euler rY coordinate
    :param rZ: (num): Optional. Euler rZ coordinate
    :param overWritePose: (array[str]): Optional. Array of parameter names such as ["x", "rZ"]. Forces generator to use
    raw input versions of listed parameters instead of values from dictionary input. Useful for modified versions of existing poses.
    Technically you could feed this a dictionary where the item names to overwrite are keys, might be helpful.
    :return: (numpy array[num]) 4x4 transformation matrix
    """
    if overWritePose is None:
        overWritePose = []
    if pose is not None:
        if "x" in pose and "x" not in overWritePose:
            x = pose["x"]
        if "y" in pose and "y" not in overWritePose:
            y = pose["y"]
        if "z" in pose and "z" not in overWritePose:
            z = pose["z"]
        if "rX" in pose and "rX" not in overWritePose:
            rX = pose["rX"]
        if "rY" in pose and "rY" not in overWritePose\
            :rY = pose["rY"]
        if "rZ" in pose and "rZ" not in overWritePose:
            rZ = pose["rZ"]
    # Rotation matrix
    [r11, r12, r13] = rotateVector(rotateVector(rotateVector([1, 0, 0], "z", rZ), "y", rY), "x", rX)
    [r21, r22, r23] = rotateVector(rotateVector(rotateVector([0, 1, 0], "z", rZ), "y", rY), "x", rX)
    [r31, r32, r33] = rotateVector(rotateVector(rotateVector([0, 0, 1], "z", rZ), "y", rY), "x", rX)
    t1 = x
    t2 = y
    t3 = z
    # Transformation matrix
    T = np.array([[r11, r21, r31, t1],
                  [r12, r22, r32, t2],
                  [r13, r23, r33, t3],
                  [0, 0, 0, 1]])
    return T


def addPoses(pose1, pose2, addRotation=True):
    """
    Adds 2 poses in the same frame.
    :param pose1: (dict[str|num]): The first pose to add.
    :param pose2: (dict[str|num]): The second pose to add.
    :param addRotation: (bool): Optional, default = True. If false will only use the rotation coordinates from pose1.
    :return: (dict[str|num): Result of adding poses 1 and 2.
    """
    # Fill missing params
    pose1Filled = fillParams(pose1)
    pose2Filled = fillParams(pose2)

    total = {"x": (pose1Filled["x"] + pose2Filled["x"]), "y": (pose1Filled["y"] + pose2Filled["y"]), "z": (pose1Filled["z"] + pose2Filled["z"])}
    if addRotation:
        total["rX"] = pose1Filled["rX"] + pose2Filled["rX"]
        total["rY"] = pose1Filled["rY"] + pose2Filled["rY"]
        total["rZ"] = pose1Filled["rZ"] + pose2Filled["rZ"]
    else:
        total["rX"] = pose1Filled["rX"]
        total["rY"] = pose1Filled["rY"]
        total["rZ"] = pose1Filled["rZ"]
    return total


def offsetInFrame(origin, offset, refFrame, ignoreRot = False):
    """
    Takes an origin pose, offsets it by another pose translated into a reference frame.
    :param origin: (dict[str|num): Original pose coordinates.
    :param refFrame: (dict[str|num): Reference frame to offset in. Positional coords can be omitted (no effect).
    :param offset: (dict[str|num): Coordinates to offset by.
    :param ignoreRot: (bool) - Default False: Whether to ignore rotation in the offset coords.
    :return: (dict[str|num): Offset pose.
    """
    offsetFilled = fillParams(offset)
    refFrameFilled = fillParams(refFrame)
    refFrameFilled["x"], refFrameFilled["y"], refFrameFilled["z"] = 0, 0, 0  # Remove position from reference frame
    framedOffset = appendCoords(refFrameFilled, offsetFilled)  # Translate offset to reference frame

    # Rotation is not relative
    framedOffset["rX"], framedOffset["rY"], framedOffset["rZ"] = offsetFilled["rX"], offsetFilled["rY"], offsetFilled["rZ"]
    pose = addPoses(origin, framedOffset, addRotation=not ignoreRot)
    return pose


def fillParams(pose):
    """
    Fills missing pose parameters ("x", "rY, etc.) with zero
    :param pose: (dict[str|num]) Input pose
    :return: (dict[str|num]) Filled pose
    """
    output = pose.copy()
    if "x" not in output:
        output["x"] = 0
    if "y" not in output:
        output["y"] = 0
    if "z" not in output:
        output["z"] = 0
    if "rX" not in output:
        output["rX"] = 0
    if "rY" not in output:
        output["rY"] = 0
    if "rZ" not in output:
        output["rZ"] = 0
    return output


baseFrame = pose2Transform()
basePose = fillParams({})