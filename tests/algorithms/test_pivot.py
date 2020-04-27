#  -*- coding: utf-8 -*-

import pytest
import sksurgerycore.algorithms.pivot as p


def test_pivot():
    with pytest.raises(NotImplementedError):
        p.pivot_calibration(None)


def test_pivot_with_ransac():
    with pytest.raises(NotImplementedError):
        p.pivot_calibration_with_ransac(None, None, None, None)
