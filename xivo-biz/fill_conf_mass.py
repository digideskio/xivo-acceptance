#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import os
import xivo_ws
import subprocess

from lettuce.registry import world
from xivo_lettuce import terrain
from xivo_lettuce.manager_ws import context_manager_ws, user_manager_ws, \
    trunkcustom_manager_ws
from xivo_lettuce.ssh import SSHClient
from xivo_ws.objects.incall import Incall
from xivo_ws.objects.outcall import Outcall, OutcallExten
from xivo_ws.destination import UserDestination
from xivo_lettuce.manager_dao import user_manager_dao

_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))


def main():
    Prerequisite(terrain.read_config())


class Prerequisite(object):

    def __init__(self, config):
        hostname = config.get('xivo_biz', 'hostname')
        world.xivo_host = hostname
        login = config.get('ssh_infos', 'login')
        world.ssh_client_xivo = SSHClient(hostname, login)

        login = config.get('webservices_infos', 'login')
        password = config.get('webservices_infos', 'password')
        world.ws = xivo_ws.XivoServer(hostname, login, password)

        self._init_webservices()
        self._create_pgpass_on_remote_host()

        self._check_configuration_dahdi()
        self._configuration_dahdi()

        self._prepare_context()
        self._prepare_trunk()
        self._prepare_user()
        self._prepare_outcall()
        self._prepare_incall()

        print 'Configuration finished.'

    def _prepare_context(self):
        print 'Configuring Context..'
        context_manager_ws.update_contextnumbers_user('default', 100, 199)
        context_manager_ws.update_contextnumbers_incall('from-extern', 1000, 2000, 4)

    def _prepare_trunk(self):
        print 'Configuring Trunk..'
        data1 = {'name': 'dahdi-g1',
                 'interface': 'dahdi/g1'
                 }
        trunkcustom_manager_ws.add_or_replace_trunkcustom(data1)
        data2 = {'name': 'dahdi-g2',
                 'interface': 'dahdi/g2'
                 }
        trunkcustom_manager_ws.add_or_replace_trunkcustom(data2)

    def _prepare_user(self):
        print 'Configuring User..'
        user_data_tpl = {
            'firstname': 'user',
            'line_context': 'default',
            'enable_client': True,
            'client_password': '12345',
            'client_profile': 'client'
        }
        nb_user = 10
        user_increment = range(0, nb_user)
        for i in user_increment:
            user_data = {'lastname': '%i' % (i),
                         'line_number': '10%i' % (i),
                         'client_username': 'user%i' % (i)}
            user_data.update(user_data_tpl)
            user_exist = user_manager_dao.is_user_with_name_exists('user', '%i' % (i))
            if not user_exist:
                user_manager_ws.add_user(user_data)

            line = world.ws.lines.search('10%s' % (i))

            print
            print 'User%s line infos:' % (i)
            print 'Name: %s' % line[0].name
            print 'Secret: %s' % line[0].secret
            print

    def _prepare_incall(self):
        print 'Configuring Incall..'
        nb_incall = 1
        incall_increment = range(0, nb_incall)
        for i in incall_increment:
            incall_exist = world.ws.incalls.search('100%s' % (i))
            if not incall_exist:
                incall = Incall()
                incall.number = '100%s' % (i)
                incall.context = 'from-extern'
                incall.destination = UserDestination(line_manager_dao.find_line_id_with_exten_context('10%s' % (i), 'default'))
                world.ws.incalls.add(incall)

    def _prepare_outcall(self):
        print 'Configuring Outcall..'
        outcall_exist = world.ws.outcalls.search('to_dahdi')
        if not outcall_exist:
            outcall = Outcall()
            outcall.name = 'to_dahdi'
            outcall.context = 'to-extern'
            outcall.trunks = [trunkcustom_manager_ws.find_trunkcustom_id_with_name('dahdi-g2')]
            outcall.extens = [OutcallExten(exten='6XXXX', stripnum=1)]
            world.ws.outcalls.add(outcall)

    def _init_webservices(self):
        ws_sql_file = os.path.join(_ROOT_DIR, 'utils', 'webservices.sql')
        cmd = ['scp', ws_sql_file, 'root@%s:/tmp/' % world.xivo_host]
        self._exec_ssh_cmd(cmd)
        cmd = ['sudo', '-u', 'postgres', 'psql', '-f', '/tmp/webservices.sql']
        world.ssh_client_xivo.check_call(cmd)

    def _create_pgpass_on_remote_host(self):
        cmd = ['echo', '*:*:asterisk:asterisk:proformatique', '>', '.pgpass']
        world.ssh_client_xivo.check_call(cmd)
        cmd = ['chmod', '600', '.pgpass']
        world.ssh_client_xivo.check_call(cmd)

    def _configuration_dahdi(self):
        print 'Configuring Dahdi..'
        cmd = ['dahdi_genconf']
        world.ssh_client_xivo.check_call(cmd)
        cmd = ['sed', '-i', '"s/,crc4//g"', '/etc/dahdi/system.conf']
        world.ssh_client_xivo.check_call(cmd)
        cmd = ['sed', '-i', '"s/group=0,11/group=1/g"', '/etc/asterisk/dahdi-channels.conf']
        world.ssh_client_xivo.check_call(cmd)
        cmd = ['sed', '-i', '"s/group=0,12/group=2/g"', '/etc/asterisk/dahdi-channels.conf']
        world.ssh_client_xivo.check_call(cmd)
        cmd = ['sed', '-i', '"s/context = default//g"', '/etc/asterisk/dahdi-channels.conf']
        world.ssh_client_xivo.check_call(cmd)
        cmd = ['sed', '-i', '"s/group = 63//g"', '/etc/asterisk/dahdi-channels.conf']
        world.ssh_client_xivo.check_call(cmd)
        cmd = ['sed', '-i', '"23s/pri_cpe/pri_net/"', '/etc/asterisk/dahdi-channels.conf']
        world.ssh_client_xivo.check_call(cmd)
        cmd = ['xivo-service', 'restart']
        print 'Wait during xivo-service restart'
        world.ssh_client_xivo.check_call(cmd)
        cmd = ['asterisk', '-rx', '"dahdi show status"']
        res = world.ssh_client_xivo.out_call(cmd)
        print 'result of "dahdi show status": %s' % res

    def _check_configuration_dahdi(self):
        cmd = ['lspci', '|', 'grep', 'Digium']
        world.ssh_client_xivo.check_call(cmd)

    def _exec_ssh_cmd(self, cmd):
        p = subprocess.Popen(cmd,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)

        (stdoutdata, stderrdata) = p.communicate()

        if p.returncode != 0:
            print stdoutdata
            print stderrdata

        return stdoutdata


if __name__ == '__main__':
    main()
