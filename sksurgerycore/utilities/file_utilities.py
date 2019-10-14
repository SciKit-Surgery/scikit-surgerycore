# -*- coding: utf-8 -*-

""" File processing utils. """

import os


def get_absolute_path_of_file(file_name, dir_name=None):
    """
    Filenames in our .json config could be absolute or relative to the
    current working dir. This method tries to find the valid, full file path.

    :param file_name:
    :param dir_name: prefix, for example, the dirname of our .json file.
    :return: absolute path name of file if found, otherwise None.
    """
    if not file_name:
        raise ValueError("Empty file_name.")
    file = None
    if os.path.isabs(file_name):
        if os.path.isfile(file_name):
            file = file_name
    elif dir_name is not None:
        joined = os.path.join(dir_name, file_name)
        if os.path.isfile(joined):
            file = joined
    elif os.getcwd() is not None:
        joined = os.path.join(os.getcwd(), file_name)
        if os.path.isfile(joined):
            file = joined
    return file
