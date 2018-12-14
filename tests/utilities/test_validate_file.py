# coding=utf-8

"""
Tests for file_utilities.py
"""

import pytest
from sksurgerycore.utilities import validate_file as f


def test_invalid_file_name_because_its_null():

    with pytest.raises(ValueError):
        f.validate_is_file(None)


def test_invalid_file_name_because_its_empty():

    with pytest.raises(ValueError):
        f.validate_is_file("")


def test_invalid_file_name_because_its_an_integer():

    with pytest.raises(TypeError):
        f.validate_is_file(1)


def test_invalid_file_name_because_non_existent():

    with pytest.raises(ValueError):
        f.validate_is_file("/invalid/file/name")


def test_invalid_file_name_because_its_a_directory():

    with pytest.raises(ValueError):
        f.validate_is_file(".")


def test_valid_file_name():

    result = f.validate_is_file("tests/data/FordPrefect.json")
    assert result


def test_valid_writeable_file():

    result = f.validate_is_writable_file("tests/data/FordPrefect.json")
    assert result
