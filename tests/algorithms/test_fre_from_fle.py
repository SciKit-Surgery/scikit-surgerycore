#  -*- coding: utf-8 -*-

""" Tests concerning computing TRE from FLE. """

# pylint: skip-file

import pytest
import numpy as np
import sksurgerycore.algorithms.errors as err


def measure_fre_1(mean_fle_squared):

    fiducials = np.zeros((4, 3))
    fiducials[0][0] = 1
    fiducials[0][1] = 1
    fiducials[1][0] = -0.5
    fiducials[1][1] = 0.5
    fiducials[2][0] = -1
    fiducials[2][1] = -1
    fiducials[3][0] = 0.5
    fiducials[3][1] = -0.5

    error = err.compute_fre_from_fle(fiducials, mean_fle_squared)
    return error

def test_fre_origin_zero_fle():
    target = np.zeros((1, 3))
    error = measure_fre_1(0)
    assert np.isclose(error, 0)


def test_fre_origin_1mm_fle():
    target = np.zeros((1, 3))
    error = measure_fre_1(1)
    assert np.isclose(error, 0.5)


def test_invalid_because_fiducials_wrong_type():
    with pytest.raises(TypeError):
        err.compute_fre_from_fle("not an arrray", 1)


def test_invalid_because_fiducials_wrong_columns():
    with pytest.raises(ValueError):
        err.compute_fre_from_fle(np.ones((1,4)), 1)


def test_invalid_because_fiducials_wrong_rows():
    with pytest.raises(ValueError):
        err.compute_fre_from_fle(np.ones((2, 3)), 1)

