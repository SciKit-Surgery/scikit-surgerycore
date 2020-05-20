# coding=utf-8

"""Tests for load_mps"""

import pytest
import sksurgerycore.io.load_mps as lmps


def test_load_mps():
    ids, points = lmps.load_mps('tests/data/pointset.mps')
    assert points.shape[0] == 3
    assert points.shape[1] == 3
    assert ids.shape[0] == 3


