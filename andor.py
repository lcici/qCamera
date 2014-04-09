"""
Andor camera interface

"""

from __future__ import print_function
import time
import warnings
import ctypes
import numpy as np
import camera
from camera_errors import AndorError, AndorWarning
from andor_error_codes import ANDOR_ERRORS

def _int_ptr(val=0):
    """Utility function to create integer pointers."""
    return ctypes.pointer(ctypes.c_int(val))
    
def _warn(msg):
    """Warn with an AndorWarning."""
    # TODO: fix warning messages (says None now)
    warnings.warn(msg, AndorWarning)

def _chk(status):
    """
    Checks the error status of an Andor DLL function call. If
    something catastrophic happened, an AndorError exception is
    raised. In non-critical cases, warnings are given.

    Parameters
    ----------
    status : int
        The return code from an Andor DLL function.

    Raises
    ------
    AndorError
        Whenever something very bad happens. Generally, this should
        hopefully only be whenever the user is trying to do something
        stupid.

    """
    if status == 20072: # Acquiring
        _warn("Action not completed when data acquisition is in progress!")
    elif status == 20034: # temperature off
        #_warn("Temperature control is off.")
        pass
    elif status == 20037: # temperature not reached
        _warn("Temperature set point not yet reached.")
    elif status == 20040: # temperature drift
        _warn("Temperature is drifting.")
    elif status == 20035 or status == 20036: # temperature not stabilized
        #_warn("Temperature set point reached but not yet stable.")
        pass
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

    # Valid acquisition modes.
    _acq_modes = {
        "single": 1,
        "accumulate": 2,
        "kinetics": 3,
        "fast kinetics": 4,
        "run till abort": 5}

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

    def __init__(self, temperature=-50, bins=None, crop=None, real=True):
        """
        Initialize the Andor camera.

        Keyword arguments
        -----------------
        temperature : int
            Temperature in Celsius to set the TEC to.
        bins : int or None
            Specifies the number of binned pixels to use.
        crop : tuple or None
            A tuple of the form [x, y, width, height] specifying the
            cropped portion of the sensor to use. If None, use the
            full sensor.
        real : bool
            If False, the camera will be simulated.        

        """
        # Check if we are simulating a camera or using a real one
        super(AndorCamera, self).__init__(real=real)
        if not self.real_camera:
            return
        
        # Try to load the Andor DLL
        self.clib = ctypes.windll.LoadLibrary("atmcd32d.dll")

        # Initialize the camera and get the detector size
        # TODO: directory to Initialize?
        _chk(self.clib.Initialize("."))
        xpx, ypx = _int_ptr(), _int_ptr()
        _chk(self.clib.GetDetector(xpx, ypx))
        self.shape = [xpx.contents.value, ypx.contents.value]

        # Configure binning and cropping
        if bins is not None:
            self.set_bins(bins)
        if crop is not None:
            self.set_crop(crop)

        # TODO: Get hardware and software information?

        # Enable temperature control
        T_min, T_max = _int_ptr(), _int_ptr()
        _chk(self.clib.GetTemperatureRange(T_min, T_max))
        self.T_min = T_min.contents.value
        self.T_max = T_max.contents.value
        self.set_cooler_temperature(temperature)
        self.cooler_on()

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
        self.close_shutter()
        while True:
            temp = self.get_cooler_temperature()
            if temp > -20:
                break
            else:
                time.sleep(1)
        _chk(self.clib.ShutDown())
        
    # Image acquisition
    # -----------------
        
    def set_acquisition_mode(self, mode):
        """Set the image acquisition mode."""
        if mode not in self._acq_modes:
            raise AndorError(
                "Acquisition mode must be one of " + repr(self._acq_modes))
        self.acq_mode = mode
        if not self.real_camera:
            return
        _chk(self.clib.SetAcquisitionMode(
            ctypes.c_int(self._acq_modes['mode'])))
    
    def get_image(self):
        """
        Acquire the current image from the camera. This is mainly to
        be used when running in some sort of single trigger
        acquisition mode.

        """
        if self.acq_mode != "single":
            _warn("Not in single acquisition mode!")
        if not self.real_camera:
            return self.get_simulated_image()
        img_size = self.shape[0]*self.shape[1]/self.bins**2
        img_array = np.zeros(img_size)
        img_pointer = (ctypes.c_int32*img_size)(*img_array)
        _chk(self.clib.GetAcquiredData(img_pointer, ctypes.c_ulong(img_size)))
        img_array = np.frombuffer(img_pointer, dtype=ctypes.c_int32)
        img_array.reshape(self.shape)
        return img_array
        
    # Triggering
    # ----------

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
        if self.real_camera:
            _chk(self.clib.SetTriggerMode(self._trigger_modes[mode]))
        
    def trigger(self):
        """Send a software trigger to take an image immediately."""
        # TODO: only work if in software trigger mode
        if self.real_camera:
            _chk(self.clib.StartAcquisition())
        
    # Shutter control
    # ---------------

    def open_shutter(self):
        """Open the shutter."""
        super(AndorCamera, self).open_shutter()
        if self.real_camera:
            _chk(self.clib.SetShutter(1, 1, 20, 20))
        
    def close_shutter(self):
        """Close the shutter."""
        super(AndorCamera, self).close_shutter()
        if self.real_camera:
            _chk(self.clib.SetShutter(1, 2, 20, 20))

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
        if self.real_camera:
            _chk(self.clib.CoolerON())

    def cooler_off(self):
        """Turn off the TEC."""
        if self.real_camera:
            _chk(self.clib.CoolerOFF())

    def get_cooler_temperature(self):
        """Check the TEC temperature."""
        # TODO: make this work better with simulated cameras
        if not self.real_camera:
            return 20
        temp = _int_ptr()
        _chk(self.clib.GetTemperature(temp))
        return temp.contents.value

    def set_cooler_temperature(self, temp):
        """Set the cooler temperature to temp."""
        # TODO: make this work better with simulated cameras
        if not self.real_camera:
            pass
        if temp > self.T_max or temp < self.T_min:
            raise ValueError(
                "Set point temperature must be between " + \
                repr(self.T_min) + " and " + repr(self.T_max) + ".")
        _chk(self.clib.SetTemperature(temp))

    # ROI, cropping, and binning
    # --------------------------

    def set_roi(self, roi):
        """Define the region of interest."""
        super(AndorCamera, self).set_roi(roi)
        
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
        
if __name__ == "__main__":
    with AndorCamera(temperature=10) as cam:
        cam.set_acquisition_mode('single')
        cam.set_exposure_time(10)
        cam.trigger()
        cam.get_image()
