"""Template file for creating new camera interfaces."""

from __future__ import print_function
import ctypes
import numpy as np
import camera
from camera_errors import *

class Template(camera.Camera):
    """Docstring me!"""

    # Setup and shutdown
    # -------------------------------------------------------------------------

    def _chk(self, status):
        """Use this function to wrap around C calls in order to check
        return codes.

        """
    
    def _initialize(self, **kwargs):
        """Initialization should take place here."""

    def get_camera_properties(self):
        """Code for getting camera properties should go here."""

    def close(self):
        """Close the camera safely. Anything necessary for doing so
        should be defined here.

        """

    # Image acquisition
    # -------------------------------------------------------------------------

    def set_acquisition_mode(self, mode):
        """Set the image acquisition mode."""

    def _acquire_image_data(self):
        """Code for getting image data from the camera should be
        placed here. This must return a numpy array.

        """

    # Triggering
    # -------------------------------------------------------------------------

    def get_trigger_mode(self):
        """Query the current trigger mode."""

    def set_trigger_mode(self, mode):
        """Setup trigger mode."""

    def start(self):
        """Code needed for getting the camera to begin triggering
        should be placed here.

        """

    def stop(self):
        """Code needed to stop accepting triggering should be placed
        here.

        """

    # Shutter control
    # -------------------------------------------------------------------------

    def _set_shutter(self, state):
        """This will set the shutter to the given state ('open' or
        'closed'). Since not all cameras have a built in shutter, this
        will simply do nothing if not overridden.

        """
        pass

    # Gain and exposure time
    # -------------------------------------------------------------------------

    def _update_exposure_time(self, t):
        """Code required to change the camera exposure time should go
        here.

        """

    def get_gain(self):
        """Query the current gain settings."""

    def set_gain(self, **kwargs):
        """Set the camera gain."""

    # Cooling
    # -------------------------------------------------------------------------

    # Simply delete these functions if the camera you are implementing
    # doesn't have a built-in cooler.

    def cooler_on(self):
        """Turn on the TEC."""

    def cooler_off(self):
        """Turn off the TEC."""

    def get_cooler_temperature(self):
        """Check the TEC temperature."""

    def set_cooler_temperature(self, temp):
        """Set the cooler temperature to temp."""

    # Cropping and binning
    # -------------------------------------------------------------------------

    def _update_crop(self, crop):
        """Camera-specific code for setting the crop should go
        here.

        """

    def set_bins(self, bins):
        """Set binning to bins x bins."""
