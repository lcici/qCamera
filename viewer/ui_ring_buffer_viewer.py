# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ring_buffer_viewer.ui'
#
# Created: Mon Aug 11 12:45:21 2014
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_RingBufferViewer(object):
    def setupUi(self, RingBufferViewer):
        RingBufferViewer.setObjectName(_fromUtf8("RingBufferViewer"))
        RingBufferViewer.resize(617, 601)
        self.verticalLayout = QtGui.QVBoxLayout(RingBufferViewer)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.imageWidget = ImageWidget(RingBufferViewer)
        self.imageWidget.setOrientation(QtCore.Qt.Vertical)
        self.imageWidget.setObjectName(_fromUtf8("imageWidget"))
        self.verticalLayout.addWidget(self.imageWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.indexSlider = QtGui.QSlider(RingBufferViewer)
        self.indexSlider.setOrientation(QtCore.Qt.Horizontal)
        self.indexSlider.setObjectName(_fromUtf8("indexSlider"))
        self.horizontalLayout.addWidget(self.indexSlider)
        self.indexBox = QtGui.QSpinBox(RingBufferViewer)
        self.indexBox.setObjectName(_fromUtf8("indexBox"))
        self.horizontalLayout.addWidget(self.indexBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.closeButton = QtGui.QPushButton(RingBufferViewer)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.horizontalLayout_2.addWidget(self.closeButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(RingBufferViewer)
        QtCore.QObject.connect(self.indexSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.indexBox.setValue)
        QtCore.QObject.connect(self.indexBox, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.indexSlider.setValue)
        QtCore.QMetaObject.connectSlotsByName(RingBufferViewer)

    def retranslateUi(self, RingBufferViewer):
        RingBufferViewer.setWindowTitle(QtGui.QApplication.translate("RingBufferViewer", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("RingBufferViewer", "Close", None, QtGui.QApplication.UnicodeUTF8))

from guiqwt.plot import ImageWidget
