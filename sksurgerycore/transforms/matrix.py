"""
Construct 3x3 rotation matrices for rotating around the x, y and z axes
individually, as well as 3x3 rotation matrices from sequences of three
Euler angles.
"""

import numpy as np


def construct_rx_matrix(angle, is_in_radians=True):
    """
    Construct a rotation matrix for rotation around the x axis.

    :param angle: the angle to rotate, float
    :param is_in_radians: if angle is in radians, default being True, bool
    :returns: rot_x -- the 3x3 rotation matrix constructed, numpy array
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

    :param angle: the angle to rotate, float
    :param is_in_radians: if angle is in radians, default being True, bool
    :returns: rot_y -- the 3x3 rotation matrix constructed, numpy array
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

    :param angle: the angle to rotate, float
    :param is_in_radians: if angle is in radians, default being True, bool
    :returns: rot_z -- the 3x3 rotation matrix constructed, numpy array
    """
    if not is_in_radians:
        angle = np.pi * angle / 180

    cos_z = np.cos(angle)
    sin_z = np.sin(angle)

    rot_z = np.array([[cos_z, -sin_z, 0], [sin_z, cos_z, 0], [0, 0, 1]])

    return rot_z

# pylint: disable=too-many-branches
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

    :param angle_a: first Euler angle, float
    :param angle_b: second Euler angle, float
    :param angle_c: third Euler angle, float
    :param sequence: the sequence of axes the three elemental rotations are
    about, with respect to the intrinsic axes, string
    :param is_in_radians: if the angles are in radians, default being True,
    bool
    :returns: rot_m -- the 3x3 rotation matrix, numpy array
    """
    while True:
        if sequence == 'zxz':
            rot_a = construct_rz_matrix(angle_a, is_in_radians)
            rot_b = construct_rx_matrix(angle_b, is_in_radians)
            rot_c = construct_rz_matrix(angle_c, is_in_radians)
            break

        if sequence == 'zyz':
            rot_a = construct_rz_matrix(angle_a, is_in_radians)
            rot_b = construct_ry_matrix(angle_b, is_in_radians)
            rot_c = construct_rz_matrix(angle_c, is_in_radians)
            break

        if sequence == 'zxy':
            rot_a = construct_rz_matrix(angle_a, is_in_radians)
            rot_b = construct_rx_matrix(angle_b, is_in_radians)
            rot_c = construct_ry_matrix(angle_c, is_in_radians)
            break

        if sequence == 'zyx':
            rot_a = construct_rz_matrix(angle_a, is_in_radians)
            rot_b = construct_ry_matrix(angle_b, is_in_radians)
            rot_c = construct_rx_matrix(angle_c, is_in_radians)
            break

        if sequence == 'xyx':
            rot_a = construct_rx_matrix(angle_a, is_in_radians)
            rot_b = construct_ry_matrix(angle_b, is_in_radians)
            rot_c = construct_rx_matrix(angle_c, is_in_radians)
            break

        if sequence == 'xzx':
            rot_a = construct_rx_matrix(angle_a, is_in_radians)
            rot_b = construct_rz_matrix(angle_b, is_in_radians)
            rot_c = construct_rx_matrix(angle_c, is_in_radians)
            break

        if sequence == 'xyz':
            rot_a = construct_rx_matrix(angle_a, is_in_radians)
            rot_b = construct_ry_matrix(angle_b, is_in_radians)
            rot_c = construct_rz_matrix(angle_c, is_in_radians)
            break

        if sequence == 'xzy':
            rot_a = construct_rx_matrix(angle_a, is_in_radians)
            rot_b = construct_rz_matrix(angle_b, is_in_radians)
            rot_c = construct_ry_matrix(angle_c, is_in_radians)
            break

        if sequence == 'yxy':
            rot_a = construct_ry_matrix(angle_a, is_in_radians)
            rot_b = construct_rx_matrix(angle_b, is_in_radians)
            rot_c = construct_ry_matrix(angle_c, is_in_radians)
            break

        if sequence == 'yzy':
            rot_a = construct_ry_matrix(angle_a, is_in_radians)
            rot_b = construct_rz_matrix(angle_b, is_in_radians)
            rot_c = construct_ry_matrix(angle_c, is_in_radians)
            break

        if sequence == 'yxz':
            rot_a = construct_ry_matrix(angle_a, is_in_radians)
            rot_b = construct_rx_matrix(angle_b, is_in_radians)
            rot_c = construct_rz_matrix(angle_c, is_in_radians)
            break

        if sequence == 'yzx':
            rot_a = construct_ry_matrix(angle_a, is_in_radians)
            rot_b = construct_rz_matrix(angle_b, is_in_radians)
            rot_c = construct_rx_matrix(angle_c, is_in_radians)
            break

        raise ValueError(sequence + " is not a valid sequence.")

    rot_tmp = np.matmul(rot_a, rot_b)
    rot_m = np.matmul(rot_tmp, rot_c)

    return rot_m


def construct_rigid_transformation(rot_m, trans_v):
    """Construct a 4x4 rigid-body transformation from a 3x3 rotation matrix and
    a 3x1 vector as translation

    :param rot_m: 3x3 rotation matrix, numpy array
    :param trans_v: 3x1 vector as translation, numpy array
    :returns: rigid_transformation -- 4x4 rigid transformation matrix,
    numpy array
    """
    rigid_transformation = np.identity(4)

    for i in range(3):
        for j in range(3):
            rigid_transformation[i][j] = rot_m[i][j]

    rigid_transformation[0][3] = trans_v[0]
    rigid_transformation[1][3] = trans_v[1]
    rigid_transformation[2][3] = trans_v[2]

    return rigid_transformation
