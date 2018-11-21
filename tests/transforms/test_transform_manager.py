#  -*- coding: utf-8 -*-

import numpy as np
import pytest
import sksurgerycore.transforms.transform_manager as m

test_manager_matrix_tolerance = 0.0001


def test_invalid_empty_transform():

    with pytest.raises(TypeError):
        m.TransformManager.is_valid_transform(None)


def test_invalid_wrong_rows():

    with pytest.raises(ValueError):
        m.TransformManager.is_valid_transform(np.ones((2, 4)))


def test_invalid_wrong_cols():

    with pytest.raises(ValueError):
        m.TransformManager.is_valid_transform(np.ones((4, 2)))


def test_invalid_name_none():

    with pytest.raises(TypeError):
        m.TransformManager.is_valid_name(None)


def test_invalid_name_integer():

    with pytest.raises(TypeError):
        m.TransformManager.is_valid_name(1)


def test_invalid_name_empty():

    # Empty string, is a string, so its
    # a ValueError rather than a TypeError
    with pytest.raises(ValueError):
        m.TransformManager.is_valid_name("")


def test_invalid_name_no_2():

    with pytest.raises(ValueError):
        m.TransformManager.is_valid_name("appletobanana")


def test_invalid_name_wrong_number():

    with pytest.raises(ValueError):
        m.TransformManager.is_valid_name("apple3banana")


def test_invalid_name_upper_case():

    with pytest.raises(ValueError):
        m.TransformManager.is_valid_name("Apple2Banna")


def test_invalid_name_too_many_parts():

    with pytest.raises(ValueError):
        m.TransformManager.is_valid_name("apple2banana2pear")


def test_invalid_name_implicit_identity():

    with pytest.raises(ValueError):
        m.TransformManager.is_valid_name("world2world")


def test_add_invalid_name():

    with pytest.raises(ValueError):
        tm = m.TransformManager()
        tm.add("banana", None)


def test_add_invalid_transform():

    with pytest.raises(TypeError):
        tm = m.TransformManager()
        tm.add("model2world", None)


def test_add_invalid_size():

    with pytest.raises(ValueError):
        tm = m.TransformManager()
        tm.add("model2world", np.eye(5))


def test_remove_invalid_name():

    with pytest.raises(ValueError):
        tm = m.TransformManager()
        tm.remove("banana")


def test_remove_non_existing_name():

    with pytest.raises(ValueError):
        tm = m.TransformManager()
        tm.remove("model2world")


def test_add_remove_valid():

    tm = m.TransformManager()
    tm.add("model2world", np.eye(4))
    tm.add("camera2world", np.eye(4))
    assert tm.exists("model2world")
    assert tm.exists("camera2world")
    assert tm.count() == 4  # as we also store inverse
    tm.remove("model2world")
    assert tm.count() == 2 # as we also store inverse

    tm.repository.pop("camera")  # Hack, as member vars aren't private.
    assert tm.count() == 1
    with pytest.raises(ValueError):
        tm.remove("camera2world")


def test_multiply_point():

    t = np.eye(4)
    t[0][3] = 1
    t[1][3] = 2
    t[2][3] = 3

    model_point = np.ones((4, 1))
    expected_world_point = np.ones((4, 1))
    expected_world_point[0][0] = 2
    expected_world_point[1][0] = 3
    expected_world_point[2][0] = 4
    expected_world_point[3][0] = 1

    tm = m.TransformManager()
    tm.add("model2world", t)

    with pytest.raises(ValueError):
        tm.multiply_point("a2b", model_point)

    world_point = tm.multiply_point("model2world", model_point)
    assert np.allclose(expected_world_point, world_point, test_manager_matrix_tolerance)


def test_get_exact_match():

    t = np.eye(4)
    tm = m.TransformManager()
    tm.add("model2world", t)
    r = tm.get("model2world")
    assert np.allclose(t, r, test_manager_matrix_tolerance)

    with pytest.raises(ValueError):
        r = tm.get("hand2eye")


def test_get_inverse_match():

    t = np.eye(4)
    t[0][3] = 1
    t[1][3] = 2
    t[2][3] = 3

    tm = m.TransformManager()
    tm.add("model2world", t)

    r = tm.get("world2model")
    assert np.allclose(t, np.linalg.inv(r), test_manager_matrix_tolerance)


def test_get_2_step_path():

    a2b = np.eye(4)
    a2b[0][3] = 1
    a2b[1][3] = 2
    a2b[2][3] = 3

    b2c = np.eye(4)
    b2c[0][3] = 1
    b2c[1][3] = 2
    b2c[2][3] = 3

    tm = m.TransformManager()
    tm.add("a2b", a2b)
    tm.add("b2c", b2c)

    r = tm.get("a2c")
    assert np.allclose(np.matmul(b2c, a2b), r, test_manager_matrix_tolerance)


def test_get_2_step_path_with_inverse():

    a2b = np.eye(4)
    a2b[0][3] = 1
    a2b[1][3] = 2
    a2b[2][3] = 3

    c2b = np.eye(4)
    c2b[0][3] = 1
    c2b[1][3] = 2
    c2b[2][3] = 3

    tm = m.TransformManager()
    tm.add("a2b", a2b)
    tm.add("c2b", c2b)

    r = tm.get("a2c")

    assert np.allclose(np.matmul(np.linalg.inv(c2b), a2b), r, test_manager_matrix_tolerance)


def create_test_matrix(seed):
    mat = np.eye(4)
    mat[0][3] = seed
    mat[1][3] = seed + 1
    mat[2][3] = seed + 2
    return mat


def test_get_path_with_diversions():

    a2b = create_test_matrix(1)
    b2c = create_test_matrix(2)
    c2d = create_test_matrix(3)
    b2e = create_test_matrix(4)
    e2f = create_test_matrix(5)
    b2g = create_test_matrix(6)

    tm = m.TransformManager()
    tm.add("a2b", a2b)
    tm.add("b2c", b2c)
    tm.add("c2d", c2d)
    tm.add("b2e", b2e)
    tm.add("e2f", e2f)
    tm.add("b2g", b2g)

    r = tm.get("a2f")

    assert np.allclose(
        np.matmul(e2f, np.matmul(b2e, a2b)), r, test_manager_matrix_tolerance)


def test_get_path_with_multiple_path():

    a2b = create_test_matrix(1)
    b2c = create_test_matrix(2)
    c2d = create_test_matrix(3)
    a2e = create_test_matrix(3)
    e2f = create_test_matrix(2)
    f2d = create_test_matrix(1)

    tm = m.TransformManager()
    tm.add("a2b", a2b)
    tm.add("b2c", b2c)
    tm.add("c2d", c2d)
    tm.add("a2e", a2e)
    tm.add("e2f", e2f)
    tm.add("f2d", f2d)

    r = tm.get("a2d")

    assert np.allclose(
        np.matmul(c2d, np.matmul(b2c, a2b)), r, test_manager_matrix_tolerance)


def test_get_path_with_y_shape():

    a2b = create_test_matrix(1)
    b2c = create_test_matrix(2)
    d2e = create_test_matrix(3)
    e2c = create_test_matrix(4)
    c2f = create_test_matrix(5)
    f2g = create_test_matrix(6)

    tm = m.TransformManager()
    tm.add("a2b", a2b)
    tm.add("b2c", b2c)
    tm.add("d2e", d2e)
    tm.add("e2c", e2c)
    tm.add("c2f", c2f)
    tm.add("f2g", f2g)

    r = tm.get("d2g")

    assert np.allclose(
        np.matmul(np.matmul(c2f, np.matmul(e2c, d2e)), f2g), r, test_manager_matrix_tolerance)

