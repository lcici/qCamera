"""Sensicam interface

Much of this was adapted from the older sensicam module written
primarily by Magnus and Gregers.

"""

from __future__ import print_function
import time
import warnings
import ctypes
import numpy as np
import camera
from camera_errors import SensicamError, SensicamWarning

def _chk(code):
    """Check the return code of a command.

    TODO: Do saner testing (at least translate the error codes!)

    """
    if code != 0:
        raise SensicamError("Camera error code " + str(code) + ".")

class CAMTYPE(ctypes.Structure):
    _pack_ = 0
    _fields_ = [("gain", ctypes.c_bool*2),
                ("CCDtype", ctypes.c_bool*2),
                ("Cameratype", ctypes.c_bool*2),
                ("sensicam", ctypes.c_bool*3),
                ("CCDcolor", ctypes.c_bool),
                ("Shutter", ctypes.c_bool*2),
                ("temp_reg", ctypes.c_bool*1),
                ("reserved", ctypes.c_bool*5)]

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

    def __init__(self, bins=None, crop=None, real=True):
        """Initialize a PCO Sensicam.

        Keyword arguments
        -----------------
        bins : int or None
            Specifies the number of binned pixels to use.
        crop : tuple or None
            A tuple of the form [x, y, width, height] specifying the
            cropped portion of the sensor to use. If None, use the
            full sensor.
        real : bool
            If False, the camera will be simulated.
        
        """
        
        # Check if using a real or simulated camera.
        super(Sensicam, self).__init__(real=real)
        if not self.real_camera:
            return
        self.clib = ctypes.windll.LoadLibrary("sen_cam.dll")

        # Initalize the camera.
        self.filehandle = ctypes.c_int()
        _chk(self.clib.INITBOARD(0, ctypes.pointer(self.filehandle)))
        _chk(self.clib.SETUP_CAMERA(self.filehandle))

        # Acquire hardware information. See p. 34 of the API
        # documentation for details.
        camtype = CAMTYPE()
        ele_temp = ctypes.c_int()
        ccd_temp = ctypes.c_int()
        _chk(self.clib.GET_STATUS(self.filehandle, ctypes.pointer(camtype),
                                  ctypes.pointer(ele_temp), ctypes.pointer(ccd_temp)))
        if camtype.CCDtype[0] == 0 and camtype.CCDtype[1] == 0:
            self.shape = (640, 480)
        elif camtype.CCDtype[0] == 0 and camtype.CCDtype[1] == 1:
            self.shape = (640, 480)
        elif camtype.CCDtype[0] == 1 and camtype.CCDtype[1] == 0:
            self.shape = (1280, 1024)
        else:
            raise SensicamError("Unknown CCD type.")

        # Buffer mapping
        # I don't know what this means!
        # TODO: figure out the 00000 parameters
        # TODO: self.size
        self.address = ctypes.c_void_p
        self.buffer_number = ctypes.c_int(-1)
        self.size = None # c_int(self.width.value * self.height.value * ((self.bit_pix.value + 7) / 8))
        
        _chk(self.clib.MAP_BUFFER(
            self.filehandle, 00000, 00000, 0, ctypes.pointer(self.address)))
        _chk(self.clib.ALLOCATE_BUFFER(
            self.filehandle, ctypes.pointer(self.buffer_number),
            ctypes.pointer(self.size)))

        # Write camera settings to the hardware
        # TODO
        self._update_coc()

    def _update_coc(self, **kwargs):
        """Update the 'camera operation code', i.e., set everything
        from acquisition modes to triggering to binning. This function
        is intended to be called internally, hence the leading
        underscore. Only keyword arguments that are passed are
        updated.

        TODO: Proper documentation
        TODO: Proper testing

        Keyword arguments
        -----------------
        mode : ?
        trigger : int
        roi : tuple
            Length 4 tuple specifying the new region of interest.
        bins : int
            Binning to use.
        delay : int
        t_exp : int
            Exposure time in ms.

        """
        mode = None # TODO
        trigger = kwargs.get('trigger', self.trigger_mode) # TODO
        roi = kwargs.get('roi', self.roi)
        bins = kwargs.get('bins', self.bins)
        delay = kwargs.get('delay', 0)
        t_exp = kwargs.get('t_exp', self.t_ms)
        table = ctypes.c_char_p("%i,%i" % (delay, t_exp))
        _chk(self.clib.SET_COC(
            self.filehandle, mode, trigger, roi[0], roi[1], roi[2], roi[3],
            bins, bins, table))

    def close(self):
        """Close the camera safely. Anything necessary for doing so
        should be defined here.

        """
        if not self.real_camera:
            return
        _chk(self.clib.REMOVE_ALL_BUFFERS_FROM_LIST(self.filehandle))
        # TODO: _chk(self.clib.FREE_BUFFER(self.filehandle, self.buffer_number) 
        _chk(self.clib.CLOSEBOARD(ctypes.pointer(self.filehandle)))
        
    # Image acquisition
    # -----------------

    def set_acquisition_mode(self, mode):
        """Set the image acquisition mode."""
        super(Sensicam, self).set_acquisition_mode(mode)
        if not self.real_camera:
            return
        
        # TODO
        self._update_coc()

    def acquire_image_data(self):
        """Acquire the current image from the camera. This is mainly
        to be used when running in some sort of single trigger
        acquisition mode.

        """
        bytes_to_read = self.shape[0]*self.shape[1]*2 # I don't know why
        _chk(self.clib.READ_IMAGE_12BIT(
            self.filehandle, 0, self.shape[0], self.shape[1], self.address))
        img = np.fromstring(
            ctypes.string_at(self.address, bytes_to_read), dtype=np.uint16)
        img.shape = self.shape
        return img
        
    # Triggering
    # ----------

    def get_trigger_mode(self):
        """Query the current trigger mode."""

    def set_trigger_mode(self, mode):
        """Setup trigger mode."""
        super(Sensicam, self).set_trigger_mode(mode)
        if not self.real_camera:
            return

        # TODO
        self._update_coc() 

    def trigger(self):
        """Send a software trigger to take an image immediately."""
        
    # Shutter control
    # ---------------

    def open_shutter(self):
        """Open the shutter."""
        super(Sensicam, self).open_shutter()
        
    def close_shutter(self):
        """Close the shutter."""
        super(Sensicam, self).close_shutter()

    # Gain and exposure time
    # ----------------------

    def get_exposure_time(self):
        """Query for the current exposure time."""

    def set_exposure_time(self, t, units='ms'):
        """Set the exposure time."""
        super(Sensicam, self).set_exposure_time(t, units)
        if not self.real_camera:
            return

        # TODO
        self._update_coc()

    def get_gain(self):
        """Query the current gain settings."""

    def set_gain(self, gain, **kwargs):
        """Set the camera gain."""
        super(Sensicam, self).set_gain(gain, kwargs)
        if not self.real_camera:
            return

        # TODO
        self._update_coc()

    # ROI, cropping, and binning
    # --------------------------

    def set_roi(self, roi):
        """Define the region of interest."""
        super(Sensicam, self).set_roi(roi)

        # TODO
        self._update_coc()
        
    def get_crop(self):
        """Get the current CCD crop settings."""

    def set_crop(self, crop):
        """
        Define the portion of the CCD to actually collect data
        from. Using a reduced sensor area typically allows for faster
        readout.

        """
        super(Sensicam, self).set_crop(self, crop)

        # TODO
        self._update_coc()
        
    def get_bins(self):
        """Query the current binning."""

    def set_bins(self, bins):
        """Set binning to bins x bins."""
        super(Sensicam, self).set_bins(bins)

        # TODO
        self._update_coc() 

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    with Sensicam(real=False) as cam:
        for i in range(10):
            img = cam.get_image()
            plt.figure()
            plt.imshow(img)
            plt.show()
