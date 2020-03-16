# -*- coding: utf-8 -*-

""" Various small maths utilities. """

import numpy as np


def distance_from_line(p_1, p_2, p_3):
    """
    Computes distance of a point p_3, from a line defined by p_1 and p_2.

    See `here <https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line>`_.

    :return: euclidean distance
    """
    # I want notation same as wikipedia page, so disabling warning.
    # pylint: disable=invalid-name
    n = p_2 - p_1
    n = n / np.linalg.norm(n)
    a_minus_p = p_1 - p_3
    vector_to_line = a_minus_p - (np.dot(a_minus_p, n) * n)
    distance = np.linalg.norm(vector_to_line)
    return distance
