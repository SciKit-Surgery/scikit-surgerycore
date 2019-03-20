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
    :raises: TypeError, ValueError if not
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
    :raises: TypeError, ValueError if not
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
        5. Is orthogonal, i.e., transpose(matrix) * matrix = identity matrix.
        6. Is its determinant positive (+1) (c.f., it is a reflection matrix
           (improper rotation) if the determinant is negative (-1))

    :param matrix: rotation matrix
    :raises: TypeError, ValueError if not
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

    # Check the orthogonality: transpose(matrix) * matrix = identity matrix.
    mat = np.matmul(np.transpose(matrix), matrix)
    tolerance = 2e-6
    identity = np.eye(3)
    residual = np.absolute(mat) - identity
    if np.flatnonzero(np.where(
            (residual < -tolerance) | (residual > tolerance))).shape[0] > 0:
        raise ValueError("Rotation matrix should be orthogonal.")

    # Check if the determinant is positive
    # (assuming that the absolute value of the determinant is (close to) 1,
    # which is followed by the orthogonality).
    if np.linalg.det(matrix) < 0.0:
        raise ValueError(
            "Rotation matrix should have a positive determinant (+1).")

    return True


# pylint: disable=invalid-name
def validate_translation_column_vector(matrix):
    """
    Validates that a translation matrix is a column vector.

        1. Is numpy array
        2. Is 2D
        3. Has 3 rows
        4. Has 1 column

    :param matrix: translation matrix
    :raises: TypeError, ValueError if not
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
    return True


def validate_rigid_matrix(matrix):
    """
    Validates that a matrix is a 4x4 rigid transform.

    :param matrix: rigid transform
    :raises: TypeError, ValueError if not
    :return: True
    """
    if not isinstance(matrix, np.ndarray):
        raise TypeError('Rigid matrix is not an np.ndarray')
    if len(matrix.shape) != 2:
        raise ValueError("Rigid matrix  should have 2 dimensions.")
    if matrix.shape[0] != 4:
        raise ValueError("Rigid matrix  should have 4 rows.")
    if matrix.shape[1] != 4:
        raise ValueError("Rigid matrix  should have 4 columns.")
    validate_rotation_matrix(matrix[0:3, 0:3])
