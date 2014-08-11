"""ROI setup dialog"""

import numpy as np
from qcamera import Camera

from PyQt4 import QtGui
from guiqwt.builder import make
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
        self.thread.image_signal.connect(self.update)

    def update(self, img_data):
        # Calculate and update ROI statistics.
        roi = img_data[self.cam.roi[1]:self.cam.roi[3],
                       self.cam.roi[0]:self.cam.roi[2]]
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

        # ROI histogram plot
        h_plot = self.roiHistWidget.get_plot()
        h_plot.del_all_items(except_grid=True)
        hist = make.histogram(roi.flatten(), 50)
        h_plot.add_item(hist)
        #print(hist.get_data())
        h_plot.set_plot_limits(0, self.xHistLimBox.value(), 0, self.yHistLimBox.value())
        h_plot.set_item_visible(hist, True)

        # Display ROI coordinates
        roi = self.cam.roi
        self.roiX1Lbl.setNum(roi[0])
        self.roiY1Lbl.setNum(roi[1])
        self.roiX2Lbl.setNum(roi[2])
        self.roiY2Lbl.setNum(roi[3])
        