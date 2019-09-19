#  -*- coding: utf-8 -*-

import six
import numpy as np
import pytest
import sksurgerycore.algorithms.procrustes as p


def test_empty_fixed():

    with pytest.raises(TypeError):
        p.orthogonal_procrustes(None, np.ones((1, 3)))


def test_empty_moving():

    with pytest.raises(TypeError):
        p.orthogonal_procrustes(np.ones((1, 3)), None)


def test_three_columns_fixed():

    with pytest.raises(ValueError):
        p.orthogonal_procrustes(np.ones((3, 4)), np.ones((3, 3)))


def test_three_columns_moving():

    with pytest.raises(ValueError):
        p.orthogonal_procrustes(np.ones((3, 3)), np.ones((3, 4)))


def test_at_least_three_points_fixed():

    with pytest.raises(ValueError):
        p.orthogonal_procrustes(np.ones((1, 3)), np.ones((3, 3)))


def test_at_least_three_points_moving():

    with pytest.raises(ValueError):
        p.orthogonal_procrustes(np.ones((3, 3)), np.ones((1, 3)))


def test_same_number_points():

    with pytest.raises(ValueError):
        p.orthogonal_procrustes(np.ones((4, 3)), np.ones((5, 3)))


def test_identity_result():

    fixed = np.zeros((3, 3))
    fixed[0][1] = 1
    fixed[2][0] = 2

    moving = np.zeros((3, 3))
    moving[0][1] = 1
    moving[2][0] = 2

    rotation, translation, error = p.orthogonal_procrustes(fixed, moving)
    assert np.allclose(rotation, np.eye(3), 0.0000001)
    assert np.allclose(translation, np.zeros((3, 1)), 0.0000001)
    assert error < 0.0000001


def test_reflection_data():
    """This seems to be testing that a rotation
    is prefered to a reflection. To transform these
    points you can either reflect through yz, or
    rotate 180 about y"""
    fixed = np.zeros((4, 3))
    fixed[0][1] = 1
    fixed[2][0] = 2
    fixed[3][0] = 4

    moving = np.zeros((4, 3))
    moving[0][1] = 1
    moving[2][0] = -2
    moving[3][0] = -4

    rotation, translation, error = p.orthogonal_procrustes(fixed, moving)
    expected_rotation = np.eye(3)
    expected_rotation[0][0] = -1
    expected_rotation[2][2] = -1
    print (np.linalg.det(rotation))
    print (rotation)
    assert False

    assert np.allclose(rotation, expected_rotation, 0.0000001)
    assert np.allclose(translation, np.zeros((3, 1)), 0.0000001)
    assert error < 0.0000001


def test_translation_result():

    fixed = np.zeros((3, 3))
    fixed[0][1] = 1
    fixed[2][0] = 2

    moving = np.zeros((3, 3))
    moving[0][1] = 1
    moving[2][0] = 2
    moving[0][2] += 1
    moving[1][2] += 1
    moving[2][2] += 1

    expected_translation = np.zeros((3, 1))
    expected_translation[2][0] = -1

    rotation, translation, error = p.orthogonal_procrustes(fixed, moving)
    assert np.allclose(rotation, np.eye(3), 0.0000001)
    assert np.allclose(translation, expected_translation, 0.0000001)
    assert error < 0.0000001


def test_rotation_result():

    fixed = np.zeros((5, 3))
    fixed[0][0] = 39.3047
    fixed[0][1] = 71.7057
    fixed[0][2] = 372.72
    fixed[1][0] = 171.844
    fixed[1][1] = 65.8063
    fixed[1][2] = 376.325
    fixed[2][0] = 312.044
    fixed[2][1] = 77.5614
    fixed[2][2] = 196
    fixed[3][0] = 176.528
    fixed[3][1] = 78.7922
    fixed[3][2] = 8
    fixed[4][0] = 43.4659
    fixed[4][1] = 53.2688
    fixed[4][2] = 10.5

    moving = np.zeros((5, 3))
    moving[0][0] = 192.833
    moving[0][1] = 290.286
    moving[0][2] = 155.423
    moving[1][0] = 295.688
    moving[1][1] = 287.97
    moving[1][2] = 71.5776
    moving[2][0] = 301.155
    moving[2][1] = 183.623
    moving[2][2] = -131.876
    moving[3][0] = 102.167
    moving[3][1] = 66.2676
    moving[3][2] = -150.349
    moving[4][0] = 15.3302
    moving[4][1] = 48.0055
    moving[4][2] = -47.9328

    expected_translation = np.zeros((3, 1))
    expected_rotation = np.zeros((3, 3))
    expected_rotation[0][0] = 0.7431
    expected_rotation[0][1] = 0
    expected_rotation[0][2] = -0.6691
    expected_rotation[1][0] = -0.4211
    expected_rotation[1][1] = 0.7771
    expected_rotation[1][2] = -0.4677
    expected_rotation[2][0] = 0.52
    expected_rotation[2][1] = 0.6293
    expected_rotation[2][2] = 0.5775

    rotation, translation, error = p.orthogonal_procrustes(fixed, moving)
    assert np.allclose(expected_translation, translation, 0.001, 0.001)
    assert np.allclose(expected_rotation, rotation, 0.001, 0.001)
    assert error < 0.001
