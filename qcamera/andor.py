"""Andor camera interface"""

from __future__ import print_function
import time
import traceback as tb
import ctypes
import numpy as np
import camera
from camera_errors import AndorError, AndorWarning
from andor_status_codes import *
from andor_capabilities import *

def _int_ptr(val=0):
    """Utility function to create integer pointers."""
    return ctypes.pointer(ctypes.c_int(val))

class AndorCamera(camera.Camera):
    """Class for controlling Andor cameras. This is designed
    specifically with the iXon series cameras, but the Andor API is
    rather generic so should work with most or all of their
    cameras.

    """

    # Utilities
    # -------------------------------------------------------------------------

    # Valid acquisition modes.
    _acq_modes = {
        "single": 1,
        "accumulate": 2,
        "kinetics": 3,
        "fast kinetics": 4,
        "continuous": 5}

    # Valid trigger modes.
    # There are more that are not implemented here, some of which are
    # only valid on particular camera models.
    _trigger_modes = {
        "internal": 0,
        "external": 1,
        "external start": 6,
        "software": 10}

    def _chk(self, status):
        """Checks the error status of an Andor DLL function call. If
        something catastrophic happened, an AndorError exception is
        raised. In non-critical cases, warnings are given.

        Parameters
        ----------
        status : int
            The return code from an Andor DLL function.

        Raises
        ------
        AndorError
            Whenever something very bad happens. Generally, this
            should hopefully only be whenever the user is trying to do
            something stupid.

        """
        if status == ANDOR_STATUS['DRV_ACQUIRING']:
            self.logger.warn(
                "Action not completed when data acquisition is in progress!")
        elif status == ANDOR_STATUS['DRV_TEMPERATURE_OFF']:
            #self.logger.warn("Temperature control is off.")
            pass
        elif status == ANDOR_STATUS['DRV_TEMPERATURE_NOT_REACHED']:
            self.logger.warn("Temperature set point not yet reached.")
        elif status == ANDOR_STATUS['DRV_TEMPERATURE_DRIFT']:
            self.logger.warn("Temperature is drifting.")
        elif status == ANDOR_STATUS['DRV_TEMP_NOT_STABILIZED']:
            self.logger.warn("Temperature set point reached but not yet stable.")
        elif status == ANDOR_STATUS['DRV_TEMPERATURE_STABILIZED']:
            pass
        elif status == ANDOR_STATUS['DRV_IDLE']:
            stack = tb.extract_stack()
            self.logger.warn(
                'Function call resulted in DRV_IDLE.\n' + \
                ''.join(tb.format_list(stack)))
        elif status != ANDOR_STATUS['DRV_SUCCESS']:
            raise AndorError("Andor returned the status message " + \
                             ANDOR_CODES[status])

    # Setup and shutdown
    # -------------------------------------------------------------------------
    
    def initialize(self, **kwargs):
        """Initialize the Andor camera.

        Keyword arguments
        -----------------
        temperature : int
            Temperature in Celsius to set the TEC to.

        """
        # Get and check keyword arguments.
        temperature = int(kwargs.get('temperature', -50))
        
        # Try to load the Andor DLL
        # TODO: library name in Linux?
        self.clib = ctypes.windll.atmcd32d

        # Initialize the camera and get the detector size
        # TODO: directory to Initialize?
        self._chk(self.clib.Initialize("."))
        xpx, ypx = _int_ptr(), _int_ptr()
        self._chk(self.clib.GetDetector(xpx, ypx))
        self.shape = [xpx.contents.value, ypx.contents.value]
        self.set_crop([1, self.shape[0], 1, self.shape[1]])
        self.set_bins(1)

        # Set default acquisition and trigger modes
        self.set_acquisition_mode('continuous')
        self.set_trigger_mode('software')

        # Enable temperature control
        T_min, T_max = _int_ptr(), _int_ptr()
        self._chk(self.clib.GetTemperatureRange(T_min, T_max))
        self.T_min = T_min.contents.value
        self.T_max = T_max.contents.value
        self.set_cooler_temperature(temperature)
        self.cooler_on()

    def get_camera_properties(self):
        """Code for getting camera properties should go here."""
        # Get generic Andor properties
        self.props.load('props/andor.json')

        # Get camera-specific properties.
        caps = AndorCapabilities()
        caps.ulSize = 12*32
        self._chk(self.clib.GetCapabilities(ctypes.pointer(caps)))

        # Update properties.
        # TODO: actually set things based on the result of GetCapabilities
        new_props = {
            'pixels': self.shape,
            'gain_adjust': True,
            'temp_control': True,
            'shutter': True,
        }
        self.props.update(new_props)

    def close(self):
        """Turn off temperature regulation and safely shutdown the
        camera.

        The Andor SDK guide indicates that for classic and ICCD
        systems, it is best to wait until the temperature is above -20
        degrees C before shutting down, so this will wait until that
        condition is met.

        """
        self.stop()
        self.cooler_off()
        self.close_shutter()
        while True:
            temp = self.get_cooler_temperature()
            if temp > -20:
                break
            else:
                time.sleep(1)
        self._chk(self.clib.ShutDown())

    # Image acquisition
    # -------------------------------------------------------------------------

    def set_acquisition_mode(self, mode):
        """Set the image acquisition mode."""
        if mode not in self._acq_modes:
            raise AndorError(
                "Acquisition mode must be one of " + repr(self._acq_modes))
        self.acq_mode = mode
        if not self.real_camera:
            return
        self.logger.info('Setting acquisition mode to ' + mode)
        self._chk(self.clib.SetAcquisitionMode(
            ctypes.c_int(self._acq_modes[mode])))

        # Have 0 kinetic cycle time for continuous acquisition mode
        if mode == 'continuous':
            self._chk(self.clib.SetKineticCycleTime(0))

    def acquire_image_data(self):
        """Acquire the most recent image data from the camera. This
        will work best in single image acquisition mode.

        """
        # TODO: Check that acquisition was actually started!
        
        # Wait for acquisition to finish
        #print('waiting')
        #self.clib.WaitForAcquisition()
        #print('done waiting')
        while False:
            status = ctypes.c_int(0)
            self.clib.GetStatus(ctypes.pointer(status))
            if ANDOR_CODES[status.value] != 'DRV_SUCCESS':
                print(ANDOR_CODES[status.value])
            else:
                break
            time.sleep(0.1)

        # Allocate image storage
        img_size = self.shape[0]*self.shape[1]/self.bins**2
        c_array = ctypes.c_long*img_size
        c_img = c_array()

        # Trigger or wait for a trigger then acquire data
        if self.trigger_mode == self._trigger_modes['software']:
            self._chk(self.clib.SendSoftwareTrigger())
        self.clib.WaitForAcquisition()
        self._chk(self.clib.GetMostRecentImage(ctypes.pointer(c_img), ctypes.c_ulong(img_size)))
        img_array = np.frombuffer(c_img, dtype=ctypes.c_long)
        img_array.shape = np.array(self.shape)/self.bins
        return img_array

    # Triggering
    # -------------------------------------------------------------------------

    def get_trigger_mode(self):
        """Query the current trigger mode."""

    def set_trigger_mode(self, mode):
        """Setup trigger mode.

        Parameters
        ----------
        mode : str
            Specifies the mode to use and must be one of the (non-case
            sensitive) strings found in self._trigger_modes.

        """
        mode = mode.lower()
        if mode not in self._trigger_modes:
            raise AndorError("Invalid trigger mode: " + mode)
        self.trigger_mode = self._trigger_modes[mode]
        self.logger.info("Setting trigger mode to " + mode)
        if self.real_camera:
            self._chk(self.clib.SetTriggerMode(self.trigger_mode))

    def start(self):
        """Start accepting triggers."""
        if self.real_camera:
            self._chk(self.clib.StartAcquisition())

    def stop(self):
        """Stop acquisition."""
        if self.real_camera:
            self._chk(self.clib.AbortAcquisition())

    # Shutter control
    # -------------------------------------------------------------------------

    def set_shutter(self, state):
        """Open or close the shutter."""
        assert state in ['open', 'closed']
        if state == 'open':
            self._chk(self.clib.SetShutter(1, 1, 20, 20))
        else:
            self._chk(self.clib.SetShutter(1, 2, 20, 20))

    # Gain and exposure time
    # -------------------------------------------------------------------------

    def set_exposure_time(self, t):
        """Set the exposure time in ms."""
        self.t_ms = t
        t_s = self.t_ms/1000.
        self.logger.info('Setting exposure time to %.03f s.' % t_s)
        self._chk(self.clib.SetExposureTime(ctypes.c_float(t_s)))

        exposure = ctypes.c_float()
        accumulate = ctypes.c_float()
        kinetic = ctypes.c_float()
        self.clib.GetAcquisitionTimings(
            ctypes.pointer(exposure),
            ctypes.pointer(accumulate),
            ctypes.pointer(kinetic))
        self.logger.debug(
            'Results of GetAcquisitionTimings:\n' + \
            '\texposure = %.03f\n' % exposure.value + \
            '\taccumulate = %.03f\n' % accumulate.value + \
            '\tkinetic = %.03f' % kinetic.value)

    def get_gain(self):
        """Query the current gain settings."""
        if self.real_camera:
            gain = _int_ptr()
            self._chk(self.clib.GetEMCCDGain(gain))
            return gain.contents.value
        else:
            return 1

    def set_gain(self, gain, **kwargs):
        """Set the camera gain and mode.

        Parameters
        ----------
        gain : float
            Gain for the camera. The acceptable values depend on the
            mode.

        Keyword arguments
        -----------------
        em_gain : bool
            When True, enable EM gain. The gain parameter is then
            setting the gain value for EM gain rather than
            conventional gain.

        Raises
        ------
        ValueError

        """
        em_gain = kwargs.get('em_gain', False)
        if em_gain:
            self._chk(self.clib.SetEMGainMode(0)) # gain is 0-255
            if gain < 0 or gain > 255:
                raise ValueError("gain must be in the range [0, 255].")
            self._chk(self.clib.SetEMCCDGain(ctypes.c_int(gain)))
        else:
            # TODO
            pass

    # Cooling
    # -------------------------------------------------------------------------

    def cooler_on(self):
        """Turn on the TEC."""
        if self.real_camera:
            self._chk(self.clib.CoolerON())

    def cooler_off(self):
        """Turn off the TEC."""
        if self.real_camera:
            self._chk(self.clib.CoolerOFF())

    def get_cooler_temperature(self):
        """Check the TEC temperature."""
        # TODO: make this work better with simulated cameras
        if not self.real_camera:
            return 20
        temp = _int_ptr()
        self._chk(self.clib.GetTemperature(temp))
        return temp.contents.value

    def set_cooler_temperature(self, temp):
        """Set the cooler temperature to temp."""
        # TODO: make this work better with simulated cameras
        self.temperature_set_point = temp
        if not self.real_camera:
            pass
        if temp > self.T_max or temp < self.T_min:
            raise ValueError(
                "Set point temperature must be between " + \
                repr(self.T_min) + " and " + repr(self.T_max) + ".")
        self._chk(self.clib.SetTemperature(temp))

    # Cropping and binning
    # -------------------------------------------------------------------------

    def update_crop(self, crop):
        """Define the portion of the CCD to actually collect data
        from. Using a reduced sensor area typically allows for faster
        readout.

        """
        self.logger.info("Setting new crop to: " + ', '.join([str(x) for x in crop]))
        self._chk(self.clib.SetImage(
            self.bins, self.bins,
            self.crop[0], self.crop[1], self.crop[2], self.crop[3]))

    def set_bins(self, bins):
        """Set binning to bins x bins."""
        self.bins = bins
        self._chk(self.clib.SetImage(
            self.bins, self.bins,
            self.crop[0], self.crop[1], self.crop[2], self.crop[3]))
        
if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    
    with AndorCamera(temperature=10) as cam:
        cam.set_exposure_time(10)
        cam.open_shutter()
        cam.start()
        cam.test_real_time_acquisition()
        # img = cam.get_image()
        # plt.figure()
        # plt.gray()
        # plt.imshow(img, interpolation='none')
        # time.sleep(.2)
        cam.stop()
        cam.close_shutter()
