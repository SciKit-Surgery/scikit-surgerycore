# coding=utf-8

"""
Various file utilities.
"""
import os


def validate_is_file(file_name):
    """
    Check if file_name exists.
    """
    if os.path.isfile(file_name):
        return True

    raise ValueError('File `' + file_name + '` does not exist')
