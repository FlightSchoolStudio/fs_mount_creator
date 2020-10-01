# -*- coding: utf-8 -*-
#!/usr/bin/env python
#------------------------------------------------------------------------------#
#-------------------------------------------------------------------- HEADER --#
"""
Copyright Project Flight School, LLC, 2008-2019 - All rights reserved.
This software is the property of Project Flight School, LLC. It may not be 
sold, transferred, assigned, licensed, copied, distributed, or otherwise 
used without written permission.

:author:
    Joseph Kiser

:description:
    Form generated from reading UI file 'dialog.ui' 
    Created by: Qt User Interface Compiler version 5.14.2
    WARNING! All changes made in this file will be lost when recompiling 
    UI file!
"""

#------------------------------------------------------------------------------#
#------------------------------------------------------------------- IMPORTS --#
# built-in

# third-party
from tank.platform.qt import QtCore, QtGui

# external
import resources_rc

#------------------------------------------------------------------------------#
#------------------------------------------------------------------- GLOBALS --#

#------------------------------------------------------------------------------#
#----------------------------------------------------------------- FUNCTIONS --#

#------------------------------------------------------------------------------#
#------------------------------------------------------------------ CLASSES ---#
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(350, 50)

        self.horizontalLayout = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.vertical_layout = QtGui.QVBoxLayout()
        self.vertical_layout.setSpacing(6)
        self.vertical_layout.setObjectName(u"vertical_layout")
        self.vertical_layout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)        
        self.vhd_location_hor = QtGui.QHBoxLayout()
        self.vhd_location_hor.setObjectName(u"vhd_location_hor")
        self.vhd_location_hor.setContentsMargins(0, 0, -1, -1)
        self.vhd_location_lbl = QtGui.QLabel(Dialog)
        self.vhd_location_lbl.setObjectName(u"vhd_location_lbl")
        self.vhd_location_hor.addWidget(self.vhd_location_lbl)
        self.vhd_location_le = QtGui.QLineEdit(Dialog)
        self.vhd_location_le.setObjectName(u"vhd_location_le")
        self.vhd_location_hor.addWidget(self.vhd_location_le)
        self.vhd_location_browse_btn = QtGui.QPushButton(Dialog)
        self.vhd_location_browse_btn.setObjectName(u"vhd_location_browse_btn")
        self.vhd_location_hor.addWidget(self.vhd_location_browse_btn)
        self.vertical_layout.addLayout(self.vhd_location_hor)
        self.verticalSpacer = QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        self.vertical_layout.addItem(self.verticalSpacer)
        self.line = QtGui.QFrame(Dialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.vertical_layout.addWidget(self.line)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.button_hor_spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(self.button_hor_spacer)
        self.create_btn = QtGui.QPushButton(Dialog)
        self.create_btn.setObjectName(u"create_btn")
        self.horizontalLayout_2.addWidget(self.create_btn)
        self.close_btn = QtGui.QPushButton(Dialog)
        self.close_btn.setObjectName(u"close_btn")
        self.horizontalLayout_2.addWidget(self.close_btn)
        self.vertical_layout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addLayout(self.vertical_layout)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "The Current Sgtk Environment", None, QtGui.QApplication.UnicodeUTF8))
        self.vhd_location_lbl.setText(QtGui.QApplication.translate("Dialog", "VHD File Location: ", None, QtGui.QApplication.UnicodeUTF8))
        self.vhd_location_browse_btn.setText(QtGui.QApplication.translate("Dialog", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.create_btn.setText(QtGui.QApplication.translate("Dialog", "Create Mount", None, QtGui.QApplication.UnicodeUTF8))
        self.close_btn.setText(QtGui.QApplication.translate("Dialog", "Close", None, QtGui.QApplication.UnicodeUTF8))

