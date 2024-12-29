# -*- coding: utf-8 -*-

""" Functions to load 3D Slicer's landmarks, saved as .json or .mrk.json """

import json
import numpy as np
import sksurgerycore.utilities.file_utilities as fu
import sksurgerycore.utilities.validate_file as f


def load_slicer_pointset(file_name):
    """
    Load a 3D Slicer's pointset file from .mrk.json or .json.

    :param file_name: string representing file path.
    :return: ids (length N), points (Nx3)
    """
    abs_file = fu.get_absolute_path_of_file(file_name)
    f.validate_is_file(abs_file)

    file_data = None
    with open(abs_file, "r", encoding='utf-8') as read_file:
        file_data = json.load(read_file)

    if file_data is None:
        raise IOError(f"Failed to read data from {abs_file}")

    ids = []
    points = []
    counter = 0
    list_of_markups = file_data["markups"]
    for markup in list_of_markups:
        control_points = markup['controlPoints']
        for control_point in control_points:
            point = control_point['position']
            ids.append(counter)
            points.append(point)
            print(f"Point id={counter}, position={point}")
            counter += 1
    result = np.array(points)
    ids = np.array(ids)
    return ids, result
