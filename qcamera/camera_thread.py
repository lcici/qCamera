"""Threading for camera live feeds"""

import time
import logging
import threading
import numpy as np
from camera import Camera

class CameraThread(threading.Thread):
    """Thread class for producing live feed images from a camera.

    Attributes
    ----------
    running : bool
        True when the thread is running.
    abort : bool
        Set to True when stopping of the thread is requested.
    transmitters : list
        A list of functions used for transmitting QPixmaps and raw
        image data for GUI integration. See :func:`add_transmitter`
        for details.
    logger : Logger
        A Logger object for logging any important output from the
        thread.

    """

    running = False
    abort = False
    transmitters = []
    
    def __init__(self, cam, **kwargs):
        """Initialize the camera thread.

        Parameters
        ----------
        camera : Camera
            A camera instance for acquiring images.

        Keyword arguments
        -----------------
        logger : str
            Logger to use.

        """
        # Get and check kwargs.
        logger = kwargs.get('logger', 'Camera')
        assert isinstance(cam, Camera)
        assert isinstance(logger, str)

        # Initialize thread.
        self.cam = cam
        self.logger = logging.getLogger(logger)
        super(CameraThread, self).__init__()

    def stop(self):
        """Stop the thread."""
        self.abort = True
        while self.running:
            time.sleep(0.01)

    def run(self):
        """Run the thread until receiving a stop request. It is up to
        the user to properly setup acquisition and triggering modes
        prior to running the thread!

        """
        while not self.abort:
            try:
                image = self.cam.get_image()
                self.transmit_pixmap(image)
            except:
                # TODO: DTRT, have exception in case camera is busy
                # changing settings or whatever
                print('exception')
                time.sleep(0.01)

    def add_transmitter(self, function):
        """Add a transmitter function to the list of transmitters.

        Parameters
        ----------
        function : callable
            A Python callable accepting two arguments: a QPixmap and a
            :mod:`numpy` array containing the raw image data, i.e.,
            ``function(q_pixmap, img_array)``.

        """
        assert callable(function)
        self.transmitters.append(function)

    def transmit_pixmap(self, image):
        """Create and transmit the pixmap for use in a GUI. See
        :func:`add_transmitter` for a description of valid transmitter
        functions.

        """
        assert isinstance(image, np.ndarray)
        pixmap = image # TODO: get from image mapper

        for transmitter in self.transmitters:
            transmitter(pixmap, image)
            