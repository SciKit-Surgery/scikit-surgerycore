"""
Tests for skcore baseclasses
"""

import pytest

from sksurgerycore.baseclasses.tracker import SKSBaseTracker

def test_tracker_baseclass():
    """
    We should throw not implemented error when we make a tracker without
    the required functions.
    """
    class BadTracker(SKSBaseTracker):# pylint: disable=abstract-method
        """
        A tracker class without the necessary member functions.
        """
        def close(self):
            pass

    with pytest.raises(TypeError):
        _ = BadTracker() # pylint: disable=abstract-class-instantiated


    class GoodTracker(SKSBaseTracker):
        """
        A tracker class with the necessary member functions.
        """
        def __init__(self, configuration = None, tracked_objects = None):
            super().__init__(configuration, tracked_objects) # pylint: disable=useless-super-delegation
        def close(self):# pylint: disable=useless-super-delegation
            super().close()
        def get_frame(self):# pylint: disable=useless-super-delegation
            super().get_frame()
        def get_tool_descriptions(self):# pylint: disable=useless-super-delegation
            super().get_tool_descriptions()
        def start_tracking(self):# pylint: disable=useless-super-delegation
            super().start_tracking()
        def stop_tracking(self):# pylint: disable=useless-super-delegation
            super().stop_tracking()

    good_tracker = GoodTracker()
    assert good_tracker.rvec_rolling_means[0]._buffer.shape == (1,4)
    assert good_tracker.tvec_rolling_means[0]._buffer.shape == (1,3)

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
    another_good_tracker = GoodTracker(config)

    assert another_good_tracker.rvec_rolling_means[0]._buffer.shape == (3,4)
    assert another_good_tracker.tvec_rolling_means[0]._buffer.shape == (3,3)

    class RigidBody():
        def __init__(self):
            self.name = "test rb"

    rigid_bodies = []
    rigid_bodies.append(RigidBody())
    rigid_bodies.append(RigidBody())
    another_good_tracker = GoodTracker(config, rigid_bodies)

