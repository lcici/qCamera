"""Simple testing of acquiring image data from a camera and displaying
it in a Qt GUI.

"""

from __future__ import print_function

import time
import sys
sys.path[0:0] = ['..']
from PyQt4 import QtGui
from qcamera import Sensicam
from qcamera.camera_thread import CameraThread

from guiqwt.image import ImageItem
from guiqwt.plot import ImageDialog
from guiqwt.builder import make

class Window(QtGui.QWidget):
    def __init__(self, cam):
        super(Window, self).__init__()
        self.cam = cam
        self.init_ui()

    def init_ui(self):
        """Initialize all the Qt UI components."""
        # Image plotting
        self.img = ImageDialog(edit=False, toolbar=False)
        self.img.resize(640, 480)
        plot = self.img.get_plot()
        plot.set_aspect_ratio(640/480., lock=True)

        # Image settings
        # --------------

        # Exposure time
        self.sbExpTime = QtGui.QSpinBox()
        self.sbExpTime.setRange(10, 10000)
        self.sbExpTime.setValue(100)
        self.sbExpTime.setSingleStep(100)
        self.sbExpTime.setToolTip('Exposure time in ms.')
        self.sbExpTime.valueChanged.connect(self.set_t_exp)

        # Minimum and maximum threshold values for image mapping
        self.sbThresholdMin = QtGui.QSpinBox()
        self.sbThresholdMin.setRange(0, 2**12)
        self.sbThresholdMin.setValue(0)
        self.sbThresholdMin.setSingleStep(10)
        self.sbThresholdMin.valueChanged.connect(self.set_lut_range)
        
        self.sbThresholdMax = QtGui.QSpinBox()
        self.sbThresholdMax.setRange(0, 2**12)
        self.sbThresholdMax.setValue(500)
        self.sbThresholdMax.setSingleStep(10)
        self.sbThresholdMax.valueChanged.connect(self.set_lut_range)

        # Image acquisition controls
        # --------------------------

        # Take a single picture
        self.bTakePicture = QtGui.QPushButton()
        self.bTakePicture.setText('Take Picture')
        self.bTakePicture.setToolTip(
            'Take a single image.')
        self.bTakePicture.clicked.connect(self.take_picture)

        # Start continuous acquisition
        self.bStartContinuous = QtGui.QPushButton()
        self.bStartContinuous.setText('Start continuous acquisition')
        self.bStartContinuous.setToolTip(
            'Begin continous, real time acquisition.')
        self.bStartContinuous.setDisabled(True)

        # Stop continuous acquisition
        self.bStopContinuous = QtGui.QPushButton()
        self.bStopContinuous.setText('Stop continuous acquisition')
        self.bStopContinuous.setDisabled(True)

        # GUI Layout
        # ----------

        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.img)
        
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(QtGui.QLabel('t:'))
        hbox.addWidget(self.sbExpTime)
        hbox.addWidget(QtGui.QLabel('Min:'))
        hbox.addWidget(self.sbThresholdMin)
        hbox.addWidget(QtGui.QLabel('Max:'))
        hbox.addWidget(self.sbThresholdMax)
        vbox.addLayout(hbox)

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.bTakePicture)
        hbox.addWidget(self.bStartContinuous)
        hbox.addWidget(self.bStopContinuous)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.setWindowTitle('qCamera Qt Test')
        self.show()

    def take_picture(self):
        """Take a single image."""
        img_data = self.cam.get_image()
        plot = self.img.get_plot()
        plot.del_all_items(except_grid=True)
        img = make.image(img_data, colormap='Spectral')
        img.set_lut_range((self.sbThresholdMin.value(), self.sbThresholdMax.value()))
        plot.add_item(img)
        plot.set_plot_limits(0, img_data.shape[1], 0, img_data.shape[0])

    def set_t_exp(self):
        """Change the exposure time."""
        t = self.sbExpTime.value()
        self.cam.set_exposure_time(t)

    def set_lut_range(self):
        """Change the LUT maximum value."""
        for item in self.img.get_plot().get_items():
            img = item
            if isinstance(item, ImageItem):
                break
        img.set_lut_range(
            (self.sbThresholdMin.value(), self.sbThresholdMax.value()))

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    app = QtGui.QApplication(sys.argv)
    with Sensicam(real=True) as cam:
        win = Window(cam)
        sys.exit(app.exec_())
    