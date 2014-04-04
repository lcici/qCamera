"""
qcamera base camera class

This file contains the class definition for the Camera class on which
all subsequent cameras should be based on.

"""

from abc import ABCMeta, abstractmethod
from camera_errors import UnitsError

_t_units = {'ms': 1, 's': 1e3} # Allowed units for exposure time

class Camera(object):
    """Abstract base class for all cameras."""
    __metaclass__ = ABCMeta

    # Members
    # -------
    
    roi = [1, 0, 1, 0]	# Region of interest
    t_ms = 100.		# exposure time in ms
    shape = [0, 0]	# number of pixels [x, y]

    # Setup and shutdown
    # ------------------

    def __init__(self):
        return

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        self.close()

    @abstractmethod
    def close(self):
        """
        Close the camera safely. Anything necessary for doing so
        should be defined here.
        
        """

    # Triggering and image acquisition
    # --------------------------------

    @abstractmethod
    def get_trigger_mode(self):
        """Query the current trigger mode."""

    @abstractmethod
    def set_trigger_mode(self, mode):
        """Setup trigger mode."""

    @abstractmethod
    def trigger(self):
        """Send a software trigger to take an image immediately."""

    @abstractmethod
    def get_image(self):
        """
        Acquire the current image from the camera. This is mainly to
        be used when running in some sort of single trigger
        acquisition mode.

        """

    # Gain and exposure time
    # ----------------------

    @abstractmethod
    def get_exposure_time(self):
        """Query for the current exposure time."""

    @abstractmethod
    def set_exposure_time(self, t, units='ms'):
        """Set the exposure time."""
        try:
            self.t_ms = t*_t_units[units]
        except KeyError:
            raise UnitsError(
                "Exposure time units must be one of: " + _t_units.keys())

    @abstractmethod
    def get_gain(self):
        """Query the current gain settings."""

    @abstractmethod
    def set_gain(self, gain, **kwargs):
        """Set the camera gain."""

    # Cooling
    # -------

    @abstractmethod
    def cooler_on(self):
        """Turn on the TEC."""

    @abstractmethod
    def cooler_off(self):
        """Turn off the TEC."""

    @abstractmethod
    def get_cooler_temperature(self):
        """Check the TEC temperature."""

    @abstractmethod
    def set_cooler_temperature(self, temp):
        """Set the cooler temperature to temp."""

    # ROI, cropping, and binning
    # --------------------------

    @abstractmethod
    def set_roi(self, roi):
        """Define the region of interest."""
        
    @abstractmethod
    def get_crop(self):
        """Get the current CCD crop settings."""

    @abstractmethod
    def set_crop(self, crop):
        """
        Define the portion of the CCD to actually collect data
        from. Using a reduced sensor area typically allows for faster
        readout.

        """
        
    @abstractmethod
    def get_bins(self):
        """Query the current binning."""

    @abstractmethod
    def set_bins(self, bins):
        """Set binning to bins x bins."""

