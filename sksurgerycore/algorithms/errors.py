#  -*- coding: utf-8 -*-

"""Functions for point based registration using Orthogonal Procrustes."""

import numpy as np
from sksurgerycore.algorithms.procrustes import validate_procrustes_inputs


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
