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
from guiqwt.builder import make
from guiqwt.colormap import get_colormap_list
from guiqwt.plot import ImageDialog
from guiqwt.tools import SelectTool, RectangleTool

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

        # Rotation and mirroring of the image.
        self.rotation = 0
        self.mirror = [False, False]

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
        
        # Connect image signal
        self.cam_thread.image_signal.connect(self.update)

        # Setup the rest of the GUI
        self._setup_scale_widgets()
        self._setup_exposure_widgets()
        self._setup_transform_buttons()
        self._setup_statusbar()
        self._setup_dialogs()

        # Start the thread.
        self.acquisitionButton.clicked.connect(self.toggle_acquisition)
        self.cam_thread.start()
        self.toggle_acquisition()

    def _setup_scale_widgets(self):
        self.scale = [self.scaleMinBox.value(), self.scaleMaxBox.value()]
        self.colormapBox.addItems(get_colormap_list())
        self.colormapBox.setCurrentIndex(51) # jet
        self.colormapBox.currentIndexChanged.connect(self.update_colormap)
        self.scaleMinBox.valueChanged.connect(self.set_lut_range)
        self.scaleMaxBox.valueChanged.connect(self.set_lut_range)
        self.rescaleButton.clicked.connect(self.rescale)

    def _setup_exposure_widgets(self):
        self.set_t_exp()
        self.exposureTimeBox.editingFinished.connect(self.set_t_exp)
        self.exposureTimeBox.valueChanged.connect(self.set_t_exp)        

    def _setup_transform_buttons(self):
        def rotate_cw():
            print(self.cam.roi)
            self.rotation = (self.rotation + 1) % 4

        def rotate_ccw():
            self.rotation = (self.rotation - 1) % 4

        def flip_vertical():
            self.mirror[0] = not self.mirror[0]

        def flip_horizontal():
            self.mirror[1] = not self.mirror[1]

        self.rotateCWButton.clicked.connect(rotate_cw)
        self.rotateCCWButton.clicked.connect(rotate_ccw)
        self.flipVerticalButton.clicked.connect(flip_vertical)
        self.flipHorizontalButton.clicked.connect(flip_horizontal)

    def _setup_statusbar(self):
        # Temperature monitoring
        if self.cam.props['temp_control']:
            self.tempLbl = QtGui.QLabel('T = ')
            self.statusBar.addPermanentWidget(self.tempLbl)
            self.temp_timer = QtCore.QTimer()
            self.temp_timer.setInterval(100)
            self.temp_timer.timeout.connect(
                lambda: self.tempLbl.setText(u'T = {0}\u00b0C'.format(cam.get_cooler_temperature())))
            self.temp_timer.start()

        # Ring buffer index monitoring
        self.rbLbl = QtGui.QLabel('Current index = ')
        self.statusBar.addPermanentWidget(self.rbLbl)
        self.rb_timer = QtCore.QTimer()
        self.rb_timer.setInterval(100)
        self.rb_timer.timeout.connect(
            lambda: self.rbLbl.setText(u'Current index = {0}'.format(self.cam.rbuffer.get_current_index())))
        self.rb_timer.start()

    def _setup_dialogs(self):
        self.adjustROIButton.clicked.connect(self.roi_setup)
        self.roiStatisticsButton.clicked.connect(self.launch_roi_dialog)
        self.cameraSettingsButton.clicked.connect(self.launch_setup_dialog)

    def closeEvent(self, event):
        self.cam_thread.stop()
        self.cam.close()
        super(Viewer, self).closeEvent(event)


    # Slots
    # -------------------------------------------------------------------------

    def update(self, img_data):
        """Update the image plot and other information."""
        # Apply image transformations if necessary.
        img_data = np.rot90(img_data, -self.rotation)
        if self.mirror[0]:
            img_data = np.flipud(img_data)
        if self.mirror[1]:
            img_data = np.fliplr(img_data)

        # Configure plot
        plot = self.imageWidget.get_plot()
        img = get_image_item(self.imageWidget)
        roi_rect = get_rect_item(self.imageWidget)
        if img is None:
            img = make.image(img_data, colormap=str(self.colormapBox.currentText()))
            plot.add_item(img)
        else:
            img.set_data(img_data)
        #img.select()
        #plot.replot()
            
        # Display ROI if requested.
        # TODO: fix this so that it rotates correctly along with the image!
        roi = np.array(self.cam.roi)
        # roi.shape = (2, 2)
        # center = img_data.shape[0]/2, img_data.shape[1]/2
        # roi = np.rot90(roi, -self.rotation)
        # if self.mirror[0]:
        #     roi = np.flipud(roi)
        # if self.mirror[1]:
        #     roi = np.fliplr(roi)
        # roi = roi.flatten()
        if self.showROIBox.isChecked():
            if roi_rect is None:
                roi_rect = make.annotated_rectangle(
                    roi[0], roi[1], roi[2], roi[3])
                roi_rect.set_resizable(False)
                roi_rect.set_selectable(False)
                plot.add_item(roi_rect)
            else:
                roi_rect.set_rect(roi[0], roi[1], roi[2], roi[3])
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

    def roi_setup(self):
        """Show a dialog to setup the region of interest."""
        dialog = ImageDialog("ROI Setup", edit=True, toolbar=False)
        default = dialog.add_tool(SelectTool)
        dialog.set_default_tool(default)
        roi_tool = dialog.add_tool(RectangleTool,
                                   switch_to_default_tool=True)
        roi = self.cam.roi
        old_roi = roi
        roi_tool.activate()

        # Get image and display
        plot = dialog.get_plot()
        img = make.image(self.cam_thread.img_data)
        plot.add_item(img)
        plot.set_active_item(img)

        # Wait for user input
        dialog.show()
        if dialog.exec_():
            try:
                roi = get_rect(roi_tool)
                self.cam.set_roi(roi)
            except:
                e = sys.exc_info()
                print(e)
                self.cam.set_roi(old_roi)
        
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
    #app.setWindowIcon(QtGui.QIcon('icon.png'))
    try:
        import ctypes
        myappid = 'qCamera_viewer'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except:
        pass

    win = Viewer(config, cam_select=cam_select)
    sys.exit(app.exec_())
    