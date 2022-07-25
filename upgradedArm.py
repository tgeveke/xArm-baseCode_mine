try:
    from xarm.tools import utils
except:
    pass
from xarm import version
from xarm.wrapper import XArmAPI
from transformer import fillParams


class upgradedArm(XArmAPI):

    def __init__(self, port=None, is_radian=False, do_not_open=False, **kwargs):
        super().__init__(port, is_radian, do_not_open, **kwargs)

    def set_pose(self, pose, speed=100, mvacc = 1000, wait=False, mvtime=None, radius=None, relative=None,\
                 is_radian=False, timeout=None):
        """
        :param pose: (dict[str|num]): Pose to move to
        :param radius: move radius, if radius is None or radius less than 0, will MoveLine, else MoveArcLine
            MoveLine: Linear motion
                ex: code = arm.set_position(..., radius=None)
            MoveArcLine: Linear arc motion with interpolation
                ex: code = arm.set_position(..., radius=0)
                Note: Need to set radius>=0
        :param speed: move speed (mm/s, rad/s), default is self.last_used_tcp_speed
        :param mvacc: move acceleration (mm/s^2, rad/s^2), default is self.last_used_tcp_acc
        :param mvtime: 0, reserved
        :param relative: relative move or not
        :param is_radian: the roll/pitch/yaw in radians or not, default is self.default_is_radian
        :param wait: whether to wait for the arm to complete, default is False
        :param timeout: maximum waiting time(unit: second), default is None(no timeout), only valid if wait is True
        :param kwargs: reserved
        :return: code
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
                code < 0: the last_used_position/last_used_tcp_speed/last_used_tcp_acc will not be modified
                code >= 0: the last_used_position/last_used_tcp_speed/last_used_tcp_acc will be modified
        """
        filledPose = fillParams(pose)
        return self.set_position(filledPose["x"], filledPose["y"], filledPose["z"], filledPose["rX"], filledPose["rY"],
                                 filledPose["rZ"], speed=speed, mvacc=mvacc, wait=wait, mvtime=mvtime, radius=radius,
                                 relative=relative, is_radian=is_radian, timeout=timeout)
