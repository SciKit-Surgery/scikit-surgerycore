# coding=utf-8

"""
Various validation functions.
"""


def validate_is_string_or_number(var):
    """
    Checks if the input is either a str, int or float.

    :param var: input
    :raises: TypeError if not
    :returns: True
    """
    valid_types = (str, int, float)
    if not isinstance(var, valid_types):
        raise TypeError("Input is not a string or a number:" + str(var))

    return True


def validate_width_height(dims):
    """
    Checks if dims (width, height) is a valid specification,
    meaning width and height are both integers above zero.

    :param dims: (width, height)
    :raises: TypeError, ValueError
    :returns: True
    """
    if dims is None:
        raise ValueError("Null input for (width, height).")

    width, height = dims

    if not isinstance(width, int):
        raise TypeError("Width should be an integer.")

    if not isinstance(height, int):
        raise TypeError("Height should be an integer.")

    if width < 1:
        raise ValueError("Width should be >= 1.")

    if height < 1:
        raise ValueError("Height should be >= 1.")

    return True
