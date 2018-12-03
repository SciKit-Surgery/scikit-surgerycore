# coding=utf-8

"""
Various file utilities, often calling standard
functions in the os package, but throwing
nice informative Exception messages.
"""
import os


def validate_is_file(file_name):
    """
    Check if file_name is a file.
    """
    if not file_name:
        raise ValueError("Empty parameter file_name")

    if os.path.isfile(file_name):
        return True

    raise ValueError('File `' + file_name + '` is not a file')


def validate_is_writable_file(file_name):
    """
    Check if file_name is a writable file.
    """
    validate_is_file(file_name)

    if os.access(file_name, os.W_OK):
        return True

    raise ValueError('File `' + file_name + '` is not a writeable file.')
