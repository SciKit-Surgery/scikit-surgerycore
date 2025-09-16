# -*- coding: utf-8 -*-

""" File processing utils. """

import os
import pytest

import sksurgerycore.utilities.file_utilities as fu

def test_get_absolute_file_exceptions():
    with pytest.raises(ValueError) as excinfo:
        fu.get_absolute_path_of_file(None)
    assert "file_name is None." in str(excinfo.value)

    with pytest.raises(TypeError) as excinfo:
        fu.get_absolute_path_of_file(123)
    assert "file_name is not a string." in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        fu.get_absolute_path_of_file("   ")
    assert "file_name is empty." in str(excinfo.value)

    with pytest.raises(TypeError) as excinfo:
        fu.get_absolute_path_of_file("file.txt", dir_name=123)
    assert "dir_name is not a string." in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        fu.get_absolute_path_of_file("file.txt", dir_name="   ")
    assert "dir_name is empty." in str(excinfo.value)

def test_get_absolute_file():

    cwd = os.getcwd()
    this_file = "tests/utilities/test_file_utilities.py"

    fp = fu.get_absolute_path_of_file(this_file)
    assert fp == os.path.join(cwd, fp)

    fp2 = fu.get_absolute_path_of_file(fp)
    assert fp2 == fp

    fp3 = fu.get_absolute_path_of_file(this_file, cwd)
    assert fp3 == fp

    # Similar to test for fp, but file doesn't exist.
    # So, really just checking that we always get an absolute path.
    fp4 = fu.get_absolute_path_of_file("nonsense.txt")
    assert fp4 is not None
    assert os.path.basename(fp4) == "nonsense.txt"
    assert os.path.isabs(fp4)
    assert os.path.dirname(fp4) == cwd