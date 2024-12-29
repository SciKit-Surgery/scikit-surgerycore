"""An abstract base class for trackers used in sksurgery"""
from abc import ABCMeta, abstractmethod
import numpy as np
from sksurgerycore.algorithms.tracking_smoothing import RollingMean, \
                RollingMeanRotation, quaternion_to_matrix

class SKSBaseTracker(metaclass=ABCMeta):
    """Abstract base class for trackers using in sksurgery.
    Defines methods that all trackers should implement.
    """

    def __init__(self, configuration = None, tracked_objects = None):
        self.buffer_size = 1
        if configuration is not None:
            self.buffer_size = configuration.get('smoothing buffer', 1)

        self.use_quaternions = False
        if configuration is not None:
            self.use_quaternions = configuration.get('use quaternions', False)
        self.port_handles = []
        self.time_stamps = []
        self.frame_numbers = []
        self.qualities = []
        self.rvec_rolling_means = []
        self.tvec_rolling_means = []

        if tracked_objects is not None:
            for tracked_object in tracked_objects:
                self.port_handles.append(tracked_object.name)
                self.time_stamps.append(RollingMean(1, self.buffer_size,
                        datatype = float))
                #let's not average the frame numbers, set buffer = 1
                self.frame_numbers.append(RollingMean(1, 1,
                        datatype = int))
                self.qualities.append(RollingMean(1, self.buffer_size,
                        datatype = float))
                self.rvec_rolling_means.append(
                                RollingMeanRotation(self.buffer_size))
                self.tvec_rolling_means.append(RollingMean(3, self.buffer_size))

    def get_smooth_frame(self, port_handles):
        """
        Called by derived classes to return smoothed data

        :param port_handles: a list of port handles to get data for

        :returns:

            port_numbers : list of port handles, one per tool

            time_stamps : list of timestamps (cpu clock), one per tool

            frame_numbers : list of framenumbers (tracker clock) one per tool

            tracking : list of 4x4 tracking matrices, rotation and position,
            or if use_quaternions is true, a list of tracking quaternions,
            column 0-3 is the rotation as a quaternion (qw, qx, qy, qz),
            column 4-6 is the translation (x,y,z).

            tracking_quality : list the tracking quality, one per tool.
        """
        smth_handles = []
        smth_times = []
        smth_frame_nos = []
        smth_tracking = []
        smth_qual = []
        for port_handle in port_handles:
            try:
                my_index = self.port_handles.index(port_handle)
                smth_handles.append(port_handle)
                smth_times.append(self.time_stamps[my_index].getmean()[0])
                smth_frame_nos.append(self.frame_numbers[my_index].getmean()[0])
                mean_quat = self.rvec_rolling_means[my_index].getmean()
                mean_tvec = self.tvec_rolling_means[my_index].getmean()
                smth_qual.append(self.qualities[my_index].getmean()[0])

                if self.use_quaternions:
                    output_matrix = np.full((1,7), np.nan)
                    output_matrix[0,0:4] = mean_quat
                    output_matrix[0,4:7] = mean_tvec
                    smth_tracking.append(output_matrix)

                else:
                    output_matrix = np.identity(4, dtype=np.float64)
                    output_matrix[0:3, 0:3] = quaternion_to_matrix(mean_quat)
                    output_matrix[0:3, 3] = mean_tvec
                    smth_tracking.append(output_matrix)

            except ValueError:
                raise ValueError(str(port_handle) + " not found in tracking " +
                                 "buffers, did you call smooth_tracking " +
                                 "before add_frame?") from ValueError

        assert len(smth_handles) == len(port_handles)

        return smth_handles, smth_times, smth_frame_nos, smth_tracking, \
                        smth_qual

    # pylint: disable=too-many-positional-arguments
    def add_frame_to_buffer(self, port_handles, time_stamps, frame_numbers,
                    tracking_rot, tracking_trans, quality,
                    rot_is_quaternion = False):
        """
        Called by derived classes to add data to the smoothing buffers

        :param port_handles: a list of port handles
        :param time_stamps: list of timestamps (cpu clock), one per tool
        :param frame_numbers: list of framenumbers (tracker clock) one per tool
        :param tracking_rot: list of tracking rotations
        :param tracking_trans: list of tracking translations
        :param quality: list the tracking quality, one per tool.
        :param rot_is_quaternion: True if rotation is a quaternion.
        """
        for your_index, port_handle in enumerate(port_handles):
            my_index = None
            try:
                my_index = self.port_handles.index(port_handle)

            except ValueError:
                self.port_handles.append(port_handle)
                self.time_stamps.append(RollingMean(1, self.buffer_size,
                            datatype = float))
                self.frame_numbers.append(RollingMean(1, 1,
                            datatype = float))
                self.qualities.append(RollingMean(1, self.buffer_size,
                            datatype = float))
                self.rvec_rolling_means.append(
                                RollingMeanRotation(self.buffer_size))
                self.tvec_rolling_means.append(RollingMean(3, self.buffer_size))
                my_index = self.port_handles.index(port_handle)

            assert my_index >= 0

            self.time_stamps[my_index].pop(time_stamps[your_index])
            self.frame_numbers[my_index].pop(frame_numbers[your_index])
            self.rvec_rolling_means[my_index].pop(tracking_rot[your_index],
                            rot_is_quaternion)
            self.tvec_rolling_means[my_index].pop(tracking_trans[your_index])
            self.qualities[my_index].pop(quality[your_index])


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
            column 0-3 is the rotation as a quaternion (qw, qx, qy, qz),
            column 4-6 is the translation (x,y,z).

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
