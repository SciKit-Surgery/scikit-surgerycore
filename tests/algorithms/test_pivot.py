#  -*- coding: utf-8 -*-

# import six
import numpy as np
import pytest
import sksurgerycore.algorithms.pivot as p
from glob import glob


def test_empty_matrices4x4():
    with pytest.raises(TypeError):
        p.pivot_calibration(None)


def test_range_le_six():
    with pytest.raises(SystemExit):
        file_names = glob('tests/algorithms/PivotCalibration/1378476416922755200.txt')
        arrays = [np.loadtxt(f) for f in file_names]
        matrices = np.concatenate(arrays)
        numberOf4x4Matrices = int(matrices.size/16)
        matrices4x4 = matrices.reshape(numberOf4x4Matrices, 4, 4)
        p.pivot_calibration(matrices4x4)


def test_four_columns_matrices4x4():
    with pytest.raises(ValueError):
        p.pivot_calibration(np.arange(2, 11, dtype=float).reshape(3, 3))


def test_four_rows_matrices4x4():
    with pytest.raises(ValueError):
        p.pivot_calibration(np.arange(2, 11, dtype=float).reshape(3, 3))


def test_return_value():
    file_names = glob('tests/algorithms/PivotCalibration/*')
    arrays = [np.loadtxt(f) for f in file_names]
    matrices = np.concatenate(arrays)
    numberOf4x4Matrices = int(matrices.size/16)
    matrices4x4 = matrices.reshape(numberOf4x4Matrices, 4, 4)
    p.pivot_calibration(matrices4x4)




