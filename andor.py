"""
Andor camera interface

"""

from __future__ import print_function
import ctypes
import time
import warnings
import camera
from camera_errors import AndorError
from andor_error_codes import ANDOR_ERRORS

def _chk(status):
    """Run the callable func and check the error status."""
    if status == 20072: # Acquiring
        warnings.warn(
            "Action not completed when data acquisition is in progress!")
    elif status == 20034: # temperature off
        warnings.warn("Temperature control is off.")
    elif status == 20037: # temperature not reached
        warnings.warn("Temperature set point not yet reached.")
    elif status == 20040: # temperature drift
        warnings.warn("Temperature is drifting.")
    elif status == 20036: # temperature not stabilized
        warnings.warn(
            "Temperature set point reached but not yet stable.")
    elif status == 20036: # temperature *is* stabilized
        pass
    elif status != 20002:
        raise AndorError(
            "Andor returned the status message " + \
            ANDOR_ERRORS[status])

class AndorCamera(camera.Camera):
    """
    Class for controlling Andor cameras. This is designed specifically
    with the iXon series cameras, but the Andor API is rather generic
    so should work with most or all of their cameras.

    """

    # Valid trigger modes.
    # There are more that are not implemented here, some of which are
    # only valid on particular camera models.
    _trigger_modes = {
        "internal": 0,
        "external": 1,
        "external start": 6,
        "software": 10}

    # Setup and shutdown
    # ------------------

    def __init__(self, temperature=-50):
        """
        Initialize the Andor camera.

        Parameters
        ----------
        temperature : int
            Temperature in Celsius to set the TEC to.

        """
        # Try to load the Andor DLL
        self.clib = ctypes.windll.LoadLibrary("atmcd32d.dll")

        # Initialize the camera and get the detector size
        _chk(self.clib.Initialize("."))
        xpx = ctypes.pointer(c_int(0))
        ypx = ctypes.pointer(c_int(0))
        _chk(self.clib.GetDetector(xpx, ypx))
        self.shape = [xpx.contents, ypx.contents]

        # Get hardware and software information
        # TODO
        _chk(self.clib.GetHardwareVersion())
        _chk(self.clib.GetSoftwareVersion())
        _chk(self.clib.GetNumberVSSpeeds())
        _chk(self.clib.GetVSSpeed())
        _chk(self.clib.GetNumberHSSpeeds())
        _chk(self.clib.GetHSSpeed())

        # Enable temperature control
        # TODO
        _chk(GetTemperatureRange())
        self.set_cooler_temperature(temperature) # TODO: check setting
        self.cooler_on()

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        self.close()

    def close(self):
        """
        Turn off temperature regulation and safely shutdown the
        camera.

        The Andor SDK guide indicates that for classic and ICCD
        systems, it is best to wait until the temperature is above -20
        degrees C before shutting down, so this will wait until that
        condition is met.

        """
        self.cooler_off()
        while True:
            temp = self.get_cooler_temperature()
            if temp > -20:
                break
            else:
                time.sleep(1)
        _chk(self.clib.ShutDown())

    # Triggering and image acquisition
    # --------------------------------

    def get_trigger_mode(self):
        """Query the current trigger mode."""

    def set_trigger_mode(self, mode):
        """
        Setup trigger mode.

        Parameters
        ----------
        mode : str
            Specifies the mode to use and must be one of the (non-case
            sensitive) strings found in self._trigger_modes.

        """
        mode = mode.lower()
        if mode not in self._trigger_modes:
            raise AndorError("Invalid trigger mode: " + mode)
        _chk(SetTriggerMode(self._trigger_modes[mode])

    def trigger(self):
        """Send a software trigger to take an image immediately."""

    def get_image(self):
        """
        Acquire the current image from the camera. This is mainly to
        be used when running in some sort of single trigger
        acquisition mode.

        """

    # Gain and exposure time
    # ----------------------

    def get_exposure_time(self):
        """Query for the current exposure time."""
        return self.t_ms

    def set_exposure_time(self, t, units='ms'):
        """Set the exposure time."""
        super(AndorCamera, self).set_exposure_time(t, units)
        t_s = self.t_ms*1000
        _chk(self.clib.SetExposureTime(t_s))

    def get_gain(self):
        """Query the current gain settings."""

    def set_gain(self, gain, **kwargs):
        """Set the camera gain."""

    # Cooling
    # -------

    def cooler_on(self):
        """Turn on the TEC."""
        _chk(self.dll.CoolerON())

    def cooler_off(self):
        """Turn off the TEC."""
        _chk(self.clib.CoolerOFF())

    def get_cooler_temperature(self):
        """Check the TEC temperature."""
        temp = ctypes.pointer(ctypes.c_int(0))
        _chk(self.clib.GetTemperature(temp))
        return temp

    def set_cooler_temperature(self, temp):
        """Set the cooler temperature to temp."""
        _chk(self.clib.SetTemperature(ctypes.c_int(temp)))

    # ROI, cropping, and binning
    # --------------------------

    def set_roi(self, roi):
        """Define the region of interest."""
        
    def get_crop(self):
        """Get the current CCD crop settings."""

    def set_crop(self, crop):
        """
        Define the portion of the CCD to actually collect data
        from. Using a reduced sensor area typically allows for faster
        readout.

        """
        
    def get_bins(self):
        """Query the current binning."""

    def set_bins(self, bins):
        """Set binning to bins x bins."""
