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

    # For passing lint tests only temporary.
    x_values = x_values + 0

    # a,b,c = svd(data)
    #
    # # Zero out diagonal values less than threshold
    #
    # rank = 0
    #
    #
    #
    # for i in range(len(a)):
    #     if a[i,0] < 0.01:
    #         a[i, 0] = 0
    #     if a[i,0] != 0:
    #         rank += 1