"""
Tests for matrix.py
"""

import pytest
import numpy as np

import sksurgerycore.transforms.matrix as mat
import sksurgerycore.utilities.validate_matrix as vm


def check_construct_rx_matrix(angle, is_in_radians, point):
    """"
    Check if the rotation matrix for rotating around the x axis is correct.

    :param angle: the angle to rotate
    :param is_in_radians: if angle is in radians or not
    :param point: the point to be rotated
    :returns: new_point -- the point after rotation
    """
    rot_x = mat.construct_rx_matrix(angle, is_in_radians)
    vm.validate_rotation_matrix(rot_x)

    new_point = np.matmul(rot_x, point)
    assert new_point[0] == point[0]
    assert np.abs(np.linalg.norm(new_point) - np.linalg.norm(point)) <= 0.0001

    return new_point


def check_construct_ry_matrix(angle, is_in_radians, point):
    """"
    Check if the rotation matrix for rotating around the y axis is correct.

    :param angle: the angle to rotate
    :param is_in_radians: if angle is in radians or not
    :param point: the point to be rotated
    :returns: new_point -- the point after rotation
    """
    rot_y = mat.construct_ry_matrix(angle, is_in_radians)
    vm.validate_rotation_matrix(rot_y)

    new_point = np.matmul(rot_y, point)
    assert new_point[1] == point[1]
    assert np.abs(np.linalg.norm(new_point) - np.linalg.norm(point)) <= 0.0001

    return new_point


def check_construct_rz_matrix(angle, is_in_radians, point):
    """"
    Check if the rotation matrix for rotating around the z axis is correct.

    :param angle: the angle to rotate
    :param is_in_radians: if angle is in radians or not
    :param point: the point to be rotated
    :returns: new_point -- the point after rotation
    """
    rot_z = mat.construct_rz_matrix(angle, is_in_radians)
    vm.validate_rotation_matrix(rot_z)

    new_point = np.matmul(rot_z, point)
    assert new_point[2] == point[2]
    assert np.abs(np.linalg.norm(new_point) - np.linalg.norm(point)) <= 0.0001

    return new_point


def test_construct_rx_matrix():
    tiny = 0.0001

    new_point = check_construct_rx_matrix(90, 0, np.array([0, 1, 0]).T)
    assert np.abs(new_point[0]) <= tiny
    assert np.abs(new_point[1]) <= tiny
    assert np.abs(new_point[2] - 1) <= tiny

    new_point = check_construct_rx_matrix(np.pi/2, 1, np.array([0, 1, 0]).T)
    assert np.abs(new_point[0]) <= tiny
    assert np.abs(new_point[1]) <= tiny
    assert np.abs(new_point[2] - 1) <= tiny

    new_point = check_construct_rx_matrix(-90, 0, np.array([0, 1, 0]).T)
    assert np.abs(new_point[0]) <= tiny
    assert np.abs(new_point[1]) <= tiny
    assert np.abs(new_point[2] + 1) <= tiny

    new_point = check_construct_rx_matrix(-np.pi/2, 1, np.array([0, 1, 0]).T)
    assert np.abs(new_point[0]) <= tiny
    assert np.abs(new_point[1]) <= tiny
    assert np.abs(new_point[2] + 1) <= tiny

    new_point = check_construct_rx_matrix(180, 0, np.array([0, 1, 0]).T)
    assert np.abs(new_point[0]) <= tiny
    assert np.abs(new_point[1] + 1) <= tiny
    assert np.abs(new_point[2]) <= tiny

    new_point = check_construct_rx_matrix(np.pi, 1, np.array([0, 1, 0]).T)
    assert np.abs(new_point[0]) <= tiny
    assert np.abs(new_point[1] + 1) <= tiny
    assert np.abs(new_point[2]) <= tiny

    new_point = check_construct_rx_matrix(-180, 0, np.array([0, 1, 0]).T)
    assert np.abs(new_point[0]) <= tiny
    assert np.abs(new_point[1] + 1) <= tiny
    assert np.abs(new_point[2]) <= tiny

    new_point = check_construct_rx_matrix(-np.pi, 1, np.array([0, 1, 0]).T)
    assert np.abs(new_point[0]) <= tiny
    assert np.abs(new_point[1] + 1) <= tiny
    assert np.abs(new_point[2]) <= tiny


def test_construct_ry_matrix():
    tiny = 0.0001

    new_point = check_construct_ry_matrix(90, 0, np.array([1, 0, 0]).T)
    assert np.abs(new_point[0]) <= tiny
    assert np.abs(new_point[1]) <= tiny
    assert np.abs(new_point[2] + 1) <= tiny

    new_point = check_construct_ry_matrix(np.pi/2, 1, np.array([1, 0, 0]).T)
    assert np.abs(new_point[0]) <= tiny
    assert np.abs(new_point[1]) <= tiny
    assert np.abs(new_point[2] + 1) <= tiny

    new_point = check_construct_ry_matrix(-90, 0, np.array([1, 0, 0]).T)
    assert np.abs(new_point[0]) <= tiny
    assert np.abs(new_point[1]) <= tiny
    assert np.abs(new_point[2] - 1) <= tiny

    new_point = check_construct_ry_matrix(-np.pi/2, 1, np.array([1, 0, 0]).T)
    assert np.abs(new_point[0]) <= tiny
    assert np.abs(new_point[1]) <= tiny
    assert np.abs(new_point[2] - 1) <= tiny

    new_point = check_construct_ry_matrix(180, 0, np.array([1, 0, 0]).T)
    assert np.abs(new_point[0] + 1) <= tiny
    assert np.abs(new_point[1]) <= tiny
    assert np.abs(new_point[2]) <= tiny

    new_point = check_construct_ry_matrix(np.pi, 1, np.array([1, 0, 0]).T)
    assert np.abs(new_point[0] + 1) <= tiny
    assert np.abs(new_point[1]) <= tiny
    assert np.abs(new_point[2]) <= tiny

    new_point = check_construct_ry_matrix(-180, 0, np.array([1, 0, 0]).T)
    assert np.abs(new_point[0] + 1) <= tiny
    assert np.abs(new_point[1]) <= tiny
    assert np.abs(new_point[2]) <= tiny

    new_point = check_construct_ry_matrix(-np.pi, 1, np.array([1, 0, 0]).T)
    assert np.abs(new_point[0] + 1) <= tiny
    assert np.abs(new_point[1]) <= tiny
    assert np.abs(new_point[2]) <= tiny


def test_construct_rz_matrix():
    tiny = 0.0001

    new_point = check_construct_rz_matrix(90, 0, np.array([1, 0, 0]).T)
    assert np.abs(new_point[0]) <= tiny
    assert np.abs(new_point[1] - 1) <= tiny
    assert np.abs(new_point[2]) <= tiny

    new_point = check_construct_rz_matrix(np.pi/2, 1, np.array([1, 0, 0]).T)
    assert np.abs(new_point[0]) <= tiny
    assert np.abs(new_point[1] - 1) <= tiny
    assert np.abs(new_point[2]) <= tiny

    new_point = check_construct_rz_matrix(-90, 0, np.array([1, 0, 0]).T)
    assert np.abs(new_point[0]) <= tiny
    assert np.abs(new_point[1] + 1) <= tiny
    assert np.abs(new_point[2]) <= tiny

    new_point = check_construct_rz_matrix(-np.pi/2, 1, np.array([1, 0, 0]).T)
    assert np.abs(new_point[0]) <= tiny
    assert np.abs(new_point[1] + 1) <= tiny
    assert np.abs(new_point[2]) <= tiny

    new_point = check_construct_rz_matrix(180, 0, np.array([1, 0, 0]).T)
    assert np.abs(new_point[0] + 1) <= tiny
    assert np.abs(new_point[1]) <= tiny
    assert np.abs(new_point[2]) <= tiny

    new_point = check_construct_rz_matrix(np.pi, 1, np.array([1, 0, 0]).T)
    assert np.abs(new_point[0] + 1) <= tiny
    assert np.abs(new_point[1]) <= tiny
    assert np.abs(new_point[2]) <= tiny

    new_point = check_construct_rz_matrix(-180, 0, np.array([1, 0, 0]).T)
    assert np.abs(new_point[0] + 1) <= tiny
    assert np.abs(new_point[1]) <= tiny
    assert np.abs(new_point[2]) <= tiny

    new_point = check_construct_rz_matrix(-np.pi, 1, np.array([1, 0, 0]).T)
    assert np.abs(new_point[0] + 1) <= tiny
    assert np.abs(new_point[1]) <= tiny
    assert np.abs(new_point[2]) <= tiny


def check_construct_rotm_from_euler(
        angle_a, angle_b, angle_c,
        sequence, is_in_radians,
        point):
    """"
    Check if the rotation matrix for rotating around the x axis is correct.

    :param angle_a: first Euler angle
    :param angle_b: second Euler angle
    :param angle_c: third Euler angle
    :param is_in_radians: if angle is in radians or not
    :param point: the point to be rotated
    :returns: new_point -- the point after rotation
    """
    rot_m = mat.construct_rotm_from_euler(
        angle_a, angle_b, angle_c,
        sequence, is_in_radians)
    vm.validate_rotation_matrix(rot_m)

    new_point = np.matmul(rot_m, point)
    assert np.abs(np.linalg.norm(new_point) - np.linalg.norm(point)) <= 0.0001

    return new_point


def test_construct_rotm_from_euler():
    tiny = 0.0001

    new_point = check_construct_rotm_from_euler(
        90, -90, 0,
        'zyz', 0,
        np.array([0, -1, -1]).T)
    assert np.abs(new_point[0] - 1) <= tiny
    assert np.abs(new_point[1] - 1) <= tiny
    assert np.abs(new_point[2]) <= tiny

    new_point = check_construct_rotm_from_euler(
        np.pi/2, -np.pi/2, 0,
        'zyz', 1,
        np.array([0, -1, -1]).T)
    assert np.abs(new_point[0] - 1) <= tiny
    assert np.abs(new_point[1] - 1) <= tiny
    assert np.abs(new_point[2]) <= tiny

    new_point = check_construct_rotm_from_euler(
        90, -90, 0,
        'zxz', 0,
        np.array([1, 0, -1]).T)
    assert np.abs(new_point[0] - 1) <= tiny
    assert np.abs(new_point[1] - 1) <= tiny
    assert np.abs(new_point[2]) <= tiny

    new_point = check_construct_rotm_from_euler(
        0, 90, -90,
        'zyx', 0,
        np.array([0, -1, 1]).T)
    assert np.abs(new_point[0] - 1) <= tiny
    assert np.abs(new_point[1] - 1) <= tiny
    assert np.abs(new_point[2]) <= tiny

    new_point = check_construct_rotm_from_euler(
        0, 90, -90,
        'xyz', 0,
        np.array([-1, 0, 1]).T)
    assert np.abs(new_point[0] - 1) <= tiny
    assert np.abs(new_point[1] - 1) <= tiny
    assert np.abs(new_point[2]) <= tiny


test_construct_rotm_from_euler()
