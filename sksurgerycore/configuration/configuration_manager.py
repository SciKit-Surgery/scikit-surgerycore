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

import os
import json
import copy
import sksurgerycore.utilities.file_utilities as fu
import sksurgerycore.utilities.validate_file as f


class ConfigurationManager:
    # pylint: disable=line-too-long
    """ Class to load application configuration from a json file.
    For example, this might be used at the startup of an application.

    :param file_name: a json file to read.
    :param write_on_setter: if True, will write back to the same file whenever the setter is called.
    :raises: All errors raised as various Exceptions.
    """
    def __init__(self, file_name,
                 write_on_setter=False
                 ):

        abs_file = fu.get_absolute_path_of_file(file_name)
        f.validate_is_file(abs_file)

        if write_on_setter:
            f.validate_is_writable_file(abs_file)

        with open(abs_file, "r") as read_file:
            self.config_data = json.load(read_file)

        self.file_name = abs_file
        self.write_on_setter = write_on_setter

    def get_file_name(self):
        """
        Returns the absolute filename that was used when
        the ConfigurationManager was created.

        :return: str absolute file name
        """
        return self.file_name

    def get_dir_name(self):
        """
        Returns the directory name of the file that was used when
        creating the ConfigurationManager.

        :return: str dir name
        """
        return os.path.dirname(self.file_name)

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
