# coding=utf-8

"""Tests for load_mps"""

import pytest
import numpy as np
import sksurgerycore.io.load_mps as lmps


def test_load_mps():
    ids, points = lmps.load_mps('tests/data/pointset.mps')

    expected_ids=[0, 1, 2]
    expected_points = np.array([[10.23520264, -87.04957082, 1773.70202613],
                       [-134.87921472, -19.02479736, 1574.53710377],
                       [111.45323853,  -22.34979736, 1570.03102231]])

    assert np.array_equal(ids, expected_ids)
    assert np.allclose(points, expected_points)
    assert points.shape[0] == 3
    assert points.shape[1] == 3
    assert ids.shape[0] == 3



