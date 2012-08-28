# -*- coding: UTF-8 -*-

import socket
import xivo_ws

from lettuce.registry import world
from xivo_lettuce.terrain import _read_config
from xivo_ws.objects.siptrunk import SIPTrunk
from xivo_lettuce.manager.context_manager import add_contextnumbers_queue, \
    add_contextnumbers_user
from xivo_lettuce.ssh import SSHClient


def main():
    config = _read_config()
    Prerequisite(config)


class Prerequisite(object):

    def __init__(self, config):
        world.callgen_host = config.get('callgen', 'hostname')
        world.xivo_host = config.get('xivo', 'hostname')
        login = config.get('webservices_infos', 'login')
        password = config.get('webservices_infos', 'password')
        world.ws = xivo_ws.XivoServer(world.xivo_host, login, password)

        add_contextnumbers_queue('statscenter', 5000, 5100)
        add_contextnumbers_user('statscenter', 1000, 1100)

        callgen_ip = socket.gethostbyname(world.callgen_host)
        self.add_trunksip(callgen_ip, 'to_default', 'default')
        self.add_trunksip(callgen_ip, 'to_statscenter', 'statscenter')

        self._setup_ssh_client(config)

    def add_trunksip(self, host, name, context):
        trunksip_exist = self.has_trunksip(name)
        if len(trunksip_exist) == 1:
            self.del_trunksip(trunksip_exist[0].id)
        sip_trunk = SIPTrunk()
        sip_trunk.name = name
        sip_trunk.username = sip_trunk.name
        sip_trunk.secret = sip_trunk.name
        sip_trunk.context = context
        sip_trunk.host = host
        sip_trunk.type = 'friend'
        world.ws.sip_trunk.add(sip_trunk)

    def has_trunksip(self, name):
        return world.ws.sip_trunk.search(name)

    def del_trunksip(self, trunk_id):
        world.ws.sip_trunk.delete(trunk_id)

    def _setup_ssh_client(self, config):
        login = config.get('ssh_infos', 'login')
        ssh_client = SSHClient(world.xivo_host, login)
        self._create_pgpass_on_remote_host(ssh_client)

    def _create_pgpass_on_remote_host(self, ssh_client):
        cmd = ['echo', '*:*:asterisk:asterisk:proformatique', '>', '.pgpass']
        ssh_client.check_call(cmd)
        cmd = ['chmod', '600', '.pgpass']
        ssh_client.check_call(cmd)


if __name__ == '__main__':
    main()
