#  -*- coding: utf-8 -*-

import numpy as np
import pytest
import sksurgerycore.algorithms.errors as e


def test_empty_fixed():

    with pytest.raises(TypeError):
        e.compute_fre(None, None, np.ones(1, 3), np.ones(3, 3))


