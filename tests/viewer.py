"""Simple testing of acquiring image data from a camera and displaying
it in a Qt GUI.

"""

from __future__ import print_function

import sys
import numpy as np
sys.path[0:0] = ['..']
from PyQt4 import QtGui, QtCore
from qcamera import Sensicam
from ui_viewer import Ui_MainWindow
from camera_thread import CameraThread

from guiqwt.image import ImageItem
from guiqwt.plot import ImageDialog
from guiqwt.builder import make
from guiqwt.colormap import get_colormap_list

class Viewer(QtGui.QMainWindow, Ui_MainWindow):
    """Simple GUI testbed for qCamera."""
    def __init__(self, camera, thread):
        # Basic initialization.
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.cam = camera
        self.cam_thread = thread
        self.scale = [self.scaleMinBox.value(), self.scaleMaxBox.value()]

        # Add colormaps to the combo box
        self.colormapBox.addItems(get_colormap_list())
        self.colormapBox.setCurrentIndex(51) # jet

        # Image widget signals
        self.cam_thread.image_signal.connect(self.update_image)

        # Exposure and trigger settings signals
        self.exposureTimeBox.editingFinished.connect(self.set_t_exp)
        self.acquisitionButton.clicked.connect(self.toggle_acquisition)
        self.triggerModeBox.currentIndexChanged.connect(self.set_trigger_mode)

        # Crop and bin settings.
        self.binsBox.currentIndexChanged.connect(self.set_bins)

        # Viewing settings
        self.scaleMinBox.editingFinished.connect(self.set_lut_range)
        self.scaleMaxBox.editingFinished.connect(self.set_lut_range)

        # Start the thread.
        self.cam_thread.start()

    @QtCore.pyqtSlot(np.ndarray)
    def update_image(self, img_data):
        """Update the image plot."""
        plot = self.imageWidget.get_plot()
        plot.del_all_items(except_grid=True)
        img = make.image(img_data, colormap=str(self.colormapBox.currentText()))
        img.set_lut_range(self.scale)
        plot.add_item(img)
        plot.set_plot_limits(0, img_data.shape[1], 0, img_data.shape[0])

    def get_image_plot(self):
        """Extract the image plot from the image widget."""
        for item in self.imageWidget.get_plot().get_items():
            img = item
            if isinstance(item, ImageItem):
                break
        return img
        
    def set_lut_range(self):
        """Change the LUT range."""
        self.scale = [self.scaleMinBox.value(), self.scaleMaxBox.value()]
        img = self.get_image_plot()
        img.set_lut_range(self.scale)

    def toggle_acquisition(self):
        """Toggle between acquisition states (on or off)."""
        start_text = "Begin Acquisition"
        stop_text = "Stop Acquisition"
        if self.acquisitionButton.text() == start_text:
            self.cam_thread.queue.put('unpause')
            self.acquisitionButton.setText(stop_text)
            self.cropGroupBox.setEnabled(False)
        else:
            self.cam_thread.queue.put('pause')
            self.acquisitionButton.setText(start_text)
            self.cropGroupBox.setEnabled(True)

    def set_trigger_mode(self):
        """Change the camera's triggering mode."""
        self.cam_thread.queue.put('pause')
        mode = self.triggerModeBox.currentIndex()
        self.cam.set_trigger_mode(mode)

    def set_t_exp(self):
        """Change the exposure time."""
        self.cam_thread.queue.put('pause')
        t = self.exposureTimeBox.value()
        self.cam.set_exposure_time(t)

    def set_bins(self):
        """Change the camera's binning."""
        self.cam_thread.queue.put('pause')
        self.cam.set_bins(2**self.binsBox.currentIndex())

if __name__ == "__main__":
    # TODO: Allow for using this with other cameras (either
    #       command-line option, display a dialog to select a camera
    #       at startup, or select camera in a menu).
    import logging
    logging.basicConfig(level=logging.DEBUG)
    app = QtGui.QApplication(sys.argv)
    with Sensicam(real=True) as cam:
        thread = CameraThread(cam)
        win = Viewer(cam, thread)
        win.show()
        sys.exit(app.exec_())
    