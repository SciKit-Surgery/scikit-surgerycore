import numpy as np

# pylint: disable=invalid_name


def construct_rx_matrix(angle, is_in_radians=True):
    """
    Construct a rotation matrix for rotation around the x axis.

    :param angle: the angle to rotate
    :param is_in_radians: if angle is in radians or not, default being True
    :returns: rot_x -- the 3x3 rotation matrix
    """
    if not is_in_radians:
        angle = np.pi * angle / 180

    cx = np.cos(angle)
    sx = np.sin(angle)

    rot_x = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])

    return rot_x


def construct_ry_matrix(angle, is_in_radians=True):
    """
    Construct a rotation matrix for rotation around the y axis.

    :param angle: the angle to rotate
    :param is_in_radians: if angle is in radians or not, default being True
    :returns: rot_y -- the 3x3 rotation matrix
    """
    if not is_in_radians:
        angle = np.pi * angle / 180

    cy = np.cos(angle)
    sy = np.sin(angle)

    rot_y = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])

    return rot_y


def construct_rz_matrix(angle, is_in_radians=True):
    """
    Construct a rotation matrix for rotation around the z axis.

    :param angle: the angle to rotate
    :param is_in_radians: if angle is in radians or not, default being True
    :returns: rot_z -- the 3x3 rotation matrix
    """
    if not is_in_radians:
        angle = np.pi * angle / 180

    cz = np.cos(angle)
    sz = np.sin(angle)

    rot_z = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])

    return rot_z
