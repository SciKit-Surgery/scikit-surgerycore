#  -*- coding: utf-8 -*-

import pytest
import sksurgerycore.configuration.configuration_manager as cm


def test_constructor_fails_with_null_filename():

    with pytest.raises(ValueError):
        cm.ConfigurationManager(None)


def test_constructor_fails_with_empty_filename():

    with pytest.raises(ValueError):
        cm.ConfigurationManager("")


def test_constructor_with_valid_file():

    manager = cm.ConfigurationManager("tests/data/FordPrefect.json")
    assert manager is not None


def test_setter_getter_loop():

    m = cm.ConfigurationManager("tests/data/FordPrefect.json")
    d = m.get_copy()
    d["researcher"]["name"] = "Ford Anglia"
    m.set_data(d)
    e = m.get_copy()
    assert e["researcher"]["name"] == "Ford Anglia"
