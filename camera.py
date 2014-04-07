"""
qcamera base camera class

This file contains the class definition for the Camera class on which
all subsequent cameras should be based on.

"""

from __future__ import division
from __future__ import print_function
from abc import ABCMeta, abstractmethod
import numpy as np
import numpy.random as npr
from camera_errors import UnitsError

_t_units = {'ms': 1, 's': 1e3} # Allowed units for exposure time

class Camera:
    """Abstract base class for all cameras."""
    __metaclass__ = ABCMeta

    # Members
    # -------
    
    roi = [1, 0, 1, 0]	# Region of interest
    t_ms = 100.		# exposure time in ms
    shape = [512, 512]	# number of pixels [x, y]
    bins = 1		# binning of the sensor
    real_camera = True  # True if the camera hardware actually exists

    # Setup and shutdown
    # ------------------

    def __init__(self, real=True):
        self.real_camera = real

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

    def get_simulated_image(self, x0, y0):
        """
        Generate and return a simulated image centered at the point
        (x0, y0). This is primarily useful when testing out a full
        control program so that there is a simulated camera with an
        image to actually use.

        """
        g = lambda x, y, x0, y0, sigma: \
            np.exp(-((x - x0)**2 + (y - y0)**2)/(2*sigma**2))
        x = np.arange(0, self.shape[0])
        y = np.arange(0, self.shape[1])
        X, Y = np.meshgrid(x, y)
        img = g(x, y, x0, y0, 20)
        img /= np.max(img)
        img += 0.25*npr.random(self.shape)
        return img

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

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    class Test(Camera):
        pass
    cam = Test(real=False)
    x0, y0 = npr.randint(0, self.shape[0]), npr.randint(0, self.shape[1])
    plt.imshow(cam.get_simulated_image(x0, y0))
    plt.colorbar()
    plt.show()
