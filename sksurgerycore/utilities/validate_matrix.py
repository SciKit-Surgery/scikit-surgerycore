# coding=utf-8

"""
Various validation routines for checking matrices.
"""

import numpy as np


def validate_camera_matrix(matrix):
    """
    Validates that a matrix is a camera (intrinsic) matrix.

        1. Is a numpy array
        2. Is 2D
        3. Has 3 rows
        4. Has 3 columns

    :param matrix: camera matrix
    :raises: TypeError, ValueError if it fails
    :returns: True
    """
    if not isinstance(matrix, np.ndarray):
        raise TypeError("Camera matrix is not a numpy ndarray.")
    if len(matrix.shape) != 2:
        raise ValueError("Camera matrix should have 2 dimensions.")
    if matrix.shape[0] != 3:
        raise ValueError("Camera matrix should have 3 rows.")
    if matrix.shape[1] != 3:
        raise ValueError("Camera matrix should have 3 columns.")
    return True


# pylint: disable=invalid-name
def validate_distortion_coefficients(matrix):
    """
    Validates that a matrix is a set of OpenCV style distortion coefficients.

      1. Is a numpy array
      2. Is 2D
      3. Has 1 row
      4. Has either 4, 5, 8, 12 or 14 columns


    :param matrix: set of distortion coefficients
    :raises: TypeError, ValueError if if fails
    :returns: True
    """
    if not isinstance(matrix, np.ndarray):
        raise TypeError("Distortion coefficients are not a numpy ndarray.")
    if len(matrix.shape) != 2:
        raise ValueError("Camera matrix should have 2 dimensions.")
    if matrix.shape[0] != 1:
        raise ValueError("Distortion coefficients should have 1 row.")
    if matrix.shape[1] not in [4, 5, 8, 12, 14]:  # See OpenCV docs
        raise ValueError("Distortion coefficients should have "
                         + "4, 5, 8, 12 or 14 columns.")
    return True


def validate_rotation_matrix(matrix):
    """
    Validates that a matrix is rotation matrix.

        1. Is a numpy array
        2. Is 2D
        3. Has 3 rows
        4. Has 3 columns

    :param matrix: rotation matrix
    :raises: TypeError, ValueError if it fails
    :returns: True
    """
    if not isinstance(matrix, np.ndarray):
        raise TypeError("Rotation matrix should be a numpy ndarray.")
    if len(matrix.shape) != 2:
        raise ValueError("Rotation matrix should have 2 dimensions.")
    if matrix.shape[0] != 3:
        raise ValueError("Rotation matrix should have 3 rows.")
    if matrix.shape[1] != 3:
        raise ValueError("Rotation matrix should have 3 columns.")


# pylint: disable=invalid-name
def validate_translation_column_vector(matrix):
    """
    Validates that a translation matrix is a column vector.

        1. Is numpy array
        2. Is 2D
        3. Has 3 rows
        4. Has 1 column

    :param matrix: translation matrix
    :raises: TypeError, ValueError if it fails
    :return: True
    """
    if not isinstance(matrix, np.ndarray):
        raise TypeError("Translation matrix should be a numpy ndarray.")
    if len(matrix.shape) != 2:
        raise ValueError("Translation matrix should have 2 dimensions.")
    if matrix.shape[0] != 3:
        raise ValueError("Translation matrix  should have 3 rows.")
    if matrix.shape[1] != 1:
        raise ValueError("Translation matrix  should have 1 column.")
