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
from guiqwt.annotations import AnnotatedRectangle
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
        #self.cam.rbuffer.recording = not self.rbufferBox.checkState()

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
        self.xCropMinBox.valueChanged.connect(self.set_crop)
        self.xCropMaxBox.valueChanged.connect(self.set_crop)
        self.yCropMinBox.valueChanged.connect(self.set_crop)
        self.yCropMaxBox.valueChanged.connect(self.set_crop)
        self.binsBox.currentIndexChanged.connect(self.set_bins)

        # ROI settings
        # TODO: change limits when changing binning!
        roi = [self.xROIMinBox.value(), self.xROIMaxBox.value(),
               self.yROIMinBox.value(), self.yROIMaxBox.value()]
        self.cam.set_roi(roi)
        
        self.xROIMinBox.setMaximum(self.cam.shape[0])
        self.yROIMinBox.setMaximum(self.cam.shape[1])
        self.xROIMinSlider.setMaximum(self.cam.shape[0])
        self.yROIMinSlider.setMaximum(self.cam.shape[1])
        self.xROIMaxBox.setMaximum(self.cam.shape[0])
        self.yROIMaxBox.setMaximum(self.cam.shape[1])
        self.xROIMaxSlider.setMaximum(self.cam.shape[0])
        self.yROIMaxSlider.setMaximum(self.cam.shape[1])
        
        self.xROIMinBox.valueChanged.connect(self.set_roi)
        self.xROIMaxBox.valueChanged.connect(self.set_roi)
        self.yROIMinBox.valueChanged.connect(self.set_roi)
        self.yROIMaxBox.valueChanged.connect(self.set_roi)

        # Viewing settings
        self.scaleMinBox.valueChanged.connect(self.set_lut_range)
        self.scaleMaxBox.valueChanged.connect(self.set_lut_range)
        #self.rbufferBox.stateChanged.connect(self.set_rbuffer_recording)

        # Start the thread.
        self.cam_thread.start()

    @QtCore.pyqtSlot(np.ndarray)
    def update_image(self, img_data):
        """Update the image plot."""
        # Get and display the next image.
        plot = self.imageWidget.get_plot()
        plot.del_all_items(except_grid=True)
        img = make.image(img_data, colormap=str(self.colormapBox.currentText()))
        img.set_lut_range(self.scale)
        plot.add_item(img)
        plot.set_plot_limits(0, img_data.shape[1], 0, img_data.shape[0])

        # Draw ROI rectangle if requested.
        if self.roiShowBox.isChecked():
            roi_x1 = self.xROIMinBox.value()
            roi_x2 = self.xROIMaxBox.value()
            roi_y1 = self.yROIMinBox.value()
            roi_y2 = self.yROIMaxBox.value()
            roi_rect = make.annotated_rectangle(
                roi_x1, roi_y1, roi_x2, roi_y2,
                title='ROI')
            plot.add_item(roi_rect)

        # Calculate and update ROI statistics.
        roi = img_data[self.cam.roi[2]:self.cam.roi[3],
                       self.cam.roi[0]:self.cam.roi[1]]
        #np.save('roi.npy', roi) # for debugging
        counts = np.sum(roi)
        mean = np.mean(roi)
        max_ = np.max(roi)
        min_ = np.min(roi)
        self.roiTotalLbl.setText('%.0f' % counts)
        self.roiMeanLbl.setText('%.2f' % mean)
        self.roiMaxLbl.setText('%.0f' % max_)
        self.roiMinLbl.setText('%.0f' % min_)
        h_plot = self.roiHistWidget.get_plot()
        h_plot.del_all_items(except_grid=True)
        #hist = make.histogram(roi.flatten()/max_, 100)
        hist = make.histogram(roi.flatten(), 50)
        h_plot.add_item(hist)
        #print(hist.get_data())
        h_plot.set_plot_limits(0, self.xHistLimBox.value(), 0, self.yHistLimBox.value())
        h_plot.set_item_visible(hist, True)

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
        t = self.exposureTimeBox.value()
        self.cam.set_exposure_time(t)

    def set_crop(self):
        """Set the camera hardware cropping."""

    def set_roi(self):
        """Update the region of interest."""
        # TODO: Make this work correctly with binning!
        # Make sure min < max.
        x1, x2 = self.xROIMinBox.value(), self.xROIMaxBox.value()
        y1, y2 = self.yROIMinBox.value(), self.yROIMaxBox.value()
        if x1 >= x2:
            self.xROIMinBox.setValue(x2 - 1)
        if y1 >= y2:
            self.yROIMinBox.setValue(y2 - 1)

        # Update camera ROI.
        self.cam.set_roi([self.xROIMinBox.value(), self.xROIMaxBox.value(),
                          self.yROIMinBox.value(), self.yROIMaxBox.value()])

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
    with Sensicam(real=True, recording=False) as cam:
        thread = CameraThread(cam)
        win = Viewer(cam, thread)
        win.show()
        sys.exit(app.exec_())
    