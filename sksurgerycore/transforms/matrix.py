"""
Construct 3x3 rotation matrices for rotating around the x, y and z axes
individually, as well as 3x3 rotation matrices from sequences of three
Euler angles.
"""

import numpy as np

def _to_radians(angle, is_in_radians):
    """
    Internal function to convert angle to radians
    :param angle: float or int, the angle, must be float if in radians,
        can be int or float if in degrees
    :param: is_in_radians, bool, True if angle is already in radians
    """
    if is_in_radians:
        if not isinstance(angle, (np.float32, np.float64, float)):
            raise TypeError("Angle should be float, float32, or float64 when "
                            "using radians not ",  type(angle))
        return angle

    if not isinstance(angle, (int, np.float32, np.float64, float)):
        raise TypeError("Angle should be int, float, float32, or float64 when "
                            "using degrees not ",  type(angle))

    return np.pi * angle / 180.0


def construct_rx_matrix(angle, is_in_radians=True):
    """
    Construct a rotation matrix for rotation around the x axis.

    :param angle: the angle to rotate radians, float
    :returns: rot_x -- the 3x3 rotation matrix constructed, numpy array
    :raises: TypeError if angle is not float or int
    """
    angle = _to_radians(angle, is_in_radians)

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
    :raises: TypeError if angle is not float or int
    """
    angle = _to_radians(angle, is_in_radians)

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
    :raises: TypeError if angle is not float or int
    """
    angle = _to_radians(angle, is_in_radians)

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

    :param angle_a: first Euler angle, float, int allowed if in degrees
    :param angle_b: second Euler angle, float, int allowed if in degrees
    :param angle_c: third Euler angle, float, int allowed if in degrees
    :param sequence: the sequence of axes the three elemental rotations are
        about, with respect to the intrinsic axes, string
    :param is_in_radians: if the angles are in radians, default being True,
        bool
    :returns: rot_m -- the 3x3 rotation matrix, numpy array
    :raises: TypeError if angles are not float or of difference types
    :raises: ValueError if sequence is not 3 letters long or contains letters
        other than x, y or z
    """
    if not (isinstance(angle_b, type(angle_a)) and
                isinstance(angle_c, type(angle_a))):
        raise TypeError("All input angles should be same type")

    rot_matrices = []
    angles = [angle_a, angle_b, angle_c]
    if len(sequence) == 3:
        for index, letter in enumerate(sequence):
            if letter not in 'xyz':
                raise ValueError(sequence + " is not a valid sequence.")
            if letter == 'x':
                rot_matrices.append(construct_rx_matrix(angles[index],
                        is_in_radians))
            if letter == 'y':
                rot_matrices.append(construct_ry_matrix(angles[index],
                        is_in_radians))
            if letter == 'z':
                rot_matrices.append(construct_rz_matrix(angles[index],
                        is_in_radians))
    else:
        raise ValueError(sequence + " is not a valid sequence.")

    rot_tmp = np.matmul(rot_matrices[0], rot_matrices[1])
    rot_m = np.matmul(rot_tmp, rot_matrices[2])

    return rot_m


def construct_rigid_transformation(rot_m, trans_v):
    """
    Construct a 4x4 rigid-body transformation from a 3x3 rotation matrix and
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

    # While the specification is [3x1] which implies ndarray, the users
    # may also pass in array (3,), ndarray (3, 1) or ndarray (1, 3).
    # So, this will flatten all of them to the same array-like shape.
    # In keeping with the rotation matrix, no range checking.
    t_v = np.ravel(trans_v)

    rigid_transformation[0][3] = t_v[0]
    rigid_transformation[1][3] = t_v[1]
    rigid_transformation[2][3] = t_v[2]

    return rigid_transformation
