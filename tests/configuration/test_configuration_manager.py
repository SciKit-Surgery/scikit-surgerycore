#  -*- coding: utf-8 -*-

import pytest
import sksurgerycore.configuration.configuration_manager as cm


def test_constructor_with_empty_filename():

    with pytest.raises(ValueError):
        manager = cm.ConfigurationManager("")


def test_constructor_with_valid_file():

    manager = cm.ConfigurationManager("tests/data/FordPrefect.json")
