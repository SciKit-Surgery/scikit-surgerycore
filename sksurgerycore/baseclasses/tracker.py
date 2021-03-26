"""An abstract base class for trackers used in sksurgery"""
from abc import ABCMeta, abstractmethod
from sksurgerycore.algorithms.tracking_smoothing import RollingMean, \
                RollingMeanRotation

class SKSBaseTracker(metaclass=ABCMeta):
    """Abstract base class for trackers using in sksurgery.
    Defines methods that all trackers should implement.
    """

    def __init__(self, configuration = None, tracked_objects = None):
        buffer_size = 1
        if configuration is not None:
            buffer_size = configuration.get('smoothing buffer', 1)

        #actually, we need a buffer for each rigid body. What
        #do we do for things like the aruco, where we can have 
        #dynamically occuring rigid bodies?
        self.port_handles = []
        self.time_stamps = []
        self.frame_numbers = []
        self.qualities = []
        self.rvec_rolling_means = []
        self.tvec_rolling_means = []
       
        if tracked_objects is not None:
            for tracked_object in tracked_objects:
                self.port_handles.append(tracked_object.name);
                self.time_stamps.append(RollingMean(1, buffer_size, datatype = float))
                self.frame_numbers.append(RollingMean(1, buffer_size, datatype = int))
                self.qualities.append(RollingMean(1, buffer_size, datatype = float))
                self.rvec_rolling_means.append(RollingMeanRotation(buffer_size))
                self.tvec_rolling_means.append(RollingMean(3, buffer_size))
        else:
            self.rvec_rolling_means.append(RollingMeanRotation(buffer_size))
            self.tvec_rolling_means.append(RollingMean(3, buffer_size))


    
    def smooth_tracking(self, port_handles, tracking, etc):
       """
       Can be called by derived classes to smooth the tracking
       """
       return

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
