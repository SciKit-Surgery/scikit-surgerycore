#  -*- coding: utf-8 -*-
"""Tests for pivot calibration algorithms"""
import pytest
import sksurgerycore.algorithms.pivot as p


def test_pivot():
    """Raise Not implemented error"""
    with pytest.raises(NotImplementedError):
        p.pivot_calibration(None)


def test_pivot_with_ransac():
    """Raise Not implemented error"""
    with pytest.raises(NotImplementedError):
        p.pivot_calibration_with_ransac(None, None, None, None)
