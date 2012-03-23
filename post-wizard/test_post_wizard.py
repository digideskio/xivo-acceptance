# -*- coding: UTF-8 -*-

import unittest
import os
import subprocess

from pwd import getpwnam


class TestDhcpdUpdate(unittest.TestCase):

    DHCPD_UPDATE_DIR = '/etc/dhcp/dhcpd_update'

    def test_have_dhcpd_update_files(self):
        self.assertTrue(os.access(self.DHCPD_UPDATE_DIR, os.R_OK))
        self.assertTrue(len(os.listdir(self.DHCPD_UPDATE_DIR)) > 0)


class TestCtiConfFile(unittest.TestCase):

    CTI_INI_FILE = '/etc/pf-xivo/web-interface/cti.ini'
    CTI_INI_CONTENT_RESULT = """\
; XIVO: FILE AUTOMATICALLY GENERATED BY THE XIVO CONFIGURATION SUBSYSTEM
[general]
datastorage = "postgresql://xivo:proformatique@localhost/xivo?encoding=utf8"

[queuelogger]
datastorage = "postgresql://asterisk:proformatique@localhost/asterisk?charset=utf8"

"""

    def test_cti_conf_generation(self):
        self.assertTrue(os.access(self.CTI_INI_FILE, os.R_OK))
        with open(self.CTI_INI_FILE) as fobj:
            cti_ini_content = fobj.read()
        self.assertEqual(cti_ini_content, self.CTI_INI_CONTENT_RESULT)


class TestAsterisk(unittest.TestCase):

    def test_core_reload(self):
        retcode = subprocess.call(['asterisk', '-rx', 'core reload'])
        assert(retcode == 0)

