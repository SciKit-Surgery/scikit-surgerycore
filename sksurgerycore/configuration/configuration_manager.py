#  -*- coding: utf-8 -*-

"""Class to load application configuration information from file."""

import json
import sksurgerycore.utilities.file_utilities as f


class ConfigurationManager:
    """
    Class to load application configuration for example
    at startup of an application.

    :param: config_file
    :raises: ValueError
    """
    def __init__(self, file_name, write_on_shutdown=False):
        """
        Constructor.

        :params: file_name, a json file to read
        :params: write_on_shutdown, if True, will write back to the same
        file when the destructor is called.
        """
        if not file_name:
            raise ValueError("Empty file_name")

        f.validate_is_file(file_name)

        with open(file_name, "r") as read_file:
            self.data = json.load(read_file)

        self.file_name = file_name
        self.write_on_shutdown = write_on_shutdown
