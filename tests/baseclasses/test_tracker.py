"""
Tests for matrix.py
"""

import pytest

from sksurgerycore.baseclasses.tracker import SKSBaseTracker

def test_tracker_baseclass():

    class BadTracker(SKSBaseTracker):
        def close(self):
            pass

    with pytest.raises(TypeError):
        bad_tracker = BadTracker()
    

    class GoodTracker(SKSBaseTracker):
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
