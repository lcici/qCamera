"""Thorlabs DCx series cameras

Drivers for Windows and Linux can be downloaded from Thorlabs__.

__ http://www.thorlabs.de/software_pages/viewsoftwarepage.cfm?code=DCx

"""

from __future__ import print_function
import sys
from camera import Camera
import ctypes

def _chk(msg):
    """Check for errors from the C library."""
    # TODO
    pass

class ThorlabsDCx(Camera):
    """Class for Thorlabs DCx series cameras."""

    # Setup and shutdown
    # ------------------

    def _initialize(self):
        """Initialize the camera."""
        # Load the library.
        if 'win' in sys.platform:
            try:
                self.clib = ctypes.windll.uc480_64
            except:
                self.clib = ctypes.windll.uc480
        else:
            self.clib = ctypes.cdll.LoadLibrary('libueye_api.so')

        # Initialize the camera. The filehandle being 0 initially
        # means that the first available camera will be used. This is
        # not really the right way of doing things if there are
        # multiple cameras installed, but it's good enough for a lot
        # of cases.
        self.filehandle = ctypes.c_int(0)
        _chk(self.clib.is_InitCamera(
            ctypes.pointer(self.filehandle), None))

        # Enable autoclosing. This allows for safely closing the
        # camera if it is disconnected.
        _chk(self.clib.is_EnableAutoExit(self.filehandle, 1))

    def close(self):
        """Close the camera safely."""
        _chk(self.clib.is_ExitCamera(self.filehandle))
        
    # Image acquisition
    # -----------------

    def set_acquisition_mode(self, mode):
        """Set the image acquisition mode."""

    def _acquire_image_data(self):
        """Code for getting image data from the camera should be
        placed here.

        """
        raise NotImplementedError("You must define this method.")

    # Gain and exposure time
    # ----------------------

    def _update_exposure_time(self, t):
        """Set the exposure time."""

    def get_gain(self):
        """Query the current gain settings."""

    def set_gain(self, gain, **kwargs):
        """Set the camera gain."""

if __name__ == "__main__":
    with ThorlabsDCx() as cam:
        pass
