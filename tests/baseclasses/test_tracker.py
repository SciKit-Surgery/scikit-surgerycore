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
