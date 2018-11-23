#  -*- coding: utf-8 -*-

import pytest
import sksurgerycore.configuration.configuration_manager as cm


def test_constructor_with_empty_filename():

    with pytest.raises(ValueError):
        cm.ConfigurationManager("")


def test_constructor_with_valid_file():

    manager = cm.ConfigurationManager("tests/data/FordPrefect.json")
    assert manager is not None


def test_constructor_with_valid_read_only_file():

    manager = cm.ConfigurationManager("tests/data/Unwritable.json", False)
    assert manager is not None


def test_constructor_fails_if_file_should_be_writable():

    with pytest.raises(ValueError):
        cm.ConfigurationManager("tests/data/Unwritable.json", True)


def test_setter_getter_loop():

    manager = cm.ConfigurationManager("tests/data/FordPrefect.json")
    d = manager.get_copy()
    d["researcher"]["name"] = "Ford Anglia"
    manager.set_data(d)
    e = manager.get_copy()
    assert e["researcher"]["name"] == "Ford Anglia"
