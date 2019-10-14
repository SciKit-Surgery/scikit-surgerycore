#  -*- coding: utf-8 -*-

"""Class implementing a general purpose 4x4 transformation matrix manager."""

import re
import numpy as np


class TransformManager:
    """
    Class for managing 4x4 transformation matrices.
    This class is NOT designed to be thread-safe.


    The transforms are required to be 4x4 matrices.
    There is no checking that the upper left 3x3 is
    an orthonormal rotation matrix.

    Usage::

        tm = TransformManager()

        # Imagine some example transformations:
        t1 = np.eye(4)
        t2 = np.eye(4)
        t3 = np.eye(4)

        # Add transformations to the TransformManager.
        tm.add("model2world", t1)
        tm.add("hand2eye",t2)
        tm.add("hand2world",t3)

        # Returns a transform from model to eye,
        # by working through the above transforms.
        t4 = tm.get("model2eye")

    and so on.

    """
    def __init__(self):
        """
        Initialises an empty repository,
        which will be a dictionary of dictionaries.
        """
        self.repository = {}

    @staticmethod
    def is_valid_transform(transform):
        """
        Validates the transform as a 4x4 numpy matrix.

        :param transform: 4x4 transformation matrix.
        :raises: TypeError, ValueError
        """
        if not isinstance(transform, np.ndarray):
            raise TypeError("transform is not a 2D numpy array")

        if transform.shape[0] != 4:
            raise ValueError("transform does not have 4 rows")

        if transform.shape[1] != 4:
            raise ValueError("transform does not have 4 columns")

    @staticmethod
    def is_valid_name(name):
        """
        Validates the name, which must match "^([a-z]+)2([a-z]+)$".

        i.e. one or more lowercase letters, followed by the number
        2, followed by one or more lowercase letters.

        For example::

            a2b
            model2world

        Identity transforms such as model2model raise ValueError.

        :param name: the name of the transform, eg. model2world
        :raises: TypeError, ValueError
        :returns: str, str -- parts of string before and after the 2.
        """
        if not isinstance(name, str):
            raise TypeError("name is not a string")

        if not re.match("^([a-z]+)2([a-z]+)$", name):
            raise ValueError("name is incorrectly formatted")

        pre, post = name.split("2")

        if pre == post:
            raise ValueError("you shouldn't request the identity:"
                             + pre + "2" + post)

        return pre, post

    @staticmethod
    def flip_name(name):
        """
        Returns the inverse name.

        :param name: the name of a transformation, e.g. model2world
        :returns: str -- the opposite transformation name, e.g. world2model
        """
        before, after = TransformManager.is_valid_name(name)
        return after + "2" + before

    def exists(self, name):
        """
        Returns True if the transform exists in the manager,
        and False otherwise. Internally this class stores
        the inverse. So, if you add model2world, you are
        also implicitly adding world2model, so this
        method will return True for both the originally
        added transform, and its own inverse.
        """
        before, after = self.is_valid_name(name)
        return after in self.repository.keys() \
            and before in self.repository[after].keys()

    def count(self):
        """
        Returns how many transforms are in the manager.
        Internally this class also stores the inverse,
        so this method will count those matrices as well.
        """
        count = 0
        for i in self.repository:
            count += len(self.repository[i])
        return count

    def add(self, name, transform):
        """
        Adds a transform called name.
        If the name already exists, the corresponding
        transform is replaced without warning.

        :param name: the name of the transform, e.g. model2world
        :param transform: the transform, e.g. 4x4 matrix
        """
        before, after = self.is_valid_name(name)
        self.is_valid_transform(transform)
        if after not in self.repository.keys():
            self.repository[after] = {}
        if before not in self.repository.keys():
            self.repository[before] = {}
        self.repository[before][after] = transform
        self.repository[after][before] = np.linalg.inv(transform)

    def remove(self, name):
        """
        Removes a transform from the manager.
        If the transform name doesn't exist, will throw ValueError.

        :raises: ValueError
        """
        before, after = self.is_valid_name(name)
        flipped = TransformManager.flip_name(name)

        if not self.exists(name):
            raise ValueError("name:" + name + ", is not in repository.")
        if not self.exists(flipped):
            raise ValueError("name:" + flipped + ", is not in repository.")
        self.repository[before].pop(after)
        self.repository[after].pop(before)

    def multiply_point(self, name, points):
        """
        Multiplies points (4xN) by the named transform (4x4).

        :returns: ndarray -- 4xN matrix of transformed points
        :raises: ValueError
        """
        if not self.exists(name):
            raise ValueError("name:" + name + ", could not be found.")

        transform = self.get(name)

        return np.matmul(transform, points)

    def get(self, name):
        """
        Returns the named transform or throws ValueError.

        :raises: ValueError
        """
        before, after = self.is_valid_name(name)

        if before not in self.repository.keys() \
                or after not in self.repository.keys():
            raise ValueError("name:" + name + ", could not be found.")

        result = self.__get_direct(name)

        if result is not None:
            return result

        # If we didn't find it first time,
        # search for a list of nodes from after to before.
        list_of_nodes = [before]
        self.__get_list(before, after, list_of_nodes)

        # Multiply the nodes together. __get_list returns them
        # in order (from before to after),
        # so in the example model2world, model=before
        # world=after, so the ordering returned from __get_list
        # is from model to world. This is so we can simply
        # pre-multiply them in the same order you normally
        # do matrix multiplication.
        result = np.eye(4)
        for node_index in range(0, len(list_of_nodes) - 1):
            next_name = list_of_nodes[node_index] \
                        + "2" + list_of_nodes[node_index+1]
            transform = self.get(next_name)
            result = np.matmul(transform, result)
        return result

    def __get_direct(self, name):
        """
        Internal method to return the named transform or None.
        """
        before, after = self.is_valid_name(name)
        if self.exists(name):
            return self.repository[before][after]
        return None

    def __get_list(self, before, after, list_of_nodes):
        """
        Internal method to work out a list of transforms
        equivalent to the transform referred to by name.
        """
        candidates = self.repository[before]

        if after in candidates:
            list_of_nodes.append(after)
            return

        for candidate in candidates:

            if candidate in list_of_nodes:
                continue

            list_of_nodes.append(candidate)
            self.__get_list(candidate, after, list_of_nodes)

            if list_of_nodes[-1] == after:
                break

            list_of_nodes.pop()
