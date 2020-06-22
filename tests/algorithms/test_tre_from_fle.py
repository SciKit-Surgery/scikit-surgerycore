#  -*- coding: utf-8 -*-

""" Tests concerning computing TRE from FLE. """

# pylint: skip-file

import pytest
import numpy as np
import sksurgerycore.algorithms.errors as err


def measure_tre_1(mean_fle_squared, target):

    fiducials = np.zeros((4, 3))
    fiducials[0][0] = 1
    fiducials[0][1] = 1
    fiducials[1][0] = -0.5
    fiducials[1][1] = 0.5
    fiducials[2][0] = -1
    fiducials[2][1] = -1
    fiducials[3][0] = 0.5
    fiducials[3][1] = -0.5

    error = err.compute_tre_from_fle(fiducials, mean_fle_squared, target)
    return error


def measure_tre_2(mean_fle_squared, target):
    """This is a square to make checking moment of inertia easier"""
    fiducials = np.zeros((4, 3))
    fiducials[0][0] = 1
    fiducials[0][1] = 1
    fiducials[1][0] = -1
    fiducials[1][1] = 1
    fiducials[2][0] = 1
    fiducials[2][1] = -1
    fiducials[3][0] = -1
    fiducials[3][1] = -1

    error = err.compute_tre_from_fle(fiducials, mean_fle_squared, target)
    return error


def test_tre_origin_zero_fle():
    target = np.zeros((1, 3))
    error = measure_tre_1(0, target)
    assert np.isclose(error, 0)


def test_tre_origin_1mm_fle():
    target = np.zeros((1, 3))
    error = measure_tre_1(1, target)
    assert np.isclose(error, 0.25)


def test_tre_origin_1mm_fle_non_zero_target():
    target = np.zeros((1, 3))
    target[0][0] = 2
    error = measure_tre_1(1, target)
    assert np.isclose(error, 1.35)


def test_tre_2_origin_1mm_fle_non_zero_target():
    target = np.zeros((1, 3))
    target[0][0] = 2
    error = measure_tre_2(1, target)
    #now should be 1/4 * (1+ 1/3 * (0/1.0 + 4.0/1.0 + 4 / 2))
    #0.25 * (1 + 2) = 0.75
    assert np.isclose(error, 0.75)


def test_invalid_because_fiducials_wrong_type():
    with pytest.raises(TypeError):
        err.compute_tre_from_fle("not an arrray", 1, np.ones((1, 3)))


def test_invalid_because_fiducials_wrong_columns():
    with pytest.raises(ValueError):
        err.compute_tre_from_fle(np.ones((1,4)), 1, np.ones((1, 3)))


def test_invalid_because_fiducials_wrong_rows():
    with pytest.raises(ValueError):
        err.compute_tre_from_fle(np.ones((2, 3)), 1, np.ones((1, 3)))


def test_invalid_because_target_wrong_type():
    with pytest.raises(TypeError):
        err.compute_tre_from_fle(np.ones((3, 3)), 1, "not an array")


def test_invalid_because_target_wrong_columns():
    with pytest.raises(ValueError):
        err.compute_tre_from_fle(np.ones((3, 3)), 1, np.ones((1, 4)))


def test_invalid_because_fiducials_wrong_rows():
    with pytest.raises(ValueError):
        err.compute_tre_from_fle(np.ones((3, 3)), 1, np.ones((2, 3)))
