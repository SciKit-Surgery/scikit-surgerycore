# coding=utf-8

"""
Tests for file_utilities.py
"""

import pytest
from sksurgerycore.utilities import file_utilities as f


def test_invalid_file_name():

    with pytest.raises(ValueError):
        f.validate_is_file("/invalid/file/name")


def test_invalid_file_name_because_directory():

    with pytest.raises(ValueError):
        f.validate_is_file(".")


def test_valid_file_name():

    result = f.validate_is_file("tests/data/FordPrefect.json")
    assert result


def test_valid_writeable_file():

    result = f.validate_is_writable_file("tests/data/FordPrefect.json")
    assert result
