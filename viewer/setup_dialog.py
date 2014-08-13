"""Camera setup dialog"""

import sys
sys.path.insert(0, '..')
import math
from qcamera import Camera

from PyQt4 import QtGui, QtCore
from ui_setup_dialog import Ui_SetupDialog

class SetupDialog(QtGui.QDialog, Ui_SetupDialog):
    """Class controlling the camera setup dialog."""
    def __init__(self, cam):
        QtGui.QWidget.__init__(self)
        assert isinstance(cam, Camera)
        self.cam = cam

        # Setup UI
        self.setupUi(self)
        self.show()
        self.closeButton.clicked.connect(self.done)

        # Binning
        bin_options = [str(x) for x in self.cam.props['bins']]
        print self.cam.get_bins()
        bin_idx = int(math.log(self.cam.get_bins(), 2))
        self.binsBox.addItems(bin_options)
        self.binsBox.setCurrentIndex(bin_idx)
        self.binsBox.currentIndexChanged.connect(self.set_bins)

        # Shutter
        if not self.cam.props['shutter']:
            self.shutterGroupBox.setEnabled(False)
        elif not self.cam.shutter_open:
            self.closeShutterButton.setChecked(True)
        self.openShutterButton.clicked.connect(self.cam.open_shutter)
        self.closeShutterButton.clicked.connect(self.cam.close_shutter)

        # Cropping
        #self.adjustCropButton.clicked.connect(self.crop_setup_dialog)

        # Gain
        if not self.cam.props['gain_adjust']:
            self.gainGroupBox.setEnabled(False)
        else:
            grange = self.cam.props['gain_range']
            self.gainSlider.setRange(grange[0], grange[1])
            self.gainSlider.setValue(self.cam.gain)
            self.gainLbl.setNum(self.cam.gain)
        self.gainSlider.sliderReleased.connect(self.set_gain)

        # Temperature
        if not self.cam.props['temp_control']:
            self.tempGroupBox.setEnabled(False)
        else:
            trange = self.cam.props['temp_range']
            self.tempSetPointBox.setRange(trange[0], trange[1])
            self.tempSetPointBox.setValue(self.cam.temperature_set_point)
            self.tempSetPointBox.editingFinished.connect(self.set_temperature)
            if self.cam.cooler_active:
                self.coolerOnButton.setChecked(True)
            else:
                self.coolerOffButton.setChecked(True)
            self.coolerOnButton.clicked.connect(self.cam.cooler_on)
            self.coolerOffButton.clicked.connect(self.cam.cooler_off)

            # Setup a timer to poll the temperature
            self.temp_checker = QtCore.QTimer()
            self.temp_checker.setInterval(1000)
            self.temp_checker.timeout.connect(self.check_temperature)
            self.temp_checker.start()

    def set_trigger_mode(self):
        """Change the camera's triggering mode."""
        # TODO: fix thread stuff
        self.cam_thread.queue.put('pause')
        mode = self.triggerModeBox.currentIndex()
        self.cam.set_trigger_mode(mode)

    def set_bins(self):
        self.cam.set_bins(int(self.binsBox.currentText()))

    def open_shutter(self):
        self.cam.open_shutter()

    def close_shutter(self):
        self.cam.close_shutter()

    def set_gain(self):
        self.cam.set_gain(self.gainSlider.value())

    def check_temperature(self):
        temp = self.cam.get_cooler_temperature()
        self.tempLbl.setText('%i' % temp)

    def set_temperature(self):
        temp = self.tempSetPointBox.value()
        self.cam.set_cooler_temperature(temp)
