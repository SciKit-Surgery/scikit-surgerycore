#  -*- coding: utf-8 -*-

"""Functions for point based registration using Orthogonal Procrustes."""

import numpy as np


def validate_procrustes_inputs(fixed, moving):
    """
    Validates the fixed and moving set of points

    1. fixed and moving must be numpy array
    2. fixed and moving should have 3 columns
    3. fixed and moving should have at least 3 rows
    4. fixed and moving should have the same number of rows

    :param fixed: point set, N x 3 ndarray
    :param moving: point set, N x 3 ndarray of corresponding points
    :returns: nothing
    :raises: TypeError, ValueError
    """
    if not isinstance(fixed, np.ndarray):
        raise TypeError("fixed is not a numpy array'")

    if not isinstance(moving, np.ndarray):
        raise TypeError("moving is not a numpy array")

    if not fixed.shape[1] == 3:  # pylint: disable=literal-comparison
        raise ValueError("fixed should have 3 columns")

    if not moving.shape[1] == 3:  # pylint: disable=literal-comparison
        raise ValueError("moving should have 3 columns")

    if fixed.shape[0] < 3:
        raise ValueError("fixed should have at least 3 points (rows)")

    if moving.shape[0] < 3:
        raise ValueError("moving should have at least 3 points (rows)")

    if not fixed.shape[0] == moving.shape[0]:
        raise ValueError("fixed and moving should have "
                         + "the same number of points (rows)")


def compute_fre(fixed, moving, rotation, translation):
    """
    Computes the Fiducial Registration Error, equal
    to the root mean squared error between corresponding fiducials.

    :param fixed: point set, N x 3 ndarray
    :param moving: point set, N x 3 ndarray of corresponding points
    :param rotation: 3 x 3 ndarray
    :param translation: 3 x 1 ndarray
    :returns: Fiducial Registration Error (FRE)
    """
    # pylint: disable=assignment-from-no-return

    validate_procrustes_inputs(fixed, moving)

    transformed_moving = np.matmul(rotation, moving.transpose()) + translation
    squared_error_elementwise = np.square(fixed
                                          - transformed_moving.transpose())
    square_distance_error = np.sum(squared_error_elementwise, 1)
    sum_squared_error = np.sum(square_distance_error, 0)
    mean_squared_error = sum_squared_error / fixed.shape[0]
    fre = np.sqrt(mean_squared_error)
    return fre
