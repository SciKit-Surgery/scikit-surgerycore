"""
Construct 3x3 rotation matrices for rotating around the x, y and z axes
individually, as well as 3x3 rotation matrices from sequences of three
Euler angles.
"""

import numpy as np


def construct_rx_matrix(angle, is_in_radians=True):
    """
    Construct a rotation matrix for rotation around the x axis.

    :param angle: the angle to rotate
    :param is_in_radians: if angle is in radians or not, default being True
    :returns: rot_x -- the 3x3 rotation matrix constructed
    """
    if not is_in_radians:
        angle = np.pi * angle / 180

    cos_x = np.cos(angle)
    sin_x = np.sin(angle)

    rot_x = np.array([[1, 0, 0], [0, cos_x, -sin_x], [0, sin_x, cos_x]])

    return rot_x


def construct_ry_matrix(angle, is_in_radians=True):
    """
    Construct a rotation matrix for rotation around the y axis.

    :param angle: the angle to rotate
    :param is_in_radians: if angle is in radians or not, default being True
    :returns: rot_y -- the 3x3 rotation matrix constructed
    """
    if not is_in_radians:
        angle = np.pi * angle / 180

    cos_y = np.cos(angle)
    sin_y = np.sin(angle)

    rot_y = np.array([[cos_y, 0, sin_y], [0, 1, 0], [-sin_y, 0, cos_y]])

    return rot_y


def construct_rz_matrix(angle, is_in_radians=True):
    """
    Construct a rotation matrix for rotation around the z axis.

    :param angle: the angle to rotate
    :param is_in_radians: if angle is in radians or not, default being True
    :returns: rot_z -- the 3x3 rotation matrix constructed
    """
    if not is_in_radians:
        angle = np.pi * angle / 180

    cos_z = np.cos(angle)
    sin_z = np.sin(angle)

    rot_z = np.array([[cos_z, -sin_z, 0], [sin_z, cos_z, 0], [0, 0, 1]])

    return rot_z


def construct_rotm_from_euler(
        angle_a, angle_b, angle_c,
        sequence, is_in_radians=True):
    """
    Construct a rotation matrix from a sequence of three Euler angles, to
    pre-multiply column vectors. In the case of tracking, the column vector is
    under the local coordinate system and the resulting vector is under the
    world (reference) coordinate system.
    The three elemental rotations represented by the Euler angles are about the
    INTRINSIC axes. They can also be interpreted to be about the EXTRINSIC axes,
    in the reverse order.

    :param angle_a: first Euler angle
    :param angle_b: second Euler angle
    :param angle_c: third Euler angle
    :param sequence: the sequence of axes the three elemental rotations are
    about, with respect to the intrinsic axes
    :param is_in_radians: if angle is in radians or not, default being True
    :returns: rot_m -- the 3x3 rotation matrix
    """
    while True:
        if sequence == 'zxz':
            rot_a = construct_rz_matrix(angle_a, is_in_radians)
            rot_b = construct_rx_matrix(angle_b, is_in_radians)
            rot_c = construct_rz_matrix(angle_c, is_in_radians)
            break

        if sequence == 'xyx':
            rot_a = construct_rx_matrix(angle_a, is_in_radians)
            rot_b = construct_ry_matrix(angle_b, is_in_radians)
            rot_c = construct_rx_matrix(angle_c, is_in_radians)
            break

        if sequence == 'yzy':
            rot_a = construct_ry_matrix(angle_a, is_in_radians)
            rot_b = construct_rz_matrix(angle_b, is_in_radians)
            rot_c = construct_ry_matrix(angle_c, is_in_radians)
            break

        if sequence == 'zyz':
            rot_a = construct_rz_matrix(angle_a, is_in_radians)
            rot_b = construct_ry_matrix(angle_b, is_in_radians)
            rot_c = construct_rz_matrix(angle_c, is_in_radians)
            break

        if sequence == 'xzx':
            rot_a = construct_rx_matrix(angle_a, is_in_radians)
            rot_b = construct_rz_matrix(angle_b, is_in_radians)
            rot_c = construct_rx_matrix(angle_c, is_in_radians)
            break

        if sequence == 'yxy':
            rot_a = construct_ry_matrix(angle_a, is_in_radians)
            rot_b = construct_rx_matrix(angle_b, is_in_radians)
            rot_c = construct_ry_matrix(angle_c, is_in_radians)
            break

        if sequence == 'xyz':
            rot_a = construct_rx_matrix(angle_a, is_in_radians)
            rot_b = construct_ry_matrix(angle_b, is_in_radians)
            rot_c = construct_rz_matrix(angle_c, is_in_radians)
            break

        if sequence == 'zyx':
            rot_a = construct_rz_matrix(angle_a, is_in_radians)
            rot_b = construct_ry_matrix(angle_b, is_in_radians)
            rot_c = construct_rx_matrix(angle_c, is_in_radians)
            break

        raise ValueError(sequence + " is not a valid sequence.")

    rot_tmp = np.matmul(rot_a, rot_b)
    rot_m = np.matmul(rot_tmp, rot_c)

    return rot_m
