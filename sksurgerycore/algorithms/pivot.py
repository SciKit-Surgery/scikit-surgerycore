#  -*- coding: utf-8 -*-

"""Functions for pivot calibration."""

import numpy as np
# from numpy.linalg import svd


def pivot_calibration(matrices4x4):
    """
    The function receive [N, 4, 4] matrices.
    """

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
    for i in range(len(s_values)):
        if s_values[i] < 0.01:
            s_values[i] = 0
        if s_values[i] != 0:
            rank += 1
    if rank < 6:
        print("PivotCalibration: Failed. Rank < 6")

    # Residual Matrix

    x_values = np.transpose(x_values)
    residualMatrix = (a_values * x_values - b_values)
    residualError = 0.0;
    for i in range(number_of_matrices * 3):
        residualError = residualError + residualMatrix[i, 0] * residualMatrix[i, 0]

    residualError = residualError / float(number_of_matrices * 3)
    residualError = np.sqrt(residualError)

    # Output
    # MakeIdentity(outputMatrix);

    outputMatrix = np.identity(4)

    x_values = np.transpose(x_values)

    outputMatrix[0, 3] = x_values[0, 0]
    outputMatrix[1, 3] = x_values[1, 0]
    outputMatrix[2, 3] = x_values[2, 0]

    print("DoPivotCalibration:Pivot = (", x_values[3, 0], ", ", x_values[4, 0], ", ",
          x_values[5, 0], "), residual= ", residualError)
    return residualError

