#  -*- coding: utf-8 -*-

""" Functions for pivot calibration. """

import numpy as np

# pylint: disable=literal-comparison


def pivot_calibration_one_step(tracking_matrices):

    """
    Performs Pivot Calibration, using Algebraic One Step method,
    and returns Residual Error.

    See `Yaniv 2015 <https://dx.doi.org/10.1117/12.2081348>`_.

    :param tracking_matrices: N x 4 x 4 ndarray, of tracking matrices.
    :returns: RMS Error about centroid of pivot
    :raises: TypeError, ValueError
    """
    if not isinstance(tracking_matrices, np.ndarray):
        raise TypeError("tracking_matrices is not a numpy array'")

    if not tracking_matrices.shape[1] == 4:
        raise ValueError("tracking_matrices should have 4 rows per matrix")

    if not tracking_matrices.shape[2] == 4:
        raise ValueError("tracking_matrices should have 4 columns per matrix")

    number_of_matrices = tracking_matrices.shape[0]

    # See equation in section 2.1.2 of Yaniv 2015.
    # Ax = b.

    size_a = 3 * number_of_matrices, 6
    a_values = np.zeros(size_a, dtype=np.float64)

    size_x = 6, 1
    x_values = np.zeros(size_x, dtype=np.float64)

    size_b = 3 * number_of_matrices, 1
    b_values = np.zeros(size_b, dtype=np.float64)

    for i in range(number_of_matrices):

        # Column vector containing -1 * translation from each tracking matrix.
        b_values[i * 3 + 0, 0] = -1 * tracking_matrices[i, 0, 3]
        b_values[i * 3 + 1, 0] = -1 * tracking_matrices[i, 1, 3]
        b_values[i * 3 + 2, 0] = -1 * tracking_matrices[i, 2, 3]

        # A contains rotation matrix from each tracking matrix.
        a_values[i * 3 + 0, 0] = tracking_matrices[i, 0, 0]
        a_values[i * 3 + 1, 0] = tracking_matrices[i, 1, 0]
        a_values[i * 3 + 2, 0] = tracking_matrices[i, 2, 0]
        a_values[i * 3 + 0, 1] = tracking_matrices[i, 0, 1]
        a_values[i * 3 + 1, 1] = tracking_matrices[i, 1, 1]
        a_values[i * 3 + 2, 1] = tracking_matrices[i, 2, 1]
        a_values[i * 3 + 0, 2] = tracking_matrices[i, 0, 2]
        a_values[i * 3 + 1, 2] = tracking_matrices[i, 1, 2]
        a_values[i * 3 + 2, 2] = tracking_matrices[i, 2, 2]

        # A contains -I for each tracking matrix.
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

    return np.matrix(x_values), residual_error
