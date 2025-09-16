# -*- coding: utf-8 -*-

""" File processing utils. """

import os


def get_absolute_path_of_file(file_name, dir_name=None):
    """
    This method tries to setup an absolute pathname.
    Tt doesn't actually check if the file exists.
    If dir_name is provided, it is used as a prefix.
    If dir_name is None, the function is equivalent
    to os.path.abspath(file_name).

    :param file_name: str, the file name to convert to absolute path.
    :param dir_name: str or None, optional prefix directory.
    :return: absolute path name
    :raises ValueError if file_name is empty or None.
    """
    if file_name is None:
        raise ValueError("file_name is None.")
    if not isinstance(file_name, str):
        raise TypeError("file_name is not a string.")
    if file_name.strip() == "":
        raise ValueError("file_name is empty.")
    fname = file_name.strip()
    if dir_name is not None:
        if not isinstance(dir_name, str):
            raise TypeError("dir_name is not a string.")
        if dir_name.strip() == "":
            raise ValueError("dir_name is empty.")
        dir_name = dir_name.strip()
        fname = os.path.join(dir_name, fname)
    return os.path.abspath(fname)
