"""
Tests for skcore baseclasses
"""
import math
import pytest
import numpy as np

from sksurgerycore.transforms.matrix import construct_rx_matrix, \
                construct_rigid_transformation
from sksurgerycore.algorithms.tracking_smoothing import _rvec_to_quaternion
from sksurgerycore.baseclasses.tracker import SKSBaseTracker

class GoodTracker(SKSBaseTracker):
    # pylint: disable=useless-super-delegation, missing-function-docstring
    """
    A tracker class with the necessary member functions.
    """
    def __init__(self, configuration = None, tracked_objects = None):
        super().__init__(configuration, tracked_objects)
    def close(self):
        super().close()
    def get_frame(self):
        super().get_frame()
    def get_tool_descriptions(self):
        super().get_tool_descriptions()
    def start_tracking(self):
        super().start_tracking()
    def stop_tracking(self):
        super().stop_tracking()

class BadTracker(SKSBaseTracker):# pylint: disable=abstract-method
    """
    A tracker class without the necessary member functions.
    """
    def close(self):
        pass


class RigidBody():
    """
    A dummy rigid body class for testing SKSBaseTracker
    """
    def __init__(self, name):
        self.name = name

def test_tracker_baseclass():
    """
    We should throw not implemented error when we make a tracker without
    the required functions.
    """
    with pytest.raises(TypeError):
        _ = BadTracker() # pylint: disable=abstract-class-instantiated

    good_tracker = GoodTracker()
    assert len(good_tracker.rvec_rolling_means) == 0
    assert len(good_tracker.tvec_rolling_means) == 0

    with pytest.raises(NotImplementedError):
        good_tracker.close()

    with pytest.raises(NotImplementedError):
        good_tracker.get_frame()

    with pytest.raises(NotImplementedError):
        good_tracker.get_tool_descriptions()

    with pytest.raises(NotImplementedError):
        good_tracker.start_tracking()

    with pytest.raises(NotImplementedError):
        good_tracker.stop_tracking()

    config = {'smoothing buffer' : 3}

    rigid_bodies = []
    rigid_bodies.append(RigidBody('test rb'))
    rigid_bodies.append(RigidBody('test rb'))
    another_good_tracker = GoodTracker(config, rigid_bodies)

    port_handles, time_stamps, frame_numbers, tracking, tracking_quality = \
                    another_good_tracker.get_smooth_frame(["test rb"])

    assert len(port_handles) == 1
    assert len(time_stamps) == 1
    assert len(frame_numbers) == 1
    assert len(tracking) == 1
    assert len(tracking_quality) == 1

    assert np.isnan(tracking_quality[0])

    with pytest.raises(ValueError):
        port_handles, time_stamps, frame_numbers, tracking, tracking_quality = \
                        another_good_tracker.get_smooth_frame(["another body",
                            "test rb"])

    port_handles = ["another body", "test rb"]
    time_stamps = [1.2, 1.3]
    frame_numbers = [0, 0]
    tracking_rot = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]
    tracking_trans = [[50.0, -100.0, 70.0], [0.0, 100.0, 200.0]]
    quality = [1.0, 0.5]
    rot_is_quaternion = False

    another_good_tracker.add_frame_to_buffer(port_handles, time_stamps,
                    frame_numbers,
                    tracking_rot, tracking_trans, quality,
                    rot_is_quaternion)

    port_handles_out, time_stamps, frame_numbers, tracking, tracking_quality = \
                     another_good_tracker.get_smooth_frame(port_handles)

    test_index = port_handles_out.index("test rb")
    assert time_stamps[test_index] == 1.3
    assert frame_numbers[test_index] == 0
    rotation = construct_rx_matrix(1.0, True)
    transform = construct_rigid_transformation(rotation, [0.0, 100.0, 200.0])
    assert np.allclose(tracking[test_index], transform)
    assert tracking_quality[test_index] == 0.5

    port_handles = ["test rb"]
    time_stamps = [1.4]
    frame_numbers = [1]
    tracking_rot = [[0.2, 0.0, 0.0]]
    tracking_trans = [[10.0, 50.0, 200.0]]
    quality = [0.8]

    another_good_tracker.add_frame_to_buffer(port_handles, time_stamps,
                    frame_numbers,
                    tracking_rot, tracking_trans, quality,
                    rot_is_quaternion)

    port_handles_out, time_stamps, frame_numbers, tracking, tracking_quality = \
                     another_good_tracker.get_smooth_frame(port_handles)

    assert len(port_handles_out) == 1

    port_handles = ["another body", "test rb"]

    port_handles_out, time_stamps, frame_numbers, tracking, tracking_quality = \
                     another_good_tracker.get_smooth_frame(port_handles)

    assert len(port_handles_out) == 2

    test_index = port_handles_out.index("test rb")
    assert time_stamps[test_index] == 1.35
    assert frame_numbers[test_index] == 1
    rotation = construct_rx_matrix(0.6, True)
    transform = construct_rigid_transformation(rotation, [5.0, 75.0, 200.0])
    assert np.allclose(tracking[test_index], transform)
    assert tracking_quality[test_index] == 0.65

    test_index = port_handles_out.index("another body")
    assert time_stamps[test_index] == 1.2
    assert frame_numbers[test_index] == 0
    rotation = construct_rx_matrix(0.0, True)
    transform = construct_rigid_transformation(rotation, [50.0, -100.0, 70.0])
    assert np.allclose(tracking[test_index], transform)
    assert tracking_quality[test_index] == 1.0


def test_tracker_quaternions():
    """
    Similar to above but with quaternions
    """

    config = {
                    'smoothing buffer' : 3,
                    'use quaternions' : True
              }


    rigid_bodies = []
    rigid_bodies.append(RigidBody('test rb'))
    another_good_tracker = GoodTracker(config, rigid_bodies)

    port_handles, time_stamps, frame_numbers, tracking, tracking_quality = \
                    another_good_tracker.get_smooth_frame(["test rb"])

    assert len(port_handles) == 1
    assert len(time_stamps) == 1
    assert len(frame_numbers) == 1
    assert len(tracking) == 1
    assert len(tracking_quality) == 1

    assert np.isnan(tracking_quality[0])

    with pytest.raises(ValueError):
        port_handles, time_stamps, frame_numbers, tracking, tracking_quality = \
                        another_good_tracker.get_smooth_frame(["another body",
                            "test rb"])

    port_handles = ["another body", "test rb"]
    time_stamps = [1.2, 1.3]
    frame_numbers = [0, 0]
    tracking_rot = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]
    tracking_trans = [[50.0, -100.0, 70.0], [0.0, 100.0, 200.0]]
    quality = [1.0, 0.5]
    rot_is_quaternion = False

    another_good_tracker.add_frame_to_buffer(port_handles, time_stamps,
                    frame_numbers,
                    tracking_rot, tracking_trans, quality,
                    rot_is_quaternion)

    port_handles_out, time_stamps, frame_numbers, tracking, tracking_quality = \
                     another_good_tracker.get_smooth_frame(port_handles)

    test_index = port_handles_out.index("test rb")
    assert time_stamps[test_index] == 1.3
    assert frame_numbers[test_index] == 0
    transform = np.full((1,7), np.nan)
    rotation = _rvec_to_quaternion([1.0, 0.0, 0.0])
    transform[0,0:4] = rotation
    transform[0,4:7] = [0.0, 100.0, 200.0]
    assert np.allclose(tracking[test_index], transform)
    assert tracking_quality[test_index] == 0.5

    port_handles = ["test rb"]
    time_stamps = [1.4]
    frame_numbers = [1]
    tracking_rot = [[0.2, 0.0, 0.0]]
    tracking_trans = [[10.0, 50.0, 200.0]]
    quality = [0.8]

    another_good_tracker.add_frame_to_buffer(port_handles, time_stamps,
                    frame_numbers,
                    tracking_rot, tracking_trans, quality,
                    rot_is_quaternion)

    port_handles_out, time_stamps, frame_numbers, tracking, tracking_quality = \
                     another_good_tracker.get_smooth_frame(port_handles)

    assert len(port_handles_out) == 1

    port_handles = ["another body", "test rb"]

    port_handles_out, time_stamps, frame_numbers, tracking, tracking_quality = \
                     another_good_tracker.get_smooth_frame(port_handles)

    assert len(port_handles_out) == 2

    test_index = port_handles_out.index("test rb")
    assert time_stamps[test_index] == 1.35
    assert frame_numbers[test_index] == 1

    rotation = _rvec_to_quaternion([0.6, 0.0, 0.0])
    transform[0,0:4] = rotation
    transform[0,4:7] = [5.0, 75.0, 200.0]
    assert np.allclose(tracking[test_index], transform)
    assert tracking_quality[test_index] == 0.65

    test_index = port_handles_out.index("another body")
    assert time_stamps[test_index] == 1.2
    assert frame_numbers[test_index] == 0

    rotation = _rvec_to_quaternion([0.0, 0.0, 0.0])
    transform[0,0:4] = rotation
    transform[0,4:7] = [50.0, -100.0, 70.0]
    assert np.allclose(tracking[test_index], transform)
    assert tracking_quality[test_index] == 1.0

    port_handles = ["another body", "test rb"]
    time_stamps = [1.6, 1.5]
    frame_numbers = [2, 2]
    tracking_rot = [_rvec_to_quaternion([0.0, 0.9, 0.0]),
                    _rvec_to_quaternion([0.6, 0.0, 0.0])]
    tracking_trans = [[50.0, -100.0, 70.0], [0.0, 100.0, 100.0]]
    quality = [1.0, 0.5]
    rot_is_quaternion = True

    another_good_tracker.add_frame_to_buffer(port_handles, time_stamps,
                    frame_numbers,
                    tracking_rot, tracking_trans, quality,
                    rot_is_quaternion)

    port_handles = ["another body"]

    port_handles_out, time_stamps, frame_numbers, tracking, tracking_quality = \
                     another_good_tracker.get_smooth_frame(port_handles)

    assert len(port_handles_out) == 1

    test_index = port_handles_out.index("another body")
    assert time_stamps[test_index] == 1.4
    assert frame_numbers[test_index] == 2
    rotation = _rvec_to_quaternion([0.0, 0.45, 0.0])
    transform[0,4:7] = [50.0, -100.0, 70.0]
    transform[0,0:4] = rotation
    assert np.allclose(tracking[test_index], transform)
    assert tracking_quality[test_index] == 1.0

    port_handles = ["another body", "test rb"]

    port_handles_out, time_stamps, frame_numbers, tracking, tracking_quality = \
                     another_good_tracker.get_smooth_frame(port_handles)

    assert len(port_handles_out) == 2

    test_index = port_handles_out.index("test rb")
    assert math.isclose(time_stamps[test_index],1.4)
    assert frame_numbers[test_index] == 2
    rotation = _rvec_to_quaternion([0.6, 0.00, 0.0])
    transform[0,0:4] = rotation
    transform[0,4:7] = [3.333333, 83.33333, 166.666667]
    assert np.allclose(tracking[test_index], transform)
    assert tracking_quality[test_index] == 0.6
