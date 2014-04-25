"""Sensicam interface.

"""

from __future__ import print_function
import time
import warnings
import ctypes
import numpy as np
import camera
from camera_errors import SensicamError, SensicamWarning

class Sensicam(camera.Camera):
    """Class for controlling PCO Sensicam cameras."""

    # COC gain modes. See p. 24 of the API documentation.
    _coc_gain_modes = {
        "normal": 0,
        "extended": 1}

    # COC submodes. See p. 24 of the API documentation.
    # This sets specifics for exposure modes. For example, 'single'
    # means one trigger yields one exposure and 'double' means one
    # trigger yields two exposures.
    _coc_submodes = {
        "single": 0, # single trigger mode (DPSINGLE)
        "multi": 1,  # multi trigger mode (DPMULTI)
        "double": 2  # double trigger mode (DPDOUBLE)
    }

    # Valid trigger modes. See p. 16 of the API documentation.
    # TODO: all possible options?
    _trigger_modes = {
        "internal": 0x0,
        "external": 0x001 # external with rising edge
    }
    
    # Setup and shutdown
    # ------------------

    def __init__(self, real=True):
        super(Sensicam, self).__init__(real)
        self.clib = ctypes.windll.LoadLibrary("") # TODO

    def close(self):
        """
        Close the camera safely. Anything necessary for doing so
        should be defined here.
        
        """
        pass
        
    # Image acquisition
    # -----------------

    def set_acquisition_mode(self, mode):
        """Set the image acquisition mode."""
        super(Sensicam, self).set_acquisition_mode(mode)

    def get_image(self):
        """
        Acquire the current image from the camera. This is mainly to
        be used when running in some sort of single trigger
        acquisition mode.

        """
        super(Sensicam, self).get_image()
        
    # Triggering
    # ----------

    def get_trigger_mode(self):
        """Query the current trigger mode."""

    def set_trigger_mode(self, mode):
        """Setup trigger mode."""
        super(Sensicam, self).set_trigger_mode(mode)

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
        super(Sensicam, self).set_gain(gain, kwargs)

    # ROI, cropping, and binning
    # --------------------------

    def set_roi(self, roi):
        """Define the region of interest."""
        super(Sensicam, self).set_roi(roi)
        
    def get_crop(self):
        """Get the current CCD crop settings."""

    def set_crop(self, crop):
        """
        Define the portion of the CCD to actually collect data
        from. Using a reduced sensor area typically allows for faster
        readout.

        """
        super(Sensicam, self).set_crop(self, crop)
        
    def get_bins(self):
        """Query the current binning."""

    def set_bins(self, bins):
        """Set binning to bins x bins."""
        super(Sensicam, self).set_bins(bins)
