#  -*- coding: utf-8 -*-

# pylint: skip-file

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

    assert np.allclose(rotation, expected_rotation, 0.0000001)
    assert np.allclose(translation, np.zeros((3, 1)), 0.0000001)
    assert error < 0.0000001

def test_reflection_BARD_data():
    """This is a reflection test using data taken from using
    BARD at the 2019 summer school. This data set will give
    you reflections, unless you replace equation 13 from Arun 
    with Fitzpatrick's modification. This was done at issue #19"""
    ct_fids = np.zeros((4,3))
    world_fids = np.zeros((4,3))

    ct_fids[0][0] = 37.82
    ct_fids[0][1] = 52.99
    ct_fids[0][2] = -191.00
    ct_fids[1][0] = 310.90
    ct_fids[1][1] = 70.36
    ct_fids[1][2] = -196.50
    ct_fids[2][0] = 171.98
    ct_fids[2][1] = 57.59
    ct_fids[2][2] = -376.96
    ct_fids[3][0] = 176.56
    ct_fids[3][1] = 71.30
    ct_fids[3][2] = -7.42

    world_fids[0][0] = -7.060625292517708829e+01
    world_fids[0][1] = -4.340731346419998715e+01
    world_fids[0][2] = -7.678145283688323275e+01
    world_fids[1][0] = -8.290290497289761618e+01
    world_fids[1][1] = 2.365685716505672360e+02
    world_fids[1][2] = -6.248063455571644909e+01
    world_fids[2][0] = 1.061984137321565527e+02
    world_fids[2][1] = 1.054365783777915624e+02
    world_fids[2][2] = -6.347752061138085367e+01
    world_fids[3][0] = -2.658595567434794020e+02
    world_fids[3][1] = 9.556619277927123335e+01
    world_fids[3][2] = -7.335614476329364209e+01

    rotation, translation, error = p.orthogonal_procrustes(world_fids, ct_fids)
    expected_rotation = np.eye(3)
    expected_rotation[0][0] = -0.04933494
    expected_rotation[0][1] = -0.01438556
    expected_rotation[0][2] = -0.99867869
    expected_rotation[1][0] = 0.99212873
    expected_rotation[1][1] = 0.11451658
    expected_rotation[1][2] = -0.05066094
    expected_rotation[2][0] = 0.11509405
    expected_rotation[2][1] = -0.99331717
    expected_rotation[2][2] = 0.00862266
    assert np.allclose(rotation, expected_rotation, 0.0000001)


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
