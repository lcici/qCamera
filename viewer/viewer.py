"""Simple testing of acquiring image data from a camera and displaying
it in a Qt GUI.

"""

from __future__ import print_function
import sys

# Ensure we're loading the newest version of qcamera rather than
# anything that was installed with distutils.
sys.path.insert(0, '..')

import numpy as np

try:
    from PyQt4 import QtGui, QtCore
except ImportError:
    from PySide import QtGui, QtCore
from guiqwt.image import ImageItem
from guiqwt.annotations import AnnotatedRectangle
from guiqwt.builder import make
from guiqwt.colormap import get_colormap_list

from setup_dialog import SetupDialog
from roi_dialog import ROIDialog
from camera_select_dialog import CameraSelectDialog
from config import CAM_TYPES, CONFIG_FILE
from util import *

from ui_viewer import Ui_MainWindow
from camera_thread import CameraThread

# Viewer
# =============================================================================

class Viewer(QtGui.QMainWindow, Ui_MainWindow):
    """Simple GUI testbed for qCamera."""

    # Setup and shutdown
    # -------------------------------------------------------------------------
    
    def __init__(self, config, **kwargs):
        # UI initialization
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.config = config

        # Run the camera select dialog if necessary
        if kwargs.get('cam_select', False):
            self.launch_camera_select_dialog()
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f, sort_keys=True, indent=4)
        self.show()

        # Open the camera and create a camera thread
        Camera = CAM_TYPES[self.config['camera_type']]
        self.cam = Camera(real=self.config['real'], recording=self.config['recording'])
        self.cam_thread = CameraThread(self.cam)
        #self.cam.rbuffer.recording = not self.rbufferBox.checkState()

        # Basic UI configuration
        self.scale = [self.scaleMinBox.value(), self.scaleMaxBox.value()]
        self.colormapBox.addItems(get_colormap_list())
        self.colormapBox.setCurrentIndex(51) # jet
        self.colormapBox.currentIndexChanged.connect(self.update_colormap)

        # Connect image signals
        self.cam_thread.image_signal.connect(self.update)

        # Exposure time signals
        self.set_t_exp()
        self.exposureTimeBox.editingFinished.connect(self.set_t_exp)
        self.exposureTimeBox.valueChanged.connect(self.set_t_exp)
        #self.acquisitionButton.clicked.connect(self.toggle_acquisition)
        #self.triggerModeBox.currentIndexChanged.connect(self.set_trigger_mode)

        # Viewing settings
        self.scaleMinBox.valueChanged.connect(self.set_lut_range)
        self.scaleMaxBox.valueChanged.connect(self.set_lut_range)
        self.rescaleButton.clicked.connect(self.rescale)
        self.rotateImageButton.clicked.connect(self.rotate_image)
        #self.rbufferBox.stateChanged.connect(self.set_rbuffer_recording)

        # Dialogs
        self.adjustROIButton.clicked.connect(self.launch_roi_dialog)
        self.cameraSettingsButton.clicked.connect(self.launch_setup_dialog)

        # Start the thread.
        self.acquisitionButton.clicked.connect(self.toggle_acquisition)
        self.cam_thread.start()
        self.toggle_acquisition()

    def closeEvent(self, event):
        self.cam_thread.stop()
        self.cam.close()
        super(Viewer, self).closeEvent(event)

    # Utility functions
    # -------------------------------------------------------------------------

    def _get_rect(self, rect_tool):
        """Convert the guiqwt AnnotatedRectangleTool shape format to
        what qCamera wants.

        For some ridiculous reason, the rect shape the get_rect
        function returns depends on which corner you drag from. In
        other words, it always returns [x1, y1, x2, y2] where [x1, y1]
        is the first corner you started from and [x2, y2] is the last
        corner.

        """
        rect = rect_tool.get_last_final_shape().get_rect()
        rect = [int(x) for x in rect]
        rect[1], rect[2] = rect[2], rect[1]
        if rect[0] > rect[1]:
            rect[0], rect[1] = rect[1], rect[0]
        if rect[2] > rect[3]:
            rect[2], rect[3] = rect[3], rect[2]
        return rect

    def _make_image_item(self, data):
        return make.image(data, colormap=str(self.colormapBox.currentText()))

    # Slots
    # -------------------------------------------------------------------------

    def update(self, img_data):
        """Update the image plot and other information."""
        plot = self.imageWidget.get_plot()
        img = get_image_item(self.imageWidget)
        roi_rect = get_rect_item(self.imageWidget)
        if img is None:
            img = self._make_image_item(img_data)
            plot.add_item(img)
        else:
            img.set_data(img_data)
        #img.select()
        #plot.replot()
            
        # Display ROI if requested.
        roi_x1, roi_x2, roi_y1, roi_y2 = self.cam.roi
        if self.showROIBox.isChecked():
            if roi_rect is None:
                roi_rect = make.annotated_rectangle(
                    roi_x1, roi_x2, roi_y1, roi_y2)
                roi_rect.set_resizable(False)
                roi_rect.set_selectable(False)
                plot.add_item(roi_rect)
            else:
                roi_rect.set_rect(roi_x1, roi_y1, roi_x2, roi_y2)
        else:
            if roi_rect is not None:
                plot.del_item(roi_rect)

        # Update plot
        if self.autoscaleButton.isChecked():
            self.rescale()
        self.set_lut_range()
        plot.set_plot_limits(0, img_data.shape[1], 0, img_data.shape[0])
        plot.set_aspect_ratio(img_data.shape[0]/img_data.shape[1], lock=True)
        plot.replot()
                    
    def update_colormap(self):
        image = get_image_item(self.imageWidget)
        image.set_color_map(str(self.colormapBox.currentText()))
        
    def set_lut_range(self):
        """Change the LUT range."""
        self.scale = [self.scaleMinBox.value(), self.scaleMaxBox.value()]
        img = get_image_item(self.imageWidget)
        img.set_lut_range(self.scale)
        self.update_colormap()

    def rescale(self):
        """Change the LUT range to the have min and max values the
        same as the image data.

        """
        img = get_image_item(self.imageWidget)
        minimum = int(np.min(img.data))
        maximum = int(np.max(img.data))
        assert type(minimum) is int
        assert type(maximum) is int
        self.scaleMinBox.setValue(minimum)
        self.scaleMaxBox.setValue(maximum)
        self.set_lut_range()

    def rotate_image(self):
        """Rotate the image 90 degrees upon presing."""
        print("Rotating not yet implemented!")

    def toggle_acquisition(self):
        """Toggle between acquisition states (on or off)."""
        start_text = "Begin acquisition"
        stop_text = "Stop acquisition"
        if self.acquisitionButton.text() == start_text:
            self.cam_thread.unpause()
            self.acquisitionButton.setText(stop_text)
        else:
            self.cam_thread.pause()
            self.acquisitionButton.setText(start_text)

    def set_t_exp(self):
        """Change the exposure time."""
        t = self.exposureTimeBox.value()
        self.cam.set_exposure_time(t)

    # Dialogs
    # -------------------------------------------------------------------------

    def launch_roi_dialog(self):
        roiDialog = ROIDialog(self.cam, self.cam_thread)
        roiDialog.exec_()

    def launch_setup_dialog(self):
        self.cam_thread.pause()
        setupDialog = SetupDialog(self.cam)
        setupDialog.exec_()
        self.cam_thread.unpause()

    def launch_camera_select_dialog(self):
        selectDialog = CameraSelectDialog(self.config)
        selectDialog.exec_()
        if not selectDialog.quit:
            self.config.update(selectDialog.config)
        else:
            sys.exit(0)
        
# Main
# =============================================================================

if __name__ == "__main__":

    # Basic setup
    # -------------------------------------------------------------------------

    import os
    import argparse
    import json
    import logging

    logging.basicConfig(level=logging.DEBUG)

    # Argument parsing
    # -------------------------------------------------------------------------
        
    parser = argparse.ArgumentParser(description='qCamera Viewer')
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-c', '--camera-type', metavar='<camera type>', type=str,
        help='Specify the camera type to use. If not given, ' + \
        'default to the last camera type used. Options include:\n' + \
        cam_options_string()
    )
    group.add_argument(
        '-s', '--camera-select', action='store_true',
        help="Run the camera select dialog."
    )
    args = parser.parse_args()

    # Configuration
    # -------------------------------------------------------------------------

    # Basic config file structure
    config = {
        'camera_type': '',    # Must be one of the keys in cam_options
        'real': True,         # Real or simulated camera?
        'recording': False,   # Use the ring buffer if set to True
        'props_file': None,   # A custom camera properties JSON file if not None
    }

    # Determine camera type if possible
    cam_select = False
    if args.camera_type is None:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config.update(json.load(f))
        else:
            cam_select = True
    else:
        assert args.camera_type in CAM_TYPES
        config['camera_type'] = args.camera_type
    if args.camera_select:
        cam_select = args.camera_select

    # Main application
    # -------------------------------------------------------------------------

    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName("IonTrap Group")
    app.setApplicationName("qCamera viewer")
    app.setStyle("cleanlooks")
    app.setWindowIcon(QtGui.QIcon('icon.png'))
    try:
        import ctypes
        myappid = 'qCamera_viewer'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except:
        pass

    win = Viewer(config, cam_select=cam_select)
    sys.exit(app.exec_())
    