"""Image mapping for use with Qt GUIs."""

import numpy as np
from matplotlib import cm
from PyQt4 import QtGui

class ImageMapper(object):
    """Maps image data to 8 bit colormapped QtPixmap images."""
    def __init__(self, min_=0, max_=1000, color_map='jet'):
        """Create a new ImageMapper.

        Parameters
        ----------
        min_ : int
            The minimum pixel value for the scaled pixmap.
        max_ : int
            The maximum pixel value for the scaled pixmap.
        color_map : str
            Color map key string to use.

        """
        assert isinstance(min_, int)
        assert isinstance(max_, int)
        assert color_map in cm.cmap_d
        self.min_px = min_
        self.max_px = max_
        self.color_map = cm.cmap_d[color_map]

    def map_image(self, raw_data):
        """Map raw image data to a QImage for use with a GUI.

        Parameters
        ----------
        raw_data : np.ndarray
            A numpy array containing raw image data.

        """
        assert isinstance(raw_data, np.ndarray)
        assert len(raw_data.shape) is 2

        # Coerce data to upper and lower thresholds.
        data = raw_data.copy()
        data[data > self.max_px] = self.max_px
        data[data < self.min_px] = self.min_px

        # Scale data to 8 bits
        data = 255*(data - self.min_px)/float(self.max_px - self.min_px)
        data = data.astype(np.uint8)

        # Convert to a Qt pixmap.
        h, w = data.shape
        pixmap = QtGui.QImage(data.data, w, h, QtGui.QImage.Format_Indexed8)
        pixmap.setColorTable(self.color_map(np.arange(256)))
        #pixmap = QtGui.QPixmap.fromImage(pixmap)
        return pixmap
