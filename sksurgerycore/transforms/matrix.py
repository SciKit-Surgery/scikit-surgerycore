"""
Construct 3x3 rotation matrices for rotating around the x, y, z axes.
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


def construct_rotation_matrix_from_euler_angles(angle_a, angle_b, angle_c, sequence, is_in_radians=True):
    """
    Construct a rotation matrix from a sequence of three Euler angles, to pre-multiply column vectors.
    The three elemental rotations represented by the Euler angles are about the intrinsic axes.
    They can also be interpreted to be about the extrinsic axes, in the reverse sequence.

    :param angle_A, angle_B, angle_C: the three Euler angles
    :param sequence: the sequence of axes the three elemental rotations are about, with respect to the intrinsic axes
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

        raise ValueError(sequence + " is not in repository.")

    rot_m = rot_a * rot_b * rot_c

    return rot_m


construct_rotation_matrix_from_euler_angles(0, 0, -90, 'zxz', 0)

