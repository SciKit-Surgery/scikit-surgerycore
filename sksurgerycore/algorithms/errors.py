#  -*- coding: utf-8 -*-

""" Registration Error Calculations """

import numpy as np
import sksurgerycore.algorithms.vector_math as vm


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


def compute_tre_from_fle(fiducials, mean_fle_squared, target_point):
    """
    Computes an estimation of TRE from FLE and a list of fiducial locations.

    See:
    `Fitzpatrick (1998), equation 46 <http://dx.doi.org/10.1109/42.736021>`_.

    :param fiducials: Nx3 ndarray of fiducial points
    :param mean_fle_squared: expected (mean) FLE squared
    :param target_point: a point for which to compute TRE.
    :return: mean TRE squared
    """
    # pylint: disable=literal-comparison
    if not isinstance(fiducials, np.ndarray):
        raise TypeError("fiducials is not a numpy array'")
    if not fiducials.shape[1] == 3:
        raise ValueError("fiducials should have 3 columns")
    if fiducials.shape[0] < 3:
        raise ValueError("fiducials should have at least 3 rows")
    if not isinstance(target_point, np.ndarray):
        raise TypeError("target_point is not a numpy array'")
    if not target_point.shape[1] == 3:
        raise ValueError("target_point should have 3 columns")
    if not target_point.shape[0] == 1:
        raise ValueError("target_point should have 1 row")

    number_of_fiducials = fiducials.shape[0]
    centroid = np.mean(fiducials, axis=0)
    covariance = np.cov(fiducials.T)
    assert covariance.shape[0] == 3
    assert covariance.shape[1] == 3
    _, eigen_vectors_matrix = np.linalg.eig(covariance)

    f_array = np.zeros(3)
    for axis_index in range(3):
        sum_f_k_squared = 0
        for fiducial_index in range(fiducials.shape[0]):
            f_k = vm.distance_from_line(centroid,
                                        eigen_vectors_matrix[axis_index],
                                        fiducials[fiducial_index])
            sum_f_k_squared = sum_f_k_squared + f_k * f_k
        f_k_rms = np.sqrt(sum_f_k_squared / number_of_fiducials)
        f_array[axis_index] = f_k_rms

    inner_sum = 0
    for axis_index in range(3):
        d_k = vm.distance_from_line(centroid,
                                    eigen_vectors_matrix[axis_index],
                                    target_point)
        inner_sum = inner_sum + (d_k * d_k / (f_array[axis_index] *
                                              f_array[axis_index]))

    mean_tre_squared = (mean_fle_squared / fiducials.shape[0]) * \
                       (1 + (1./3.) * inner_sum)
    return mean_tre_squared


def compute_fre_from_fle(fiducials, mean_fle_squared):
    """
    Computes an estimation of FRE from FLE and a list of fiducial locations.

    See:
    `Fitzpatrick (1998), equation 10 <http://dx.doi.org/10.1109/42.736021>`_.

    :param fiducials: Nx3 ndarray of fiducial points
    :param mean_fle_squared: expected (mean) FLE squared
    :return: mean FRE squared
    """
    # pylint: disable=literal-comparison
    if not isinstance(fiducials, np.ndarray):
        raise TypeError("fiducials is not a numpy array'")
    if not fiducials.shape[1] == 3:
        raise ValueError("fiducials should have 3 columns")
    if fiducials.shape[0] < 3:
        raise ValueError("fiducials should have at least 3 rows")

    number_of_fiducials = fiducials.shape[0]

    fre_sq = (1 - (2.0 / number_of_fiducials)) * mean_fle_squared
    return fre_sq
