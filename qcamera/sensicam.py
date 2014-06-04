"""PCO Sensicam interface

There are a lot of hacks in this interface because the PCO SDK is
extremely low level. Therefore, it could likely use a lot of
optimization.

"""

from __future__ import print_function
import logging
import traceback as tb
import math
import ctypes
import numpy as np
import camera
from camera_errors import SensicamError
from sensicam_status_codes import *

class MODE(ctypes.Structure):
    _pack_ = 0
    _fields_ = [
        ("mode", ctypes.c_int8),
        ("submode", ctypes.c_int8)]

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

    # Valid trigger modes.
    _trigger_modes = {
        "software": 0,
        "rising": 1,
        "falling": 2
    }

    def _chk(self, code):
        """Check the return code of a command. The error messages are
        complicated 32 bit strings which are described in detail in
        the SDK manual. In short, to quote the manual:

        * Bits 0-11 are used to indicate the error number.
        * Bits 12-15 shows the layer of the error source.
        * Bits 16-23 reflect the error source.
        * Bits 24-28 are not used.
        * Bit 29 is the common error group flag. This flag is used to lookup
        * the error text inside the correct array.
        * Bit 31 indicates an error.
        * Bit 30 is set in addition to bit 31 and indicates a warning. 

        """
        code = code & 0xFFFFFFFF # convert the negative integer to the proper hex representation
        hex_ = "0x%0.8X" % code
        if code != 0:
            # Get the offending device and layer.                
            #device = code & SENSICAM_CODES['PCO_ERROR_DEVICE_MASK']
            layer = code & SENSICAM_CODES['PCO_ERROR_LAYER_MASK']
            index = code & SENSICAM_CODES['PCO_ERROR_CODE_MASK']

            # Evaluate layer text
            if layer == SENSICAM_CODES['PCO_ERROR_FIRMWARE']:
                layer_text = "Firmware"
            elif layer == SENSICAM_CODES['PCO_ERROR_DRIVER']:
                layer_text = "Driver"
            elif layer == SENSICAM_CODES['PCO_ERROR_SDKDLL']:
                layer_text = "SDK DLL"
            elif layer == SENSICAM_CODES['PCO_ERROR_APPLICATION']:
                layer_text = "Application"
            else:
                layer_text = "Unknown layer???"

            # Evaluate errors and warnings
            is_warning = code & SENSICAM_CODES['PCO_ERROR_IS_WARNING']
            if code & SENSICAM_CODES['PCO_ERROR_IS_COMMON']:
                error_text = PCO_ERROR_COMMON_TXT[index]
            if layer == SENSICAM_CODES['PCO_ERROR_FIRMWARE']:
                error_text = PCO_ERROR_FIRMWARE_TXT[index]
            elif layer == SENSICAM_CODES['PCO_ERROR_DRIVER']:
                error_text = PCO_ERROR_DRIVER_TXT[index]
            elif layer == SENSICAM_CODES['PCO_ERROR_SDKDLL']:
                error_text = PCO_ERROR_SDKDLL_TXT[index]
            elif layer == SENSICAM_CODES['PCO_ERROR_APPLICATION']:
                error_text = PCO_ERROR_APPLICATION_TXT[index]
            else:
                error_text = "Unknown error???"

            # Raise error or warn
            if not is_warning:
                self.logger.error(error_text)
                self.logger.debug("error code: " + hex_)
                raise SensicamError(error_text)
            else:
                self.logger.warn(
                    "Sensicam warning: " + error_text + \
                    "\n\tLayer = " + layer_text)
                self.logger.debug("warning code: " + hex_)
                stack = tb.extract_stack()
                self.logger.debug(''.join(tb.format_list(stack)))
    
    # Setup and shutdown
    # ------------------

    def initialize(self, **kwargs):
        """Initialize a PCO Sensicam.

        Keyword arguments
        -----------------
        bins : int
            Specifies the number of binned pixels to use. Defaults to
            1.
        crop : list
            A tuple of the form [x, y, width, height] specifying the
            cropped portion of the sensor to use. If None, use the
            full sensor. Defaults to [1, 1, 640, 480].

        """

        # Get kwargs.
        bins = kwargs.get('bins', 1)
        crop = kwargs.get('crop', [1, 1, 640, 480])

        # Check kwargs.
        assert isinstance(bins, int)
        assert isinstance(crop, (list, tuple, np.ndarray))
        
        # Load the DLL.
        self.clib = ctypes.windll.sen_cam

        # Initalize the camera.
        self.filehandle = ctypes.c_int()
        self._chk(self.clib.INITBOARD(0, ctypes.pointer(self.filehandle)))
        self._chk(self.clib.SETUP_CAMERA(self.filehandle))
        self.mode = (0, 0) # Long exposure, normal analog gain

        # Get the "actual" sizes and bits per pixel.
        # Presumably this takes into account hardware cropping and
        # binning, but the documentation is not terribly clear.
        x, y = ctypes.c_int(), ctypes.c_int()
        x_actual = ctypes.c_int()
        y_actual = ctypes.c_int()
        bit_pix = ctypes.c_int()
        self.clib.GETSIZES(
            self.filehandle,
            ctypes.pointer(x), ctypes.pointer(y),
            ctypes.pointer(x_actual), ctypes.pointer(y_actual),
            ctypes.pointer(bit_pix))
        self.x_actual = x_actual.value
        self.y_actual = y_actual.value
        self.bit_pix = bit_pix.value
        self.shape = (x.value, y.value)
        self.crop = (1, x.value, 1, y.value)
        self.logger.debug(
            "Result of GETSIZES:\n" + \
            "\tx pixels: %i, y pixels: %i\n" % (self.shape[0], self.shape[1]) + \
            "\tx_actual: %i, y_actual: %i\n" % (self.x_actual, self.y_actual) + \
            "\tbit_pix: %i" % self.bit_pix)

        # Buffer allocation.
        self.address = ctypes.c_void_p()
        self.buffer_number = ctypes.c_int(-1)
        self.buffer_size = ctypes.c_int(int(self.x_actual*self.y_actual*((self.bit_pix + 7)/8)))
        self._chk(self.clib.ALLOCATE_BUFFER(
            self.filehandle, ctypes.pointer(self.buffer_number),
            ctypes.pointer(self.buffer_size)))
        self._chk(self.clib.MAP_BUFFER(
            self.filehandle, self.buffer_number, self.buffer_size, 0,
            ctypes.pointer(self.address)))
        self._chk(self.clib.SETBUFFER_EVENT(
            self.filehandle, self.buffer_number,
            ctypes.pointer(ctypes.c_int(-1))))

        # Write camera settings to the hardware
        self._update_coc()

        # Run COC
        self._chk(self.clib.RUN_COC(self.filehandle, 0))

    def _to_sensi_crop(self, crop):
        """Convert a crop tuple/list in actual pixels into PCO's units
        of 32 pixels.

        """
        if len(crop) != 4:
            raise SensicamError("crop must be a length 4 tuple.")
        sensi_crop = [int(math.floor(x/32.)) for x in crop]
        sensi_crop = [1 if x == 0 else x for x in sensi_crop]
        return sensi_crop

    def _test_coc(self, mode, trigger, crop, bins, delay, t_exp):
        """Test the parameters to give to the SDK SET_COC
        function. This will modify the values using the SDK TEST_COC
        function to the nearest acceptable values.

        The arguments are the same as the kwargs given to
        :func:`_update_coc.`.

        """

        # TODO: Maybe the check should go somewhere else so that this
        # can fake something if it's not a real camera?
        if not self.real_camera:
            return
            
        # Prepare C data
        _ptr = lambda x: ctypes.pointer(x)
        self.logger.debug(
            "Trying the following values for TEST_COC:\n" + \
            "\tmode: %i, %i\n" % (mode[0], mode[1]) + \
            "\ttrigger: %i\n" % trigger + \
            "\tcrop: %i, %i, %i, %i\n" % (crop[0], crop[1], crop[2], crop[3]) + \
            "\tbins: %i\n" % bins + \
            "\ttiming: %i, %i" % (delay, t_exp))
        c_mode = ctypes.c_int(0) #MODE(mode[0], mode[1])
        c_trigger = ctypes.c_int(trigger)
        c_crop_x1 = ctypes.c_int(crop[0])
        c_crop_x2 = ctypes.c_int(crop[1])
        c_crop_y1 = ctypes.c_int(crop[2])
        c_crop_y2 = ctypes.c_int(crop[3])
        xbins, ybins = ctypes.c_int(bins), ctypes.c_int(bins)
        timing = "%i,%i" % (delay, t_exp)
        c_timing = ctypes.c_char_p(timing)
        self._chk(self.clib.TEST_COC(
            self.filehandle, _ptr(c_mode), _ptr(c_trigger),
            _ptr(c_crop_x1), _ptr(c_crop_x2), _ptr(c_crop_y1), _ptr(c_crop_y2),
            _ptr(xbins), _ptr(ybins),
            c_timing, _ptr(ctypes.c_int(len(timing)))))

        # Update values if there are differences
        # TODO: fix mode check
        #if c_mode.value != mode:
        #    logging.debug(
        #        "Desired mode not accepted by TEST_COC, adjusting: %i -> %i" \
        #        % (mode, c_mode.value))
        if c_trigger.value != trigger:
            self.logger.debug(
                "Desired trigger not accepted by TEST_COC, adjusting: %i -> %i" \
                % (trigger, c_trigger.value))
            trigger = c_trigger.value
        new_crop = [c_crop_x1.value, c_crop_x2.value,
                    c_crop_y1.value, c_crop_y2.value]
        for i, x in enumerate(new_crop):
            if x != crop[i]:
                self.logger.debug(
                    "Invalid crop parameter from TEST_COC: " + \
                    "Changing crop[%i] = %i -> %i" % (i, crop[i], new_crop[i]))
                crop[i] = x
        if xbins.value != bins or ybins.value != bins:
            self.logger.debug(
                "Invalid bin argument in TEST_COC. Changing %i -> %i" \
                % (bins, xbins.value))
            bins = xbins
        # TODO: add timing check

        # Return new parameters
        return mode, trigger, crop, bins, delay, t_exp
        
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
        mode : tuple
            Length 2 tuple describing the camera operation type and
            analog gain. See p. 12 of the manual.
        trigger : int
        crop : tuple
            Length 4 tuple specifying the new region of interest.
        bins : int
            Binning to use.
        delay : int
        t_exp : int
            Exposure time in ms.

        """
        
        # Update mode.
        mode = kwargs.get('mode', (0, 0))
        if len(mode) != 2:
            raise SensicamError("mode must be a length 2 tuple.")
        c_mode = MODE(mode[0], mode[1])

        # Update trigger.
        trigger = kwargs.get('trigger', self._trigger_modes[self.trigger_mode])
        if trigger not in range(2):
            raise SensicamError("trigger_mode most be one of 0, 1, 2.")

        # Update crop
        # NOTE: In the SDK, this is referred to as the ROI, but in our
        # usage, the ROI is set in software. Also, for some reason it
        # wants units of 32 pixels.
        crop = kwargs.get('crop', self.crop)
        self.crop = crop
        if len(crop) != 4:
            raise SensicamError("crop must be a length 4 tuple.")
        crop = self._to_sensi_crop(crop)
        self.logger.debug("Result of _to_sensi_crop:" + \
            "\n\tself.crop = " + str(self.crop) +\
            "\n\tsensi_crop = " + str(crop))
        
        # Update bins.
        bins = kwargs.get('bins', self.bins)
        if bins not in [2**x for x in range(5)]:
            raise SensicamError("bins must be a power of 2 and <= 16.")

        # Update timing.
        delay = kwargs.get('delay', 0)
        if not 0 <= delay <= 1000000:
            raise SensicamError("delay must be between 0 and 1E6 ms.")
        t_exp = kwargs.get('t_exp', self.t_ms)
        if not 1 <= t_exp <= 1000000:
            raise SensicamError("t_exp must be between 1 and 1E6 ms.")
        timing = ctypes.c_char_p("%i,%i" % (delay, t_exp))

        # Test new values and update class attributes.
        mode, trigger, crop, bins, delay, t_exp = \
            self._test_coc(mode, trigger, crop, bins, delay, t_exp)
        self.bins = bins
        self.t_ms = t_exp

        # Log and update settings.
        self.logger.debug(
            "Updating Sensicam COC:\n" + \
            "\tmode: %i, %i\n" % (mode[0], mode[1]) + \
            "\ttrigger: %i\n" % trigger + \
            "\tcrop: %i, %i, %i, %i\n" % (crop[0], crop[1], crop[2], crop[3]) + \
            "\tbins: %i\n" % bins + \
            "\ttiming: %i, %i" % (delay, t_exp))
        if not self.real_camera:
             return
        self._chk(self.clib.SET_COC(
            self.filehandle, c_mode, trigger,
            crop[0], crop[1], crop[2], crop[3],
            bins, bins, timing))
    
        # TODO: Update x/y_actual more sensibly. Or handle the
        # variable better.
        dummy = ctypes.pointer(ctypes.c_int(-1))
        x_actual = ctypes.c_int(0)
        y_actual = ctypes.c_int(0)
        self.clib.GETSIZES(
            self.filehandle, dummy, dummy,
            ctypes.pointer(x_actual), ctypes.pointer(y_actual), dummy)
        self.x_actual = x_actual.value
        self.y_actual = y_actual.value

    def close(self):
        """Close the camera safely. Anything necessary for doing so
        should be defined here.

        """
        if not self.real_camera:
            return
        self._chk(self.clib.STOP_COC(self.filehandle, 0))
        self._chk(self.clib.REMOVE_ALL_BUFFERS_FROM_LIST(self.filehandle))
        self._chk(self.clib.FREE_BUFFER(self.filehandle, self.buffer_number))
        self._chk(self.clib.CLOSEBOARD(ctypes.pointer(self.filehandle)))
        
    # Image acquisition
    # -----------------

    def set_acquisition_mode(self, mode):
        """Set the image acquisition mode."""
        super(Sensicam, self).set_acquisition_mode(mode)
        if not self.real_camera:
            return
        # TODO
        self.logger.warn("No action: set_acquisition_mode not yet implemented.")
        #self._update_coc()

    def acquire_image_data(self):
        """Acquire the current image from the camera."""
        # Times 2 because the camera returns 16 bit data... despite
        # the function having 12 bit in the name...
        bytes_to_read = self.x_actual*self.y_actual*2
        timeout = int(self.t_ms*3)
        self._chk(self.clib.WAIT_FOR_IMAGE(self.filehandle, timeout))
        self._chk(self.clib.READ_IMAGE_12BIT(
            self.filehandle, 0, self.x_actual, self.y_actual, self.address))
        img = np.fromstring(
            ctypes.string_at(self.address, bytes_to_read), dtype=np.uint16)
        shape = (self.crop[1]/self.bins, self.crop[3]/self.bins)[::-1]
        img.shape = shape
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
        self.logger.warn("No action. set_trigger_mode not yet implemented.")
        #self._update_coc() 

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
        self._update_coc(t_exp=self.t_ms)

    def get_gain(self):
        """Query the current gain settings."""

    def set_gain(self, gain, **kwargs):
        """Set the camera gain."""
        super(Sensicam, self).set_gain(gain, kwargs)
        if not self.real_camera:
            return
        # TODO
        self.logger.warn("No action. set_gain not yet implemented.")
        #self._update_coc()

    # ROI, cropping, and binning
    # --------------------------

    def set_roi(self, roi):
        """Define the region of interest."""
        super(Sensicam, self).set_roi(roi)
        # TODO
        
    def get_crop(self):
        """Get the current CCD crop settings."""

    def set_crop(self, crop):
        """
        Define the portion of the CCD to actually collect data
        from. Using a reduced sensor area typically allows for faster
        readout.

        """
        super(Sensicam, self).set_crop(crop)
        self.logger.info("Setting crop to: %s" % repr(self.crop))
        self._chk(self.clib.STOP_COC(self.filehandle, 0))
        self._update_coc(crop=crop)
        self._chk(self.clib.RUN_COC(self.filehandle, 0))
        
    def get_bins(self):
        """Query the current binning."""

    def set_bins(self, bins):
        """Set binning to bins x bins."""
        super(Sensicam, self).set_bins(bins)
        self.logger.info("Setting bins to: %i" % self.bins)
        self._chk(self.clib.STOP_COC(self.filehandle, 0))
        self._update_coc(bins=bins)
        self._chk(self.clib.RUN_COC(self.filehandle, 0))

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    with Sensicam(real=True) as cam:
        cam.test_real_time_acquisition()
        