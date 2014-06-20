"""Generic video capture using OpenCV."""

import numpy as np
import cv2
import camera
from camera_errors import CameraError

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
        assert port > 0

        # Try to open the camera
        if not self.real_camera:
            return
        self.cam = cv2.VideoCapture(port)
        if not self.cam.isOpened():
            raise CameraError("Opening the camera failed!")

    def close(self):
        """Close the camera."""
        if self.real_camera:
            self.cam.release()

    # Image acquisition
    # -------------------------------------------------------------------------

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

    def start(self):
        pass

    def stop(self):
        pass

