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
    Tool to facilitate in the setup of vhd drive mounts for shotgun.
"""

#------------------------------------------------------------------------------#
#------------------------------------------------------------------- IMPORTS --#
# built-in
import sgtk
import os
import sys
import threading
import distutils.spawn

# third-party
from sgtk.platform.qt import QtCore, QtGui
from .ui.dialog import Ui_Dialog
from fs_perforce_tools import perforce_utils
from sgtk.util import ShotgunPath

# external
from fs_ui.dialogs.popup import show_error, show_message
from fs_utils.file_system import join, set_permissions

#------------------------------------------------------------------------------#
#------------------------------------------------------------------- GLOBALS --#
LOGGER = sgtk.platform.get_logger(__name__)
VDH_DEPOT = 'VhdFiles'

#------------------------------------------------------------------------------#
#----------------------------------------------------------------- FUNCTIONS --#
def show_dialog(app_instance):
    """
    Shows the main dialog window.
    """
    app_instance.engine.show_dialog('FS Mount Creator', app_instance,
                                     AppDialog)


#------------------------------------------------------------------------------#
#------------------------------------------------------------------ CLASSES ---#
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
        self.cli_dict = dict()

        # now load in the UI that was created in the UI designer
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        self.powershell_loc = None
        self.root_location = None
        self.vhd_file_path = None
        self.ps_file_path = None
        
        self.p4_fw = perforce_utils.get_p4_fw()
        self.ui.create_btn.clicked.connect(self._create_mount_cb)
        self.ui.close_btn.clicked.connect(self._close_cb)
        self.ui.vhd_location_browse_btn.clicked.connect(self._open_browser)

        self._app = sgtk.platform.current_bundle()
        
    def _open_browser(self):
        """
        Method called to open the folder browser.
        """
        self.ui.vhd_location_le.clear()
        dir = QtGui.QFileDialog.getExistingDirectory(parent=self)
        if dir:
            norm_path = ShotgunPath.normalize(dir)
            if not norm_path.endswith('\\'):
                norm_path = '{0}\\'.format(norm_path)
            self.ui.vhd_location_le.insert(norm_path)

    def _create_mount_cb(self):
        """
        Method called to create the actual mount.
        """
        self.powershell_loc = distutils.spawn.find_executable('powershell')
        if not self.powershell_loc:
            msg = ('Windows powershell can not be located on your machine '
                   'please contact a TD!')
            show_error(msg, 'Error!')
            return

        self.client_created = self._create_client()
        if not self.client_created:
            return
        self._create_mapping()
        self._sync_files()
        self._mount_vhd()
        self.ui.vhd_location_le.clear()

    def _create_client(self):
        """
        Method to create a client to map the vhd file.
        """
        self.root_location = str(self.ui.vhd_location_le.text())
        if not self.root_location:
            msg = ('A Location for the VHD file has not been found. Please '
                   'use the file browser to establish a location.')
            show_error(msg, 'Error!')
            return None
        self.cli_dict = self.p4_fw.utils.create_client_for_user(root=self.root_location)

        return self.cli_dict['Client']
    
    def _create_mapping(self):
        """
        Method to create a mapping for our created client so the vhd file 
        gets synced locally.
        """
        mapping = '//{0}/... //{1}/{0}/...'.format(VDH_DEPOT, 
                                                   self.client_created)
        self.p4_fw.utils.add_workspace_mappings(self.client_created, [mapping])
    
    def _sync_files(self):
        """
        Method to actually sync the vhd file.
        """
        p4_connection = self.p4_fw.connection.connect(None, None, 
                                                      client=self.client_created, 
                                                      skip_client=False)
        vhd_file_path = '//{0}/VhdFiles/shotgun_vhd_500gb.vhdx'.format(self.client_created)
        ps_file_path = '//{0}/VhdFiles/mount_vhd.ps1'.format(self.client_created)
        self.vhd_file_path = '{0}VhdFiles\shotgun_vhd_500gb.vhdx'.format(self.root_location)
        self.ps_file_path = '{0}VhdFiles\mount_vhd.ps1'.format(self.root_location)
        self.p4_fw.utils.sync_files([vhd_file_path, ps_file_path], p4=p4_connection)
    
    def _mount_vhd(self):
        """
        Method to mount the vhd file.
        """
        self.p4_fw.utils.delete_client(self.client_created)
        
        self.powershell_loc = self.powershell_loc.replace('\\', '/')
        self.vhd_file_path = self.vhd_file_path.replace('\\', '/')
        self.ps_file_path = self.ps_file_path.replace('\\', '/')
        
        set_permissions(self.vhd_file_path)
        set_permissions(self.ps_file_path)

        call = '{0} -ExecutionPolicy Bypass -File {1}'.format(self.powershell_loc, 
                                                              self.ps_file_path)
        os.system(call)
        
        msg = 'VHD file successfully mounted!'
        show_message(msg, 'Success!')
        
    def _close_cb(self):
        """
        Method called to close the dialog.
        """
        self.close()
