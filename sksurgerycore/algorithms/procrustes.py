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
    validate_procrustes_inputs(fixed, moving)

    transformed_moving = np.matmul(rotation, moving.transpose()) + translation
    squared_error_elementwise = np.square(fixed
                                          - transformed_moving.transpose())
    square_distance_error = np.sum(squared_error_elementwise, 1)
    sum_squared_error = np.sum(square_distance_error, 0)
    mean_squared_error = sum_squared_error / fixed.shape[0]
    fre = np.sqrt(mean_squared_error)
    return fre


# pylint: disable=invalid-name, line-too-long
def orthogonal_procrustes(fixed, moving):
    """
    Implements point based registration via the Orthogonal Procrustes method.

    Based on Arun's method:

      Least-Squares Fitting of two, 3-D Point Sets, Arun, 1987,
      `10.1109/TPAMI.1987.4767965 <http://dx.doi.org/10.1109/TPAMI.1987.4767965>`_.

    Also see `this <http://eecs.vanderbilt.edu/people/mikefitzpatrick/papers/2009_Medim_Fitzpatrick_TRE_FRE_uncorrelated_as_published.pdf>`_
    and `this <http://tango.andrew.cmu.edu/~gustavor/42431-intro-bioimaging/readings/ch8.pdf>`_.

    :param fixed: point set, N x 3 ndarray
    :param moving: point set, N x 3 ndarray of corresponding points
    :returns: 3x3 rotation ndarray, 3x1 translation ndarray, FRE
    :raises: ValueError
    """

    validate_procrustes_inputs(fixed, moving)

    # This is what we are calculating
    R = np.eye(3)
    T = np.zeros((3, 1))

    # Arun equation 4
    p = np.ndarray.mean(moving, 0)

    # Arun equation 6
    p_prime = np.ndarray.mean(fixed, 0)

    # Arun equation 7
    q = moving - p

    # Arun equation 8
    q_prime = fixed - p_prime

    # Arun equation 11
    H = np.matmul(q.transpose(), q_prime)

    # Arun equation 12
    # Note: numpy factors h = u * np.diag(s) * v
    svd = np.linalg.svd(H)

    # Arun equation 13
    X = np.matmul(svd[2].transpose(), svd[0].transpose())

    # Arun step 5, after equation 13.
    det_X = np.linalg.det(X)

    if det_X < 0 and np.all(np.flip(np.isclose(svd[1], np.zeros((3, 1))))):

        # Don't yet know how to generate test data.
        # If you hit this line, please report it, and save your data.
        raise ValueError("Registration fails as determinant < 0"
                         " and no singular values are close enough to zero")

    elif det_X < 0 and np.any(np.isclose(svd[1], np.zeros((3, 1)))):

        # Implement 2a in section VI in Arun paper.
        v_prime = svd[2].transpose()
        v_prime[0][2] *= -1
        v_prime[1][2] *= -1
        v_prime[2][2] *= -1
        X = np.matmul(v_prime, svd[0].transpose())

    # Compute output
    R = X
    tmp = p_prime.transpose() - np.matmul(R, p.transpose())
    T[0][0] = tmp[0]
    T[1][0] = tmp[1]
    T[2][0] = tmp[2]
    fre = compute_fre(fixed, moving, R, T)

    return R, T, fre
