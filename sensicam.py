"""Sensicam interface.

"""

from __future__ import print_function
import time
import warnings
import ctypes
import numpy as np
import camera
from camera_errors import CameraError

class Sensicam(camera.Camera):
    """Class for controlling PCO Sensicam cameras."""
    # Setup and shutdown
    # ------------------

    def __init__(self, real=True):
        super(Sensicam, self).__init__(real)

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        print("Shutting down camera.")
        self.close()

    def close(self):
        """
        Close the camera safely. Anything necessary for doing so
        should be defined here.
        
        """
        
    # Image acquisition
    # -----------------

    def set_acquisition_mode(self, mode):
        """Set the image acquisition mode."""

    def get_image(self):
        """
        Acquire the current image from the camera. This is mainly to
        be used when running in some sort of single trigger
        acquisition mode.

        """
        
    # Triggering
    # ----------

    def get_trigger_mode(self):
        """Query the current trigger mode."""

    def set_trigger_mode(self, mode):
        """Setup trigger mode."""

    def trigger(self):
        """Send a software trigger to take an image immediately."""
        
    # Shutter control
    # ---------------

    def open_shutter(self):
        """Open the shutter."""
        self.shutter_open = True
        
    def close_shutter(self):
        """Close the shutter."""
        self.shutter_open = False
        
    def toggle_shutter(self):
        """Toggle the shutter state from open to closed and vice versa."""
        if self.shutter_open:
            self.close_shutter()
        else:
            self.open_shutter()

    # Gain and exposure time
    # ----------------------

    def get_exposure_time(self):
        """Query for the current exposure time."""

    def set_exposure_time(self, t, units='ms'):
        """Set the exposure time."""
        super(Sensicam, self).set_exposure_time(t, units)

    def get_gain(self):
        """Query the current gain settings."""

    def set_gain(self, gain, **kwargs):
        """Set the camera gain."""

    # Cooling
    # -------

    def cooler_on(self):
        """Turn on the TEC."""

    def cooler_off(self):
        """Turn off the TEC."""

    def get_cooler_temperature(self):
        """Check the TEC temperature."""

    def set_cooler_temperature(self, temp):
        """Set the cooler temperature to temp."""

    # ROI, cropping, and binning
    # --------------------------

    def set_roi(self, roi):
        """Define the region of interest."""
        if len(roi) != 4:
            raise CameraError("roi must be a length 4 list.")
        self.roi = roi
        
    def get_crop(self):
        """Get the current CCD crop settings."""

    def set_crop(self, crop):
        """
        Define the portion of the CCD to actually collect data
        from. Using a reduced sensor area typically allows for faster
        readout.

        """
        if len(crop) != 4:
            raise CameraError("crop must be a length 4 array.")
        self.crop = crop
        
    def get_bins(self):
        """Query the current binning."""

    def set_bins(self, bins):
        """Set binning to bins x bins."""
