import numpy as np
import pytest

import sksurgerycore.transforms.matrix as mat
import sksurgerycore.utilities.validate_matrix as vm


def check_construct_rx_matrix(angle, point):
    """"
    Test if the rotation matrix for rotating around the x axis is correct.

    :param angle: the angle to rotate
    :param point: the point to be rotated
    """

    rot_x = mat.construct_rx_matrix(angle, 0)
    vm.validate_rotation_matrix(rot_x)

    new_point = np.dot(rot_x, point)

    assert new_point[0] == point[0]
    assert np.linalg.norm(new_point) == np.linalg.norm(point)


def test_construct_rx_matrix():

    check_construct_rx_matrix(90, np.array([0, 1, 0]).T)
