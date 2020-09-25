# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import sgtk
import os
import sys
import threading

# by importing QT from sgtk rather than directly, we ensure that
# the code will be compatible with both PySide and PyQt.
from sgtk.platform.qt import QtCore, QtGui
from .ui.dialog import Ui_Dialog
from fs_perforce_tools import perforce_utils
from sgtk.util import ShotgunPath

# standard toolkit logger
logger = sgtk.platform.get_logger(__name__)

VDH_DEPOT = 'VhdFiles'

def show_dialog(app_instance):
    """
    Shows the main dialog window.
    """
    # in order to handle UIs seamlessly, each toolkit engine has methods for launching
    # different types of windows. By using these methods, your windows will be correctly
    # decorated and handled in a consistent fashion by the system.

    # we pass the dialog class to this method and leave the actual construction
    # to be carried out by toolkit.
    app_instance.engine.show_dialog('FS Mount Creator', app_instance, AppDialog)


class AppDialog(QtGui.QWidget):
    """
    Main application dialog window
    """

    def __init__(self):
        """
        Constructor
        """
        # first, call the base class and let it do its thing.
        QtGui.QWidget.__init__(self)
        
        self.client_created = None
        self.client_dict = dict()
        
        # now load in the UI that was created in the UI designer
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.populate_combo()

        self.p4_fw = perforce_utils.get_p4_fw()

        self.ui.create_btn.clicked.connect(self._create_mount_cb)

        self.ui.close_btn.clicked.connect(self._close_cb)
        
        self.ui.vhd_location_browse_btn.clicked.connect(self._open_browser)

        self._app = sgtk.platform.current_bundle()
    
    def populate_combo(self):
        """
        This method checks perforce for the different size vhd file options.
        """
        self.ui.vhd_size_combo.clear()
        self.ui.vhd_size_combo.addItem('test')

    def _open_browser(self):
        """
        Method called to open the folder browser.
        """
        self.ui.vhd_location_le.clear()
        dir = QtGui.QFileDialog.getExistingDirectory(parent=self)
        if dir:
            norm_path = ShotgunPath.normalize(dir)
            self.ui.vhd_location_le.insert(norm_path)

    def _create_mount_cb(self):
        """
        """
        self.client_created = self._create_client()
        if not self.client_created:
            return
        self._create_mapping()
        
        self._sync_files()

        self.ui.vhd_location_le.clear()

    def _create_client(self):
        """
        """
        root_location = str(self.ui.vhd_location_le.text())
        if not root_location:
            logger.debug('A Location for the VHD file has not been found. '
                         'Please use the file browser to establish a '
                         'location.')
            return None
        self.client_dict = self.p4_fw.utils.create_client_for_user(root=root_location)

        return self.client_dict['Client']
    
    def _create_mapping(self):
        """
        """
        mapping = '//{0}/... //{1}/{0}/...'.format(VDH_DEPOT, 
                                                   self.client_created)
        self.p4_fw.utils.add_workspace_mappings(self.client_created, [mapping])
    
    def _sync_files(self):
        """
        """
        p4_connection = self.p4_fw.connection.connect(None, None, 
                                                      client=self.client_created, 
                                                      skip_client=False)
        p4_file_path = '//{0}/VhdFiles/shotgun_vhd_500gb.vhdx'.format(self.client_created)
        self.p4_fw.utils.sync_files([p4_file_path], p4=p4_connection)
        
    def _close_cb(self):
        self.close()
