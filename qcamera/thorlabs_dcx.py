"""Thorlabs DCx series cameras

Drivers for Windows and Linux can be downloaded from Thorlabs__.

__ http://www.thorlabs.de/software_pages/viewsoftwarepage.cfm?code=DCx

"""

from __future__ import print_function
import sys
from camera import Camera
import ctypes
import time

def _chk(msg):
    """Check for errors from the C library."""
    # TODO
    pass

class ThorlabsDCx(Camera):
    """Class for Thorlabs DCx series cameras."""

    # Setup and shutdown
    # ------------------

    def initialize(self,**kwargs):
        """Initialize the camera."""
        # Load the library.
        if 'win' in sys.platform:
            try:
                self.clib = ctypes.cdll.uc480_64
            except:
                self.clib = ctypes.cdll.uc480
        else:
            self.clib = ctypes.cdll.LoadLibrary('libueye_api.so')

        # Initialize the camera. The filehandle being 0 initially
        # means that the first available camera will be used. This is
        # not really the right way of doing things if there are
        # multiple cameras installed, but it's good enough for a lot
        # of cases.
        self.filehandle = ctypes.c_int(0)
        _chk(self.clib.is_InitCamera(
            ctypes.pointer(self.filehandle)))

        # Enable autoclosing. This allows for safely closing the
        # camera if it is disconnected.
        _chk(self.clib.is_EnableAutoExit(self.filehandle, 1))

    def close(self):
        """Close the camera safely."""
        _chk(self.clib.is_ExitCamera(self.filehandle))
    def start(self):
        print("Starting??")
        
    def stop(self):
        print("Stopping??")
    # Image acquisition
    # -----------------

    def set_acquisition_mode(self, mode):
        """Set the image acquisition mode."""

    def acquire_image_data(self):
        """Code for getting image data from the camera should be
        placed here.

        """
        #time.sleep(1)
        raise NotImplementedError("You must define this method.")
        
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

    # Gain and exposure time
    # ----------------------

    def get_exposure_time(self):
        """Query for the current exposure time."""

    def set_exposure_time(self, t, units='ms'):
        """Set the exposure time."""
        time.sleep(1)
        print("Setting exposure time")
        super(ThorlabsDCx,self).set_exposure_time(t,)

    def get_gain(self):
        """Query the current gain settings."""

    def set_gain(self, gain, **kwargs):
        """Set the camera gain."""

    # Cooling
    # -------

    def cooler_on(self):
        """Turn on the TEC."""
        raise NotImplementedError("No cooler?")

    def cooler_off(self):
        """Turn off the TEC."""
        raise NotImplementedError("No cooler?")

    def get_cooler_temperature(self):
        """Check the TEC temperature."""
        raise NotImplementedError("No cooler?")

    def set_cooler_temperature(self, temp):
        """Set the cooler temperature to temp."""
        raise NotImplementedError("No cooler?")

    # ROI, cropping, and binning
    # --------------------------

    def set_roi(self, roi):
        """Define the region of interest."""
        super(ThorlabsDCx,self).set_roi(roi)
        
    def get_crop(self):
        """Get the current CCD crop settings."""

    def set_crop(self, crop):
        """Define the portion of the CCD to actually collect data
        from. Using a reduced sensor area typically allows for faster
        readout.

        """
        super(ThorlabsDCx,self).set_crop(crop)
        
    def get_bins(self):
        """Query the current binning."""

    def set_bins(self, bins):
        """Set binning to bins x bins."""

if __name__ == "__main__":
    #clib = ctypes.cdll.uc480
    #import ctypes.wintypes
#    print(clib.is_GetOsVersion())
#    version = clib.is_GetDLLVersion()
#    print("Build",version & 0xFFFF)
#    version = version >> 16
#    print("minor", version & 0xFF)
#    version = version >> 8
#    print("major", version & 0xFF)
    #clib.is_GetNumberOfCameras.restype = ctypes.c_int
#    number = ctypes.c_int()
#    #clib.is_GetNumberOfCameras.argtypes = [ctypes.wintypes.POINTER(ctypes.c_int)]
#    test = ctypes.c_int(4)
#    mypointer = ctypes.addressof(number)
#    mypointer = ctypes.c_int()
#    test = clib.is_GetNumberOfCameras(ctypes.pointer(mypointer))
#    print(test)
#    print(mypointer.value)
    #print(clib.is_InitCamera(0))
    
    
    
    
    
    with ThorlabsDCx() as cam:
        pass
    
    
    
    
    
    
