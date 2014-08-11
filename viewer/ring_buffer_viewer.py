"""Ring buffer viewer"""

import tables

from qcamera.ring_buffer import RingBuffer

from PyQt4 import QtGui
from guiqwt.builder import make
from ui_ring_buffer_viewer import Ui_RingBufferViewer
from util import get_image_item

class RingBufferViewer(QtGui.QDialog, Ui_RingBufferViewer):
    def __init__(self, rbuffer, parent):
        QtGui.QDialog.__init__(self, parent=parent)
        assert isinstance(rbuffer, RingBuffer)

        # Stop recording
        self.rbuffer = rbuffer
        self.was_recording = self.rbuffer.recording
        self.rbuffer.recording = False

        # Setup UI
        self.setupUi(self)
        self.show()
        self.closeButton.clicked.connect(self.finished)
        max_ = self.parent().cam.rbuffer.get_current_index() - 1
        self.indexBox.setRange(0, max_)
        self.indexSlider.setRange(0, max_)

        # Connect signals
        self.indexBox.valueChanged.connect(self.update)
        self.update()

    def update(self):
        """Show the currently selected image from the ring buffer."""
        # Get the specified image data
        img_data = self.rbuffer.read(self.indexBox.value())

        # Update the viewer
        plot = self.imageWidget.get_plot()
        img = get_image_item(self.imageWidget)
        if img is None:
            img = make.image(img_data, colormap=str(self.parent().colormapBox.currentText()))
            plot.add_item(img)
        else:
            img.set_data(img_data)
        plot.replot()

    def finished(self):
        """Resume recording and quit."""
        if self.was_recording:
            self.rbuffer.recording = True
        self.done(0)
        