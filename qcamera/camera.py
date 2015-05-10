"""Base camera module

This file contains the class definition for the Camera class on which
all subsequent cameras should be based on.

"""

from __future__ import print_function, division

from abc import ABCMeta, abstractmethod
import logging
import time

import numpy as np
import numpy.random as npr

import log
from .ring_buffer import RingBuffer
from .camprops import CameraProperties
from .exceptions import CameraError

class DummyDLL(object):
    """Fake library reference. This will return a default value for
    any 'function' call.

    """
    def __init__(self, success):
        assert isinstance(success, int)
        self.success = success

    def __getattr__(self, name):
        setattr(self, name, lambda *args: self.success)
        return self.name

class Camera:
    """Base class for all cameras.

    TODO: Verify that this documentation is up to date!

    Attributes
    ----------
    clib : WinDLL or CDLL or DummyDLL
        A ctypes library reference or a fake one for simulating a
        camera.
    roi : list
        The defined region of interest in the form [x1, y1, x2, y2].
    t_ms : float
        Exposure time in ms.
    gain : int or float
        Gain setting. The type is dependent on the camera used.
    shape : tuple
        Number of pixels (x, y)
    bins : int
        Bin size to use.
    crop : list
        Crop specifications. Should be of the form::
            [horiz start, horiz end, vert start, vert end]
    
        with indeces starting from 1.
    shutter_open : bool
        For cameras that are equipped with an integrated shutter: is the
        shutter open?
    cooler_active : bool
        True if the cooler is on.
    temperature_set_point : int
        Temperature set point for the cooler if present.
    acq_mode : str
        Camera acquisition mode.
    trigger_mode : int
        Camera triggering mode. These are obviously defined
        differently depending on the particular camera's SDK.
    rbuffer : RingBuffer
        The RingBuffer object for autosaving of images.
    real_camera : bool
        When set to False, the camera hardware can be simulated for working in
        offline mode.
    props : CameraProperties
        A CameraProperties object defining several generic settings of
        the camera as well as flags indicating if certain
        functionality is available.

    """
    __metaclass__ = ABCMeta

    # Attributes
    # -------------------------------------------------------------------------

    clib = None
    roi = [1, 10, 1, 10]
    t_ms = 100.
    gain = 0
    shape = (512, 512)
    bins = 1
    crop = (1, shape[0], 1, shape[1])
    shutter_open = False
    cooler_active = False
    temperature_set_point = 0
    acq_mode = "single"
    trigger_mode = 0
    rbuffer = None
    real_camera = True
    props = CameraProperties()

    # Setup and shutdown
    # -------------------------------------------------------------------------

    def __init__(self, **kwargs):
        """Initialize a camera. Additional keyword arguments may also
        be passed and checked for the initialize function to be
        defined by child classes.

        Keyword arguments
        -----------------
        bins : int
            Binning to use.
        real : bool
            If True, the camera is real; otherwise it is
            simulated. Default: True.
        buffer_dir : str
            Directory to store the ring buffer file to. Default:
            '.'.
        log_level : int
            Logging level to use. Default: ``logging.INFO``.
        success_value : int
            Success value to give to the DummyDLL class.

        """
        # Get kwargs and set defaults
        bins = kwargs.get('bins', 1)
        real = kwargs.get('real', True)
        buffer_dir = kwargs.get('buffer_dir', '.')
        recording = kwargs.get('recording', True)
        success_value = kwargs.get('success_value', 0)
        
        # Check kwarg types are correct
        assert isinstance(bins, int)
        assert isinstance(real, (bool, int))
        assert isinstance(buffer_dir, str)

        # Configure logging
        log_level = kwargs.get('log_level', logging.INFO)
        self.logger = log.logger
        if len(self.logger.handlers) == 0:
            log.stream_handler.setLevel(log_level)
            self.logger.addHandler(log.stream_handler)
            self.logger.setLevel(log_level)
        self.logger.info(
            "Connecting to %s camera" % ("real" if real else "simulated"))

        # Initialize
        self.real_camera = real
        self.rbuffer = RingBuffer(directory=buffer_dir, recording=recording, roi=self.roi)
        x0 = npr.randint(self.shape[0]/4, self.shape[0]/2)
        y0 = npr.randint(self.shape[1]/4, self.shape[1]/2)
        self.sim_img_center = (x0, y0)
        if self.real_camera:
            self._initialize(**kwargs)
        else:
            self.clib = DummyDLL(success_value)
        self.get_camera_properties()
        self.logger.debug(self.props)

    def _initialize(self, **kwargs):
        """Any extra initialization required should be placed in this
        function for child camera classes.

        """
        if self.real_camera:
            self.logger.warn("_initialize not implemented.")

    def get_camera_properties(self):
        """Code for getting camera properties should go here."""
        self.logger.warn(
            "Properties not being set. " + \
            "Did you forget to override get_camera_properties?")

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        self.logger.info("Shutting down camera.")
        self.rbuffer.close()
        self.close()

    @abstractmethod
    def close(self):
        """Close the camera safely. Anything necessary for doing so
        should be defined here.

        """
        
    # Image acquisition
    # -------------------------------------------------------------------------

    @abstractmethod
    def set_acquisition_mode(self, mode):
        """Set the image acquisition mode."""

    def get_image(self):
        """Acquire the current image from the camera and write it to
        the ring buffer. This function should *not* be overwritten by
        child classes. Instead, everything necessary to acquire an
        image from the camera should be added to the
        :meth:`_acquire_image_data` method.

        """
        if not self.real_camera:
            x0, y0 = self.sim_img_center
            img = self._get_simulated_image(x0, y0)
        else:
            img = self._acquire_image_data()
        self.rbuffer.write(img)
        return img

    def _acquire_image_data(self):
        """Code for getting image data from the camera should be
        placed here. This must return a numpy array.

        """
        raise NotImplementedError("You must define this method.")

    def _get_simulated_image(self, x0, y0):
        """Generate and return a simulated image centered at the point
        (x0, y0). This is primarily useful when testing out a full
        control program so that there is a simulated camera with an
        image to actually use.

        """
        g = lambda x, y, x0, y0, sigma: \
            np.exp(-((x - x0)**2 + (y - y0)**2)/(2*sigma**2))
        x = np.arange(0, self.shape[0])
        y = np.arange(0, self.shape[1])
        X, Y = np.meshgrid(x, y)
        img = g(X, Y, x0, y0, 20)
        img = self.t_ms*img/np.max(img)
        img += self.t_ms*0.25*npr.random(self.shape)
        wait_time = max(self.t_ms/1000., 0.05)
        time.sleep(wait_time)
        return img
        
    # Triggering
    # -------------------------------------------------------------------------

    @abstractmethod
    def get_trigger_mode(self):
        """Query the current trigger mode."""

    @abstractmethod
    def set_trigger_mode(self, mode):
        """Setup trigger mode."""

    @abstractmethod
    def start(self):
        """Code needed for getting the camera to begin triggering
        should be placed here.

        """

    @abstractmethod
    def stop(self):
        """Code needed to stop accepting triggering should be placed
        here.

        """
        
    # Shutter control
    # -------------------------------------------------------------------------

    # Not all cameras have builtin shutters, so these functions should
    # have no actual effect in that case. Child classes should
    # override the _set_shutter function to set the shutter state.

    def open_shutter(self):
        """Open the shutter."""
        self.shutter_open = True
        self.logger.info('Opening shutter.')
        if self.real_camera:
            self._set_shutter('open')
        
    def close_shutter(self):
        """Close the shutter."""
        self.shutter_open = False
        self.logger.info('Closing shutter.')
        if self.real_camera:
            self._set_shutter('closed')

    def _set_shutter(self, state):
        """This will set the shutter to the given state ('open' or
        'closed'). Since not all cameras have a built in shutter, this
        will simply do nothing if not overridden.

        """
        self.logger.warn("No shutter action taken (_set_shutter not overridden).")
        
    def toggle_shutter(self, state):
        """Toggle the shutter state from open to closed and vice versa."""
        if self.shutter_open:
            self.close_shutter()
        else:
            self.open_shutter()

    # Gain and exposure time
    # -------------------------------------------------------------------------

    def get_exposure_time(self):
        """Query for the current exposure time. Default is to just
        return what is stored in the instantiation.

        """
        return self.t_ms

    def set_exposure_time(self, t):
        """Set the exposure time."""
        self.t_ms = t
        if self.real_camera:
            self._update_exposure_time(t)

    @abstractmethod
    def _update_exposure_time(self, t):
        """Camera-specific code for setting the exposure time should
        go here.

        """

    @abstractmethod
    def get_gain(self):
        """Query the current gain settings."""

    @abstractmethod
    def set_gain(self, **kwargs):
        """Set the camera gain."""

    # Cooling
    # -------------------------------------------------------------------------

    # TODO: change it so that implementations don't have to manually
    #       set the cooler_active attribute.

    def cooler_on(self):
        """Turn on the TEC."""
        self.logger.warn("No action: cooler_on not overriden.")

    def cooler_off(self):
        """Turn off the TEC."""
        self.logger.warn("No action: cooler_off not overriden.")

    def get_cooler_temperature(self):
        """Check the TEC temperature."""
        self.logger.warn("No action: get_cooler_temperature not overriden.")

    def set_cooler_temperature(self, temp):
        """Set the cooler temperature to temp."""
        self.logger.warn("No action: set_cooler_temperature not overriden.")
        raise NotImplementedError("No cooler?")

    # ROI, cropping, and binning
    # -------------------------------------------------------------------------

    def set_roi(self, roi):
        """Define the region of interest. Since ROI stuff is handled
        entirely in software, this function does not need to be
        implemented in inheriting classes.

        """
        if len(roi) != 4:
            raise CameraError("roi must be a length 4 list.")
        if roi[0] >= roi[2] or roi[1] >= roi[3] or roi[0] < 0 or roi[1] < 0:
            self.logger.error(
                'Invalid ROI: {0}. Keeping old ROI.'.format(roi))
            return
        old = self.roi
        self.roi = roi
        self.rbuffer.roi = roi
        self.logger.info(
            'Adjusting ROI: {0} --> {1}'.format(str(old), str(self.roi)))
        
    def get_crop(self):
        """Get the current CCD crop settings. If this function is not
        overloaded, it will simply return the value stored in the crop
        attribute.

        """
        return self.crop

    def set_crop(self, crop):
        """Define the portion of the CCD to actually collect data
        from. Using a reduced sensor area typically allows for faster
        readout. Derived classes should define :meth:`_update_crop`
        instead of overriding this one.

        """
        assert crop[1] > crop[0]
        assert crop[3] > crop[2]
        if len(crop) != 4:
            raise CameraError("crop must be a length 4 array.")
        self.crop = crop
        if self.real_camera:
            self._update_crop(self.crop)

    def reset_crop(self):
        """Reset the crop to the maximum size."""
        self.crop = [1, self.shape[0], 1, self.shape[1]]
        self._update_crop(self.crop)

    def _update_crop(self, crop):
        """Camera-specific code for setting the crop should go
        here.

        """
        self.logger.warn("_update_crop not implemented.")
        
    def get_bins(self):
        """Query the current binning. If this function is not
        overloaded, it will simply return the value stored in the bins
        attribute.

        """
        return self.bins

    def set_bins(self, bins):
        """Set binning to bins x bins."""
        self.logger.warn("set_bins not implemented.")

    # Standard tests
    # -------------------------------------------------------------------------

    def test_real_time_acquisition(self, max_exposures=1000):
        """Test real time acquisition.

        Parameters
        ----------
        max_exposures : int
            Maximum number of exposures to take for the real time
            test.

        """
        import matplotlib.pyplot as plt
        try:
            for i in range(max_exposures):
                img = self.get_image()
                if i == 0:
                    p = plt.imshow(img, interpolation='none')
                    plt.clim()
                else:
                    p.set_data(img)
                    plt.pause(0.0001)
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    class Test(Camera):
        pass
    with Test(real=False) as cam:
        pass
    #plt.imshow(cam.get_simulated_image(x0, y0))
    #plt.colorbar()
    #plt.show()
