#  -*- coding: utf-8 -*-

"""Functions for point based registration using Orthogonal Procrustes."""

import numpy as np
from sksurgerycore.algorithms.errors \
    import validate_procrustes_inputs, compute_fre

# pylint: disable=invalid-name, line-too-long


def orthogonal_procrustes(fixed, moving):
    """
    Implements point based registration via the Orthogonal Procrustes method.

    Based on Arun's method:

      Least-Squares Fitting of two, 3-D Point Sets, Arun, 1987,
      `10.1109/TPAMI.1987.4767965 <http://dx.doi.org/10.1109/TPAMI.1987.4767965>`_.

    Also see `this <http://eecs.vanderbilt.edu/people/mikefitzpatrick/papers/2009_Medim_Fitzpatrick_TRE_FRE_uncorrelated_as_published.pdf>`_
    and `this <http://tango.andrew.cmu.edu/~gustavor/42431-intro-bioimaging/readings/ch8.pdf>`_.

    :param fixed: point set, N x 3 ndarray
    :param moving: point set, N x 3 ndarray of corresponding points
    :returns: 3x3 rotation ndarray, 3x1 translation ndarray, FRE
    :raises: ValueError
    """

    validate_procrustes_inputs(fixed, moving)

    # This is what we are calculating
    R = np.eye(3)
    T = np.zeros((3, 1))

    # Arun equation 4
    p = np.ndarray.mean(moving, 0)

    # Arun equation 6
    p_prime = np.ndarray.mean(fixed, 0)

    # Arun equation 7
    q = moving - p

    # Arun equation 8
    q_prime = fixed - p_prime

    # Arun equation 11
    H = np.matmul(q.transpose(), q_prime)

    # Arun equation 12
    # Note: numpy factors h = u * np.diag(s) * v
    svd = np.linalg.svd(H)

    # Replace Arun Equation 13 with Fitzpatrick, chapter 8, page 470,
    # to avoid reflections, see issue #19
    X = _fitzpatricks_X(svd)

    # Arun step 5, after equation 13.
    det_X = np.linalg.det(X)

    if det_X < 0 and np.all(np.flip(np.isclose(svd[1], np.zeros((3, 1))))):

        # Don't yet know how to generate test data.
        # If you hit this line, please report it, and save your data.
        raise ValueError("Registration fails as determinant < 0"
                         " and no singular values are close enough to zero")

    if det_X < 0 and np.any(np.isclose(svd[1], np.zeros((3, 1)))):
        # Implement 2a in section VI in Arun paper.
        v_prime = svd[2].transpose()
        v_prime[0][2] *= -1
        v_prime[1][2] *= -1
        v_prime[2][2] *= -1
        X = np.matmul(v_prime, svd[0].transpose())


    # Compute output
    R = X
    tmp = p_prime.transpose() - np.matmul(R, p.transpose())
    T[0][0] = tmp[0]
    T[1][0] = tmp[1]
    T[2][0] = tmp[2]
    fre = compute_fre(fixed, moving, R, T)

    return R, T, fre

def _fitzpatricks_X(svd):
    """This is from Fitzpatrick, chapter 8, page 470.
       it's used in preference to Arun's equation 13,
       X = np.matmul(svd[2].transpose(), svd[0].transpose())
       to avoid reflections.
    """
    VU = np.matmul(svd[2].transpose(), svd[0])
    detVU = np.linalg.det(VU)

    diag = np.eye(3, 3)
    diag[2][2] = detVU

    X = np.matmul(svd[2].transpose(), np.matmul(diag, svd[0].transpose()))
    return X
