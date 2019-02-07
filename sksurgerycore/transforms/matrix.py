import numpy as np

def construct_rx_matrix(x):
    """Construct a rotation matrix for rotation around the x axis"""
    cx = np.cos(x)
    sx = np.sin(x)

    rot_x = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])

    return rot_x

def construct_ry_matrix(y):
    """Construct a rotation matrix for rotation around the y axis"""
    cy = np.cos(y)
    sy = np.sin(y)

    rot_y = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])

    return rot_y

def construct_rz_matrix(z):
    """Construct a rotation matrix for rotation around the z axis"""
    cz = np.cos(z)
    sz = np.sin(z)

    rot_z = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])

    return rot_z
