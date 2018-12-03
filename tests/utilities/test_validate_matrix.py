# coding=utf-8

"""
Tests for validate_matrix.py
"""

import pytest
import numpy as np
import sksurgerycore.utilities.validate_matrix as vm


def test_camera_matrix_invalid_because_wrong_type():
    with pytest.raises(TypeError):
        vm.validate_camera_matrix(1)


def test_camera_matrix_invalid_because_not_two_dimensional():
    with pytest.raises(ValueError):
        vm.validate_camera_matrix(np.ones((3, 3, 3)))


def test_camera_matrix_invalid_because_too_few_rows():
    with pytest.raises(ValueError):
        vm.validate_camera_matrix(np.ones((1, 3)))


def test_camera_matrix_invalid_because_too_many_rows():
    with pytest.raises(ValueError):
        vm.validate_camera_matrix(np.ones((4, 3)))


def test_camera_matrix_invalid_because_too_few_columns():
    with pytest.raises(ValueError):
        vm.validate_camera_matrix(np.ones((3, 1)))


def test_camera_matrix_invalid_because_too_many_columns():
    with pytest.raises(ValueError):
        vm.validate_camera_matrix(np.ones((3, 4)))


def test_distortion_coefficients_invalid_because_wrong_type():
    with pytest.raises(TypeError):
        vm.validate_distortion_coefficients(1)


def test_distortion_coefficients_invalid_because_not_two_dimensional():
    with pytest.raises(ValueError):
        vm.validate_distortion_coefficients(np.ones((3, 3, 3)))


def test_distortion_coefficients_invalid_because_too_many_rows():
    with pytest.raises(ValueError):
        vm.validate_distortion_coefficients(np.ones((3, 4)))


def test_distortion_coefficients_invalid_because_too_few_columns():
    with pytest.raises(ValueError):
        vm.validate_distortion_coefficients(np.ones((1, 3)))


def test_distortion_coefficients_invalid_because_number_of_columns_not_in_list():
    with pytest.raises(ValueError):
        # Should accept [4, 5, 8, 12, 14]
        vm.validate_distortion_coefficients(np.ones((1, 6)))


def test_rotation_matrix_invalid_because_wrong_type():
    with pytest.raises(TypeError):
        vm.validate_rotation_matrix(1)


def test_rotation_matrix_invalid_because_not_two_dimensional():
    with pytest.raises(ValueError):
        vm.validate_rotation_matrix(np.ones((3, 3, 3)))


def test_rotation_matrix_invalid_because_too_many_rows():
    with pytest.raises(ValueError):
        vm.validate_rotation_matrix(np.ones((4, 3)))


def test_rotation_matrix_invalid_because_too_many_columns():
    with pytest.raises(ValueError):
        vm.validate_rotation_matrix(np.ones((3, 4)))


def test_rotation_matrix_invalid_because_too_few_rows():
    with pytest.raises(ValueError):
        vm.validate_rotation_matrix(np.ones((2, 3)))


def test_rotation_matrix_invalid_because_too_few_columns():
    with pytest.raises(ValueError):
        vm.validate_rotation_matrix(np.ones((3, 2)))


def test_translation_matrix_invalid_because_wrong_type():
    with pytest.raises(TypeError):
        vm.validate_translation_column_vector(1)


def test_translation_matrix_invalid_because_not_two_dimensional():
    with pytest.raises(ValueError):
        vm.validate_translation_column_vector(np.ones((3, 3, 3)))


def test_translation_matrix_invalid_because_too_many_rows():
    with pytest.raises(ValueError):
        vm.validate_translation_column_vector(np.ones((4, 1)))


def test_translation_matrix_invalid_because_too_many_columns():
    with pytest.raises(ValueError):
        vm.validate_translation_column_vector(np.ones((3, 4)))


def test_translation_matrix_invalid_because_too_few_rows():
    with pytest.raises(ValueError):
        vm.validate_translation_column_vector(np.ones((2, 1)))
