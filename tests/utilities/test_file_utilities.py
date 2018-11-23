# coding=utf-8

"""
Tests for file_utilities.py
"""
import pytest
import six
import os
from sksurgerycore.utilities import file_utilities as f


def test_invalid_file_name():

    with pytest.raises(ValueError):
        f.validate_is_file("/invalid/file/name")


def test_valid_file_name():

    six.print_("pwd=" + os.getcwd())
    result = f.validate_is_file("data/FordPrefect.json")
    assert result
