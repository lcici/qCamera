"""ROI setup dialog"""

import sys
import numpy as np
from qcamera import Camera

try:
    from PyQt4 import QtGui, QtCore
except ImportError:
    from PySide import QtGui, QtCore
from guiqwt.builder import make
from guiqwt.plot import ImageDialog
from guiqwt.tools import SelectTool, RectangleTool

import util
from ui_roi_dialog import Ui_ROIDialog

class ROIDialog(QtGui.QDialog, Ui_ROIDialog):
    """Class controlling the ROI setup dialog."""
    def __init__(self, cam, thread):
        QtGui.QWidget.__init__(self)
        assert isinstance(cam, Camera)
        self.cam = cam
        self.thread = thread

        # Setup UI
        self.setupUi(self)
        self.show()
        self.closeButton.clicked.connect(self.done)
        self.adjustROIButton.clicked.connect(self.roi_setup)
        self.thread.image_signal.connect(self.update)

    def update(self, img_data):
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

        roi_x1, roi_x2, roi_y1, roi_y2 = self.cam.roi
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
        img = make.image(self.thread.img_data)
        plot.add_item(img)
        plot.set_active_item(img)

        # Wait for user input
        dialog.show()
        if dialog.exec_():
            try:
                roi = util.get_rect(roi_tool)
                self.cam.set_roi(roi)
            except:
                e = sys.exc_info()
                print(e)
                self.cam.set_roi(old_roi)