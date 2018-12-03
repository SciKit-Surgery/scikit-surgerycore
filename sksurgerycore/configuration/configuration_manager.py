#  -*- coding: utf-8 -*-

"""
Class to load application configuration information from a json file.

Design principles:
  - All errors as Exceptions
  - | Fail early in constructor, so the rest of the program never
    | has an invalid instance of ConfigurationManager.
    | If its constructed, its valid.
  - Setter and Getter do a deepcopy, so only suitable for small config files.
  - | Pass ConfigurationManager to any consumer of the data,
    | its up to the consumer to know where to find the data.
"""

import json
import copy
import sksurgerycore.utilities.validate_file as f


class ConfigurationManager:
    # pylint: disable=line-too-long
    """ Class to load application configuration from a json file.
    For example, this might be used at the startup of an application.

    :param file_name: a json file to read.
    :param write_on_shutdown: if True, will write back to the same file when the destructor is called.
    :param write_on_setter: if True, will write back to the same file whenever the setter is called.
    :raises: All errors raised as various Exceptions.
    """
    def __init__(self, file_name,
                 write_on_shutdown=False,
                 write_on_setter=False
                 ):
        """ Constructor. """
        f.validate_is_file(file_name)

        if write_on_shutdown or write_on_setter:
            f.validate_is_writable_file(file_name)

        with open(file_name, "r") as read_file:
            self.config_data = json.load(read_file)

        self.file_name = file_name
        self.write_on_shutdown = write_on_shutdown
        self.write_on_setter = write_on_setter

    def __del__(self):
        """ If the constructor was passed write_on_shutdown=True,
        then the destructor will attempt to save back the config into
        the file that it was read from.
        """
        if self.write_on_shutdown:
            self._save_back_to_file()

    def get_copy(self):
        """ Returns a copy of the data read from file.

        :returns: deep copy of whatever data structure is stored internally.
        """
        return copy.deepcopy(self.config_data)

    def set_data(self, config_data):
        """ Stores the provided data internally.

        Note that: you would normally load settings from disk,
        and then use get_copy() to get a copy, change some settings,
        and then use set_data() to pass the data structure back in.
        So, the data provided for this method should still represent
        the settings you want to save, not just be a completely
        arbitrary data structure.

        :param config_data: data structure representing your settings.
        """
        if self.write_on_setter:
            self._save_back_to_file()

        self.config_data = copy.deepcopy(config_data)

    def _save_back_to_file(self):
        """ Writes the internal data back to the filename
        provided during object construction.
        """
        with open(self.file_name, "w") as write_file:
            json.dump(self.config_data, write_file)
