"""Simple testing of acquiring image data from a camera and displaying
it in a Qt GUI.

"""

from __future__ import print_function
import sys

# Ensure we're loading the newest version of qcamera rather than
# anything that was installed with distutils.
sys.path[0:0] = ['..']

import time
import numpy as np

from PyQt4 import QtGui, QtCore
from guiqwt.plot import ImageDialog
from guiqwt.tools import SelectTool, AnnotatedRectangleTool
from guiqwt.image import ImageItem
from guiqwt.annotations import AnnotatedRectangle
from guiqwt.builder import make
from guiqwt.colormap import get_colormap_list

from qcamera import AndorCamera, Sensicam
from ui_viewer import Ui_MainWindow
from qcamera.camera_thread import CameraThread

def _get_image_item(imageWidget):
    items = imageWidget.get_plot().get_items()
    for item in items:
        image = item if isinstance(item, ImageItem) else None
    return image

class Viewer(QtGui.QMainWindow, Ui_MainWindow):
    """Simple GUI testbed for qCamera."""

    # Setup and shutdown
    # -------------------------------------------------------------------------
    
    def __init__(self, camera, thread):
        # Basic initialization.
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.cam = camera
        self.cam_thread = thread
        self.scale = [self.scaleMinBox.value(), self.scaleMaxBox.value()]
        #self.cam.rbuffer.recording = not self.rbufferBox.checkState()

        # Add colormaps to the combo box
        self.colormapBox.addItems(get_colormap_list())
        self.colormapBox.setCurrentIndex(51) # jet
        self.colormapBox.currentIndexChanged.connect(self.update_colormap)

        # Connect image signals
        self.cam_thread.image_signal.connect(self.update)

        # Exposure and trigger settings signals
        self.set_t_exp()
        self.exposureTimeBox.editingFinished.connect(self.set_t_exp)
        self.acquisitionButton.clicked.connect(self.toggle_acquisition)
        self.triggerModeBox.currentIndexChanged.connect(self.set_trigger_mode)

        # Shutter control
        self.openShutterButton.clicked.connect(self.open_shutter)
        self.closeShutterButton.clicked.connect(self.close_shutter)
        if self.cam.props['shutter']:
            if self.cam.props['init_shutter']:
                self.openShutterButton.setChecked(True)
                self.open_shutter()

        # Crop/binning/ROI dialogs
        self.adjustCropButton.clicked.connect(self.crop_setup)
        self.adjustROIButton.clicked.connect(self.roi_setup)
        self.setBinsButton.clicked.connect(self.bins_setup)

        # Viewing settings
        self.scaleMinBox.valueChanged.connect(self.set_lut_range)
        self.scaleMaxBox.valueChanged.connect(self.set_lut_range)
        self.rescaleButton.clicked.connect(self.rescale)
        self.rotateImageButton.clicked.connect(self.rotate_image)
        #self.rbufferBox.stateChanged.connect(self.set_rbuffer_recording)

        # Temperature control
        self.coolerOnButton.clicked.connect(self.cam.cooler_on)
        self.coolerOffButton.clicked.connect(self.cam.cooler_off)
        self.tempSetPointBox.editingFinished.connect(self.set_temperature)
        if not cam.props['temp_control']:
            self.tempSetPointBox.setEnabled(False)
            self.coolerStateBox.setEnabled(False)
            self.tempLbl.setText('N/A')
        else:
            # Setup controls
            min_, max_ = self.cam.props['temp_range']
            self.tempSetPointBox.setRange(int(min_), int(max_))
            self.tempSetPointBox.setValue(self.cam.get_cooler_temperature())

            # Turn on temperature control if camera properties say to.
            if self.cam.props['auto_temp_control']:
                self.tempSetPointBox.setValue(self.cam.props['init_set_point'])
                self.coolerOnButton.setChecked(True)
                self.set_temperature()
                self.cam.cooler_on()

            # Setup a timer to poll the temperature
            self.temp_checker = QtCore.QTimer()
            self.temp_checker.setInterval(5000)
            self.temp_checker.timeout.connect(self.check_temperature)
            self.temp_checker.start()

        # Gain control
        grange = self.cam.props['gain_range']
        self.gainSlider.setRange(grange[0], grange[1])
        self.gainLbl.setNum(self.cam.props['init_gain'])
        if not self.cam.props['gain_adjust']:
            self.gainSlider.setEnabled(False)
        self.gainSlider.sliderReleased.connect(self.set_gain)

        # Start the thread.
        self.cam_thread.start()
        self.toggle_acquisition()

    def closeEvent(self, event):
        self.cam_thread.stop()
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

    def _get_image_plot(self):
        """Extract the image plot from the image widget."""
        for item in self.imageWidget.get_plot().get_items():
            img = item
            if isinstance(item, ImageItem):
                break
        return img

    # Slots
    # -------------------------------------------------------------------------

    @QtCore.pyqtSlot(np.ndarray)
    def update(self, img_data):
        """Update the image plot and other information."""
        # Get and display the next image.
        plot = self.imageWidget.get_plot()
        #plot.del_all_items(except_grid=True)
        items = plot.get_items()
        for item in items:
            img = item if isinstance(item, ImageItem) else None
            roi_rect = item if isinstance(item, AnnotatedRectangle) else None
        if img is None:
            img = self._make_image_item(img_data)
            plot.add_item(img)
        else:
            img.set_data(img_data)
        #img.select()
        #plot.replot()
            
        # Display ROI if requested.
        # TODO
        roi_x1, roi_x2, roi_y1, roi_y2 = self.cam.roi
        if self.showROIBox.isChecked():
            if roi_rect is None:
                roi_rect = make.annotated_rectangle(
                    roi_x1, roi_x2, roi_y1, roi_y2)
                roi_rect.set_resizable(False)
                roi_rect.set_selectable(False)
                plot.add_item(roi_rect)
        else:
            if roi_rect is not None:
                plot.del_item(roi_rect)

        # Update plot
        if self.autoscaleButton.isChecked():
            self.rescale()
        self.set_lut_range()
        plot.set_plot_limits(0, img_data.shape[1], 0, img_data.shape[0])
        plot.replot()

        # Calculate and update ROI statistics.
        roi = img_data[self.cam.roi[2]:self.cam.roi[3],
                       self.cam.roi[0]:self.cam.roi[1]]
        #np.save('roi.npy', roi) # for debugging
        try:
            self.roiTotalLbl.setText('%.0f' % np.sum(roi))
            self.roiMeanLbl.setText('%.2f' % np.mean(roi))
            self.roiMaxLbl.setText('%.0f' % np.max(roi))
            self.roiMinLbl.setText('%.0f' % np.min(roi))
        except:
            print("self.cam.roi:", self.cam.roi)
            print("roi:", roi)
            print("img_data:", img_data)

        self.roiX1Lbl.setNum(roi_x1)
        self.roiX2Lbl.setNum(roi_x2)
        self.roiY1Lbl.setNum(roi_y1)
        self.roiY2Lbl.setNum(roi_y2)

        # ROI histogram plot
        h_plot = self.roiHistWidget.get_plot()
        h_plot.del_all_items(except_grid=True)
        hist = make.histogram(roi.flatten(), 50)
        h_plot.add_item(hist)
        #print(hist.get_data())
        h_plot.set_plot_limits(0, self.xHistLimBox.value(), 0, self.yHistLimBox.value())
        h_plot.set_item_visible(hist, True)
                    
    def update_colormap(self):
        image = _get_image_item(self.imageWidget)
        image.set_color_map(str(self.colormapBox.currentText()))
        
    def set_lut_range(self):
        """Change the LUT range."""
        self.scale = [self.scaleMinBox.value(), self.scaleMaxBox.value()]
        img = self._get_image_plot()
        img.set_lut_range(self.scale)

    def rescale(self):
        """Change the LUT range to the have min and max values the
        same as the image data.

        """
        img = self._get_image_plot()
        self.scaleMinBox.setValue(int(np.min(img.data)))
        self.scaleMaxBox.setValue(int(np.max(img.data)))
        self.set_lut_range()

    def rotate_image(self):
        """Rotate the image 90 degrees upon presing."""
        print("Rotating not yet implemented!")

    def toggle_acquisition(self):
        """Toggle between acquisition states (on or off)."""
        start_text = "Begin Acquisition"
        stop_text = "Stop Acquisition"
        if self.acquisitionButton.text() == start_text:
            self.cam_thread.unpause()
            self.acquisitionButton.setText(stop_text)
            self.shutterGroupBox.setEnabled(False)
        else:
            self.cam_thread.pause()
            self.acquisitionButton.setText(start_text)
            self.shutterGroupBox.setEnabled(True)

    def set_trigger_mode(self):
        """Change the camera's triggering mode."""
        self.cam_thread.queue.put('pause')
        mode = self.triggerModeBox.currentIndex()
        self.cam.set_trigger_mode(mode)

    def open_shutter(self):
        self.cam.open_shutter()

    def close_shutter(self):
        self.cam.close_shutter()

    def set_t_exp(self):
        """Change the exposure time."""
        t = self.exposureTimeBox.value()
        self.cam.set_exposure_time(t)

    # Setup dialogs
    # -------------------------------------------------------------------------

    def crop_setup(self):
        """Show the crop setup dialog."""
        # Reset the crop and take an image
        if not self.cam_thread.paused:
            self.toggle_acquisition()
        while not self.cam_thread.paused:
            time.sleep(0.01)
        old_crop = self.cam.get_crop()
        self.cam.reset_crop()
        time.sleep(0.01)
        self.cam_thread.get_single_image()
        
        # Setup the dialog with rectangle selection tool
        dialog = ImageDialog("Crop Setup", edit=True)
        default = dialog.add_tool(SelectTool)
        dialog.set_default_tool(default)
        crop_tool = dialog.add_tool(AnnotatedRectangleTool, title='Crop',
                                    switch_to_default_tool=True)
        crop_tool.activate()

        # Add last acquired image
        plot = dialog.get_plot()
        img_data = _get_image_item(self.imageWidget).data
        img = self._make_image_item(img_data)
        plot.add_item(img)
        plot.set_active_item(img)

        # Wait for user input
        dialog.show()
        if dialog.exec_():
            try:
                # Set the new crop
                crop = self._get_rect(crop_tool)
                self.cam.set_crop(crop)

                # Reset the ROI to something that won't cause problems.
                self.cam.set_roi([1, 2, 1, 2])
            except:
               # Retain old crop
               e = sys.exc_info()
               print(e)
               self.cam.set_crop(old_crop)

    def roi_setup(self):
        """Show a dialog to setup the region of interest."""
        dialog = ImageDialog("ROI Setup", edit=True)
        default = dialog.add_tool(SelectTool)
        dialog.set_default_tool(default)
        roi_tool = dialog.add_tool(AnnotatedRectangleTool, title='ROI',
                                   switch_to_default_tool=True)
        roi = self.cam.roi
        old_roi = roi
        roi_tool.activate()
        # TODO: Figure out how to show initial ROI
        #roi_tool.set_shape_style(AnnotatedRectangle(roi[0], roi[2], roi[1], roi[3]))

        # Connect the plot to the camera image.
        # TODO: Make this a live view if possible.
        plot = dialog.get_plot()
        img_data = _get_image_item(self.imageWidget).data
        img = self._make_image_item(img_data)
        plot.add_item(img)
        plot.set_active_item(img)

        # Wait for user input
        dialog.show()
        if dialog.exec_():
            try:
                roi = self._get_rect(roi_tool)
                self.cam.set_roi(roi)
            except:
                e = sys.exc_info()
                print(e)
                self.cam.set_roi(old_roi)

    def bins_setup(self):
        """Show a dialog for setting binning."""
        # Pause acquisition.
        if not self.cam_thread.paused:
            self.toggle_acquisition()
        while not self.cam_thread.paused:
            time.sleep(0.01)

        # Query for new binning.
        bin_options = [str(x) for x in self.cam.props['bins']]
        bin_index = 0
        for i, bin in enumerate(bin_options):
            if int(bin) == self.cam.bins:
                bin_index = i
        bins, ok = QtGui.QInputDialog.getItem(
            self, 'Camera binning setup',
            'Bins:', bin_options, bin_index, False)

        # Set bins
        if ok:
            self.cam.set_bins(int(bins))
            

    # Temperature controls
    # -------------------------------------------------------------------------

    def check_temperature(self):
        temp = cam.get_cooler_temperature()
        self.tempLbl.setText('%i' % temp)

    def set_temperature(self):
        temp = self.tempSetPointBox.value()
        self.cam.set_cooler_temperature(temp)

    # Gain control
    # -------------------------------------------------------------------------
        
    def set_gain(self):
        self.cam_thread.pause()
        while not self.cam_thread.paused:
            time.sleep(0.01)
        self.cam.set_gain(self.gainSlider.value())
        self.cam_thread.unpause()
        

# Main
# =============================================================================

if __name__ == "__main__":
    class CameraSelectDialog(QtGui.QDialog): # TODO
        """For interactive selection of cameras at startup."""
        def __init__(self):
            super(CameraSelectDialog, self).__init__()

    import os
    import argparse
    import json
    import logging
    
    logging.basicConfig(level=logging.DEBUG)

    cam_options = {
        'andor': AndorCamera,
        'sensicam': Sensicam
    }
    def cam_options_string():
        out = ''
        for cam in cam_options:
            out = out + cam + ' '
        return out

    parser = argparse.ArgumentParser(description='qCamera Viewer')
    parser.add_argument(
        '-c', '--camera-type', metavar='<camera type>', type=str,
        help='Specify the camera type to use. If not given, ' + \
        'default to the last camera type used. Options include:\n' + \
        cam_options_string())
    args = parser.parse_args()

    config_file = 'viewer.json'
    if args.camera_type is None:
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
                camera_type = config['camera_type']
                Camera = cam_options[camera_type]
        else:
            raise RuntimeError(
                "If this is your first time running viewer.py, " + \
                "you need to specify what camera to use. " + \
                "Try viewer.py -h.")
    else:
        try:
            camera_type = args.camera_type
            Camera = cam_options[camera_type]
        except KeyError:
            print("Invalid selection. Valid camera options are:",
                  cam_options_string())
            sys.exit(1)

    with open(config_file, 'w') as f:
        last_cam = {'camera_type': camera_type}
        json.dump(last_cam, f)
    
    app = QtGui.QApplication(sys.argv)
    with Camera(real=True, recording=False) as cam:
        thread = CameraThread(cam)
        win = Viewer(cam, thread)
        win.show()
        sys.exit(app.exec_())
    