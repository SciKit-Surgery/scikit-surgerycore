# -*- coding: utf-8 -*-

""" File processing utils. """

import os
import pytest

import sksurgerycore.utilities.file_utilities as fu


def test_get_absolute_file():

    cwd = os.getcwd()
    this_file = "tests/utilities/test_file_utilities.py"

    fp = fu.get_absolute_path_of_file(this_file)
    assert fp == os.path.join(cwd, fp)

    fp2 = fu.get_absolute_path_of_file(fp)
    assert fp2 == fp

    fp3 = fu.get_absolute_path_of_file(this_file, cwd)
    assert fp3 == fp
