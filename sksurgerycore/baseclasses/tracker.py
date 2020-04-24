"""An abstract base class for trackers used in sksurgery"""
from abc import ABCMeta, abstractmethod

@abstractmethod
class SKSBaseTracker(metaclass=ABCMeta):
    """Abstract base class for trackers using in sksurgery.
    Defines methods that all trackers should implement.
    """
    @abstractmethod
    def close(self):
        """Closes the connection to the tracker"""
        raise NotImplementedError

    @abstractmethod
    def get_frame(self):
        """
        :return:

            port_numbers : list of port handles, one per tool

            time_stamps : list of timestamps (cpu clock), one per tool

            frame_numbers : list of framenumbers (tracker clock) one per tool

            tracking : list of 4x4 tracking matrices, rotation and position,
            or if use_quaternions is true, a list of tracking quaternions,
            column 0-2 is x,y,z column 3-6 is the rotation as a quaternion.

            tracking_quality : list the tracking quality, one per tool.
            """
        raise NotImplementedError

    @abstractmethod
    def get_tool_descriptions(self):
        """
        :return: list of port handles
        :return: list of tool descriptions
        """
        raise NotImplementedError

    @abstractmethod
    def start_tracking(self):
        """
        Tells the tracker to start tracking.
        """
        raise NotImplementedError

    @abstractmethod
    def stop_tracking(self):
        """
        Tells the tracker to stop tracking.
        """
        raise NotImplementedError
