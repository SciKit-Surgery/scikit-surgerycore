# -*- coding: utf-8 -*-

"""Functions to load MITK's mps point set file. """

import xml.etree.ElementTree as ET
import numpy as np


def load_mps(file_name):
    """
    Load a pointset from a .mps file. For now, just loads points,
    without geometry information.

    :param file_name: string representing file path.
    :return: ids (length N), points (Nx3)
    """
    tree = ET.parse(file_name)
    root = tree.getroot()
    points = root[1]
    time_series = points[0]
    tmp = {}
    for point in time_series.findall('point'):
        i = point.find('id').text
        x_c = point.find('x').text
        y_c = point.find('y').text
        z_c = point.find('z').text
        tmp[int(i)] = (float(x_c), float(y_c), float(z_c))
    ids = np.zeros(len(tmp.keys()), dtype=int)
    result = np.zeros((len(tmp.keys()), 3))
    counter = 0
    for k in tmp:
        ids[counter] = k
        result[counter][0] = tmp[k][0]
        result[counter][1] = tmp[k][1]
        result[counter][2] = tmp[k][2]
        counter = counter + 1
    return ids, result
