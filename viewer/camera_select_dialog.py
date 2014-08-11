"""Camera selection dialog"""

from PyQt4 import QtGui
from config import CAM_TYPES
from ui_camera_select_dialog import Ui_CameraSelectDialog

class CameraSelectDialog(QtGui.QDialog, Ui_CameraSelectDialog):
    def __init__(self, config):
        QtGui.QWidget.__init__(self)
        self.quit = False
        self.config = config

        # Basic UI setup
        self.setupUi(self)
        self.show()
        self.quitButton.clicked.connect(self._abort)
        self.okButton.clicked.connect(self._ok)

        # Populate the camera type combo box
        self.cameraTypeBox.addItems(CAM_TYPES.keys())

    def _abort(self):
        """What to do on pressing the quit button."""
        self.quit = True
        self.done(0)

    def _ok(self):
        """What to do on pressing the OK button."""
        self.config['camera_type'] = str(self.cameraTypeBox.currentText())
        self.config['real'] = bool(self.realCameraBox.checkState())
        self.config['recording'] = bool(self.useRingBufferBox.checkState())
        self.config['props_file'] = str(self.propsFileEdit.text())
        self.done(0)
        
