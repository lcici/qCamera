"""Generic video capture using OpenCV."""

from __future__ import division
import numpy as np
import cv2
import camera
from camera_errors import CameraError

# Constants from OpenCV
# =============================================================================

# Unfortunately, these don't seem to be defined anywhere in the cv2
# module, so I'm manually setting the ones I need here.

CV_CAP_PROP_FRAME_WIDTH = 3
CV_CAP_PROP_FRAME_HEIGHT = 4
CV_CAP_PROP_FPS = 5
CV_CAP_PROP_BRIGHTNESS = 10
CV_CAP_PROP_CONTRAST = 11
CV_CAP_PROP_SATURATION = 12
CV_CAP_PROP_HUE = 13
CV_CAP_PROP_GAIN = 14
CV_CAP_PROP_EXPOSURE = 15

# OpenCV camera class
# =============================================================================

class OpenCVCamera(camera.Camera):
    """Class for OpenCV video capture using the standard qCamera
    functions. OpenCV will Just Work for quite a few web cams and
    similar devices.

    """

    # Setup and shutdown
    # -------------------------------------------------------------------------
    
    def initialize(self, **kwargs):
        """Open the camera.

        Keyword Arguments
        -----------------
        port : int
            If given, this is the camera port to use with the
            cv2.VideoCapture function. Defaults to 0.

        """
        # Get and check kwargs
        port = kwargs.get('port', 0)
        assert isinstance(port, int)
        assert port >= 0

        # Try to open the camera
        if not self.real_camera:
            return
        self.cam = cv2.VideoCapture(port)
        if not self.cam.isOpened():
            raise CameraError("Opening the camera failed!")

    def get_camera_properties(self):
        """Nothing to do here, move along."""
        pass

    def close(self):
        """Close the camera."""
        if self.real_camera:
            self.cam.release()

    # Image acquisition
    # -------------------------------------------------------------------------

    def set_acquisition_mode(self, mode):
        """Set the image acquisition mode."""

    def acquire_image_data(self):
        """Read the image data from the camera."""
        retval, img = self.cam.read()
        if not retval:
            raise CameraError(
                "Reading the image failed! Was the camera disconnected?")
        return img

    # Triggering
    # -------------------------------------------------------------------------

    # Triggering is not really relevant for OpenCV video capture, but
    # the start and stop methods must be implemented for threading to
    # work properly.

    def get_trigger_mode(self):
        """Query the current trigger mode."""

    def set_trigger_mode(self, mode):
        """Setup trigger mode."""

    def start(self):
        pass

    def stop(self):
        pass

    # Gain and exposure time
    # -------------------------------------------------------------------------

    def set_exposure_time(self, t):
        """Change the exposure time by setting the FPS property."""
        self.t_ms = t
        if not self.real_camera:
            return
        t = t/1000.
        fps = 1/t
        self.cam.set(CV_CAP_PROP_FPS, fps)

    def get_gain(self):
        """Query the current gain settings."""

    def set_gain(self, **kwargs):
        """Set the camera gain."""

    # Cropping and binning
    # -------------------------------------------------------------------------

    def update_crop(self, crop):
        """Camera-specific code for setting the crop should go
        here.

        """

    def set_bins(self, bins):
        """Set binning to bins x bins."""

if __name__ == "__main__":
    with OpenCVCamera(recording=False) as cam:
        cam.set_exposure_time(100)
        cam.test_real_time_acquisition()
        