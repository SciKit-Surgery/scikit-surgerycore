#  -*- coding: utf-8 -*-
"""Tests for algorithm errors"""
import numpy as np
import pytest
import sksurgerycore.algorithms.errors as e


def test_empty_fixed():
    """Raise type error fixed or moving is not a numpy array"""
    with pytest.raises(TypeError):
        e.compute_fre(None, None, np.ones(1, 3), np.ones(3, 3))
