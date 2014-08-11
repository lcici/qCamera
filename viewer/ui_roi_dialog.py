# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'roi_dialog.ui'
#
# Created: Mon Aug 11 10:17:45 2014
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ROIDialog(object):
    def setupUi(self, ROIDialog):
        ROIDialog.setObjectName(_fromUtf8("ROIDialog"))
        ROIDialog.resize(411, 533)
        self.verticalLayout = QtGui.QVBoxLayout(ROIDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox_5 = QtGui.QGroupBox(ROIDialog)
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.roiHistWidget = CurveWidget(self.groupBox_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.roiHistWidget.sizePolicy().hasHeightForWidth())
        self.roiHistWidget.setSizePolicy(sizePolicy)
        self.roiHistWidget.setMinimumSize(QtCore.QSize(0, 10))
        self.roiHistWidget.setOrientation(QtCore.Qt.Horizontal)
        self.roiHistWidget.setObjectName(_fromUtf8("roiHistWidget"))
        self.verticalLayout_3.addWidget(self.roiHistWidget)
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.xHistLimBox = QtGui.QSpinBox(self.groupBox_5)
        self.xHistLimBox.setMaximum(65536)
        self.xHistLimBox.setSingleStep(100)
        self.xHistLimBox.setProperty("value", 500)
        self.xHistLimBox.setObjectName(_fromUtf8("xHistLimBox"))
        self.gridLayout_3.addWidget(self.xHistLimBox, 0, 1, 1, 1)
        self.yHistLimBox = QtGui.QSpinBox(self.groupBox_5)
        self.yHistLimBox.setMaximum(65536)
        self.yHistLimBox.setSingleStep(10)
        self.yHistLimBox.setProperty("value", 2000)
        self.yHistLimBox.setObjectName(_fromUtf8("yHistLimBox"))
        self.gridLayout_3.addWidget(self.yHistLimBox, 0, 3, 1, 1)
        self.label_19 = QtGui.QLabel(self.groupBox_5)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.gridLayout_3.addWidget(self.label_19, 0, 0, 1, 1)
        self.label_20 = QtGui.QLabel(self.groupBox_5)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.gridLayout_3.addWidget(self.label_20, 0, 2, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_3)
        self.verticalLayout.addWidget(self.groupBox_5)
        self.groupBox_4 = QtGui.QGroupBox(ROIDialog)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox_4)
        self.gridLayout.setHorizontalSpacing(12)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_15 = QtGui.QLabel(self.groupBox_4)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_15)
        self.roiTotalLbl = QtGui.QLabel(self.groupBox_4)
        self.roiTotalLbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.roiTotalLbl.setObjectName(_fromUtf8("roiTotalLbl"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.roiTotalLbl)
        self.label_16 = QtGui.QLabel(self.groupBox_4)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_16)
        self.roiMeanLbl = QtGui.QLabel(self.groupBox_4)
        self.roiMeanLbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.roiMeanLbl.setObjectName(_fromUtf8("roiMeanLbl"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.roiMeanLbl)
        self.label_17 = QtGui.QLabel(self.groupBox_4)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_17)
        self.roiMinLbl = QtGui.QLabel(self.groupBox_4)
        self.roiMinLbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.roiMinLbl.setObjectName(_fromUtf8("roiMinLbl"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.roiMinLbl)
        self.label_18 = QtGui.QLabel(self.groupBox_4)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_18)
        self.roiMaxLbl = QtGui.QLabel(self.groupBox_4)
        self.roiMaxLbl.setEnabled(True)
        self.roiMaxLbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.roiMaxLbl.setObjectName(_fromUtf8("roiMaxLbl"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.roiMaxLbl)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)
        self.formLayout_4 = QtGui.QFormLayout()
        self.formLayout_4.setObjectName(_fromUtf8("formLayout_4"))
        self.label_6 = QtGui.QLabel(self.groupBox_4)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_6)
        self.label_7 = QtGui.QLabel(self.groupBox_4)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_7)
        self.label_8 = QtGui.QLabel(self.groupBox_4)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout_4.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_8)
        self.label_9 = QtGui.QLabel(self.groupBox_4)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.formLayout_4.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_9)
        self.roiX1Lbl = QtGui.QLabel(self.groupBox_4)
        self.roiX1Lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.roiX1Lbl.setObjectName(_fromUtf8("roiX1Lbl"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.FieldRole, self.roiX1Lbl)
        self.roiX2Lbl = QtGui.QLabel(self.groupBox_4)
        self.roiX2Lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.roiX2Lbl.setObjectName(_fromUtf8("roiX2Lbl"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.FieldRole, self.roiX2Lbl)
        self.roiY1Lbl = QtGui.QLabel(self.groupBox_4)
        self.roiY1Lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.roiY1Lbl.setObjectName(_fromUtf8("roiY1Lbl"))
        self.formLayout_4.setWidget(2, QtGui.QFormLayout.FieldRole, self.roiY1Lbl)
        self.roiY2Lbl = QtGui.QLabel(self.groupBox_4)
        self.roiY2Lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.roiY2Lbl.setObjectName(_fromUtf8("roiY2Lbl"))
        self.formLayout_4.setWidget(3, QtGui.QFormLayout.FieldRole, self.roiY2Lbl)
        self.gridLayout.addLayout(self.formLayout_4, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_4)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.closeButton = QtGui.QPushButton(ROIDialog)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.horizontalLayout.addWidget(self.closeButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ROIDialog)
        QtCore.QMetaObject.connectSlotsByName(ROIDialog)

    def retranslateUi(self, ROIDialog):
        ROIDialog.setWindowTitle(QtGui.QApplication.translate("ROIDialog", "Region of Interest", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_5.setTitle(QtGui.QApplication.translate("ROIDialog", "ROI Histogram", None, QtGui.QApplication.UnicodeUTF8))
        self.label_19.setText(QtGui.QApplication.translate("ROIDialog", "x lim", None, QtGui.QApplication.UnicodeUTF8))
        self.label_20.setText(QtGui.QApplication.translate("ROIDialog", "y lim", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("ROIDialog", "ROI Statistics", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("ROIDialog", "Total", None, QtGui.QApplication.UnicodeUTF8))
        self.roiTotalLbl.setText(QtGui.QApplication.translate("ROIDialog", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("ROIDialog", "Mean", None, QtGui.QApplication.UnicodeUTF8))
        self.roiMeanLbl.setText(QtGui.QApplication.translate("ROIDialog", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setText(QtGui.QApplication.translate("ROIDialog", "Min", None, QtGui.QApplication.UnicodeUTF8))
        self.roiMinLbl.setText(QtGui.QApplication.translate("ROIDialog", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_18.setText(QtGui.QApplication.translate("ROIDialog", "Max", None, QtGui.QApplication.UnicodeUTF8))
        self.roiMaxLbl.setText(QtGui.QApplication.translate("ROIDialog", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("ROIDialog", "x1", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("ROIDialog", "x2", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("ROIDialog", "y1", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("ROIDialog", "y2", None, QtGui.QApplication.UnicodeUTF8))
        self.roiX1Lbl.setText(QtGui.QApplication.translate("ROIDialog", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.roiX2Lbl.setText(QtGui.QApplication.translate("ROIDialog", "2", None, QtGui.QApplication.UnicodeUTF8))
        self.roiY1Lbl.setText(QtGui.QApplication.translate("ROIDialog", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.roiY2Lbl.setText(QtGui.QApplication.translate("ROIDialog", "2", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("ROIDialog", "Close", None, QtGui.QApplication.UnicodeUTF8))

from guiqwt.plot import CurveWidget
