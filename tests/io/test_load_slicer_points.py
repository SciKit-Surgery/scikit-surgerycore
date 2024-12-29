# coding=utf-8

""" Tests for load_slicer_points. """

import pytest
import numpy as np
import sksurgerycore.io.load_slicer_points as lsp


def test_load_slicer_points():
    ids, points = lsp.load_slicer_pointset('tests/data/F_5.json')

    expected_ids=[0, 1, 2, 3, 4, 5, 6, 7, 8,9, 10, 11, 12, 13, 14, 15, 16, 17, 18,  19]
    assert np.array_equal(ids, expected_ids)

    expected_point_0 = np.array([-104.41897583007813, -62.68093490600586, -261.3321228027344])
    assert np.allclose(points[0, :], expected_point_0)
    assert points.shape[0] == 20
    assert points.shape[1] == 3
    assert ids.shape[0] == 20



