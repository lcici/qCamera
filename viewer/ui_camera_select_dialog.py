# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'camera_select_dialog.ui'
#
# Created: Wed Aug  6 11:13:44 2014
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_CameraSelectDialog(object):
    def setupUi(self, CameraSelectDialog):
        CameraSelectDialog.setObjectName(_fromUtf8("CameraSelectDialog"))
        CameraSelectDialog.resize(487, 224)
        self.verticalLayout = QtGui.QVBoxLayout(CameraSelectDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(CameraSelectDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.cameraTypeBox = QtGui.QComboBox(CameraSelectDialog)
        self.cameraTypeBox.setObjectName(_fromUtf8("cameraTypeBox"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.cameraTypeBox)
        self.realCameraBox = QtGui.QCheckBox(CameraSelectDialog)
        self.realCameraBox.setText(_fromUtf8(""))
        self.realCameraBox.setChecked(True)
        self.realCameraBox.setObjectName(_fromUtf8("realCameraBox"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.realCameraBox)
        self.label_2 = QtGui.QLabel(CameraSelectDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtGui.QLabel(CameraSelectDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.useRingBufferBox = QtGui.QCheckBox(CameraSelectDialog)
        self.useRingBufferBox.setText(_fromUtf8(""))
        self.useRingBufferBox.setObjectName(_fromUtf8("useRingBufferBox"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.useRingBufferBox)
        self.label_4 = QtGui.QLabel(CameraSelectDialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.propsFileEdit = QtGui.QLineEdit(CameraSelectDialog)
        self.propsFileEdit.setEnabled(False)
        self.propsFileEdit.setObjectName(_fromUtf8("propsFileEdit"))
        self.horizontalLayout.addWidget(self.propsFileEdit)
        self.fileSelectButton = QtGui.QToolButton(CameraSelectDialog)
        self.fileSelectButton.setEnabled(False)
        self.fileSelectButton.setObjectName(_fromUtf8("fileSelectButton"))
        self.horizontalLayout.addWidget(self.fileSelectButton)
        self.formLayout.setLayout(3, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.verticalLayout.addLayout(self.formLayout)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.okButton = QtGui.QPushButton(CameraSelectDialog)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.horizontalLayout_2.addWidget(self.okButton)
        self.quitButton = QtGui.QPushButton(CameraSelectDialog)
        self.quitButton.setObjectName(_fromUtf8("quitButton"))
        self.horizontalLayout_2.addWidget(self.quitButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(CameraSelectDialog)
        QtCore.QMetaObject.connectSlotsByName(CameraSelectDialog)

    def retranslateUi(self, CameraSelectDialog):
        CameraSelectDialog.setWindowTitle(QtGui.QApplication.translate("CameraSelectDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("CameraSelectDialog", "Camera Type", None, QtGui.QApplication.UnicodeUTF8))
        self.realCameraBox.setToolTip(QtGui.QApplication.translate("CameraSelectDialog", "When unchecked, simulate the selected camera.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("CameraSelectDialog", "Real camera", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("CameraSelectDialog", "Use ring buffer", None, QtGui.QApplication.UnicodeUTF8))
        self.useRingBufferBox.setToolTip(QtGui.QApplication.translate("CameraSelectDialog", "When checked, enable the ring buffer.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("CameraSelectDialog", "Custom properties file", None, QtGui.QApplication.UnicodeUTF8))
        self.propsFileEdit.setToolTip(QtGui.QApplication.translate("CameraSelectDialog", "Leave blank to use the default props file for the selected camera.", None, QtGui.QApplication.UnicodeUTF8))
        self.fileSelectButton.setText(QtGui.QApplication.translate("CameraSelectDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setText(QtGui.QApplication.translate("CameraSelectDialog", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.quitButton.setText(QtGui.QApplication.translate("CameraSelectDialog", "Quit", None, QtGui.QApplication.UnicodeUTF8))

