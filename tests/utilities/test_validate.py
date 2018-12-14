# coding=utf-8

"""
Tests for validate.py
"""

import pytest
from sksurgerycore.utilities import validate as v


def test_is_string_or_number():

    string = "test"
    integer = 1
    fp = 1.01
    list_invalid = [1, 2, 3]

    assert v.validate_is_string_or_number(string)
    assert v.validate_is_string_or_number(integer)
    assert v.validate_is_string_or_number(fp)

    with pytest.raises(TypeError):
        v.validate_is_string_or_number(list_invalid)


def test_width_height_invalid_because_none_input():
    with pytest.raises(ValueError):
        v.validate_width_height(None)


def test_width_height_invalid_because_empty_input():
    with pytest.raises(ValueError):
        v.validate_width_height(())


def test_width_height_invalid_because_width_wrong_type():
    with pytest.raises(TypeError):
        v.validate_width_height(("", 2))


def test_width_height_invalid_because_width_too_low():
    with pytest.raises(ValueError):
        v.validate_width_height((0, 2))


def test_width_height_invalid_because_height_wrong_type():
    with pytest.raises(TypeError):
        v.validate_width_height((1, ""))


def test_width_height_invalid_because_height_too_low():
    with pytest.raises(ValueError):
        v.validate_width_height((1, 0))


def test_width_height_valid():
    assert v.validate_width_height((1, 1))
