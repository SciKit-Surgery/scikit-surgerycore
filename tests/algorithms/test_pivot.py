#  -*- coding: utf-8 -*-

# import six
import numpy as np
import pytest
import sksurgerycore.algorithms.pivot as p


def test_empty_matrices4x4():
    with pytest.raises(TypeError):
        p.pivot_calibration(None)


def test_four_columns_matrices4x4():
    with pytest.raises(ValueError):
        p.pivot_calibration(np.arange(2, 11, dtype=float).reshape(3, 3))

def test_four_rows_matrices4x4():
    with pytest.raises(ValueError):
        p.pivot_calibration(np.arange(2, 11, dtype=float).reshape(3, 3))

