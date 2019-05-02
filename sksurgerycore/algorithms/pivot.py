#  -*- coding: utf-8 -*-
"""Functions for pivot calibration."""

import numpy as np


def pivot_calibration(matrices4x4):

    """
    Performs Pivot Calibration and returns Residual Error.

    1. matricesNx4x4 and moving must be numpy array
    2. matricesNx4x4 and moving should have 4 columns
    3. matricesNx4x4 and moving should have at least 4 rows

    :param matrices4x4: point set, N x 4 x 4 ndarray
    :returns: residual_error
    :raises: TypeError, ValueError
    """
    if not isinstance(matrices4x4, np.ndarray):
        raise TypeError("matrices4x4 is not a numpy array'")

    if not matrices4x4.shape[1] == 4:  # pylint: disable=literal-comparison
        raise ValueError("matrices4x4 should have 4 columns per matrix")

    number_of_matrices = len(matrices4x4)

    size_a = 3 * number_of_matrices, 6
    a_values = np.zeros(size_a, dtype=np.float64)

    size_x = 6, 1
    x_values = np.zeros(size_x, dtype=np.float64)

    size_b = 3 * number_of_matrices, 1
    b_values = np.zeros(size_b, dtype=np.float64)

    for i in range(number_of_matrices):
        b_values[i * 3 + 0, 0] = -1 * matrices4x4[i, 0, 3]
        b_values[i * 3 + 1, 0] = -1 * matrices4x4[i, 1, 3]
        b_values[i * 3 + 2, 0] = -1 * matrices4x4[i, 2, 3]

        a_values[i * 3 + 0, 0] = matrices4x4[i, 0, 0]
        a_values[i * 3 + 1, 0] = matrices4x4[i, 1, 0]
        a_values[i * 3 + 2, 0] = matrices4x4[i, 2, 0]
        a_values[i * 3 + 0, 1] = matrices4x4[i, 0, 1]
        a_values[i * 3 + 1, 1] = matrices4x4[i, 1, 1]
        a_values[i * 3 + 2, 1] = matrices4x4[i, 2, 1]
        a_values[i * 3 + 0, 2] = matrices4x4[i, 0, 2]
        a_values[i * 3 + 1, 2] = matrices4x4[i, 1, 2]
        a_values[i * 3 + 2, 2] = matrices4x4[i, 2, 2]

        a_values[i * 3 + 0, 3] = -1
        a_values[i * 3 + 1, 3] = 0
        a_values[i * 3 + 2, 3] = 0
        a_values[i * 3 + 0, 4] = 0
        a_values[i * 3 + 1, 4] = -1
        a_values[i * 3 + 2, 4] = 0
        a_values[i * 3 + 0, 5] = 0
        a_values[i * 3 + 1, 5] = 0
        a_values[i * 3 + 2, 5] = -1

    # To calculate Singular Value Decomposition

    u_values, s_values, v_values = np.linalg.svd(a_values, full_matrices=False)
    c_values = np.dot(u_values.T, b_values)
    w_values = np.linalg.solve(np.diag(s_values), c_values)
    x_values = np.dot(v_values.T, w_values)

    # Back substitution

    # Calculating the rank

    rank = 0
    for i, item in enumerate(s_values):
        if item < 0.01:
            item = 0
        if item != 0:
            rank += 1

    if rank < 6:  # pylint: disable=literal-comparison
        raise ValueError("PivotCalibration: Failed. Rank < 6")

    # Residual Matrix

    residual_matrix = (np.dot(a_values, x_values) - b_values)
    residual_error = 0.0
    for i in range(number_of_matrices * 3):
        residual_error = residual_error + \
                         np.dot(residual_matrix[i, 0],
                                residual_matrix[i, 0])

    residual_error = residual_error / float(number_of_matrices * 3)
    residual_error = np.sqrt(residual_error)

    # Output
    # MakeIdentity matrix

    # output_matrix = np.identity(4)
    #
    # output_matrix[0, 3] = x_values[0, 0]
    # output_matrix[1, 3] = x_values[1, 0]
    # output_matrix[2, 3] = x_values[2, 0]

    # print("pivotCalibration=(", x_values[3, 0], ","
    #       , x_values[4, 0], ",", x_values[5, 0],
    #       "),residual=", residual_error)

    # print(x_values)

    return np.matrix(x_values), residual_error
