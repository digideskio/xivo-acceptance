# -*- coding: utf-8 -*-

# Copyright (C) 2013-2015 Avencall
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

import logging

from lettuce import world

from xivo_acceptance.helpers import context_helper
from xivo_acceptance.lettuce import common
from xivo_acceptance.lettuce import setup
from xivo_acceptance.lettuce.assets import copy_asset_to_server
from xivo_acceptance.lettuce.terrain import _check_webi_login_root
from xivo_dao.helpers import db_manager
from xivo_dao.helpers.db_utils import session_scope


logger = logging.getLogger(__name__)


def run():
    logger.debug('Initializing ...')
    setup.setup_config()
    setup.setup_logging()
    setup.setup_xivo_acceptance_config()
    setup.setup_ssh_client()
    setup.setup_ws()

    setup.setup_browser()
    try:
        _check_webi_login_root()

        logger.debug('Configuring WebService Access on XiVO')
        _create_webservices_access()

        logger.debug('Configuring Consul')
        _configure_consul()

        logger.debug('Configuring PostgreSQL on XiVO')
        _create_pgpass_on_remote_host()
        _allow_remote_access_to_pgsql()

        logger.debug('Configuring RabbitMQ on XiVO')
        copy_asset_to_server('rabbitmq.config', '/etc/rabbitmq/rabbitmq.config')

        logger.debug('Configuring xivo-agid on XiVO')
        _allow_agid_listen_on_all_interfaces()

        logger.debug('Configuring Provd REST API on XiVO')
        _allow_provd_listen_on_all_interfaces()

        logger.debug('Installing packages')
        _install_packages(['tcpflow'])

        logger.debug('Installing chan_test (module for asterisk)')
        copy_asset_to_server('chan_test.so', '/usr/lib/asterisk/modules/chan_test.so')

        logger.debug('Adding xivo-acceptance key')
        copy_asset_to_server('xivo-acceptance-key.yml', '/var/lib/xivo-auth-keys')

        logger.debug('Adding context')
        context_helper.update_contextnumbers_queue('statscenter', 5000, 5100)
        context_helper.update_contextnumbers_user('statscenter', 1000, 1100)
        context_helper.update_contextnumbers_user('default', 1000, 1999)
        context_helper.update_contextnumbers_group('default', 2000, 2999)
        context_helper.update_contextnumbers_queue('default', 3000, 3999)
        context_helper.update_contextnumbers_meetme('default', 4000, 4999)
        context_helper.update_contextnumbers_incall('from-extern', 1000, 4999, 4)

        logger.debug('Configuring xivo-auth')
        _configure_xivo_auth()

        logger.debug('Configuring xivo-ctid')
        _configure_xivo_ctid()

        logger.debug('Restarting All XiVO Services')
        _xivo_service_restart_all()
    finally:
        setup.teardown_browser()


def _create_webservices_access():
    copy_asset_to_server('webservices.sql', '/tmp')
    cmd = ['sudo', '-u', 'postgres', 'psql', '-f', '/tmp/webservices.sql']
    world.ssh_client_xivo.check_call(cmd)


def _create_pgpass_on_remote_host():
    cmd = ['echo', '*:*:asterisk:asterisk:proformatique', '>', '.pgpass']
    world.ssh_client_xivo.check_call(cmd)
    cmd = ['chmod', '600', '.pgpass']
    world.ssh_client_xivo.check_call(cmd)


def _allow_remote_access_to_pgsql():
    hba_file = '/etc/postgresql/9.4/main/pg_hba.conf'
    postgres_conf_file = '/etc/postgresql/9.4/main/postgresql.conf'

    subnet_line = 'host all all {subnet} md5'
    for subnet in world.config['prerequisites']['subnets']:
        _add_line_to_remote_file(subnet_line.format(subnet=subnet), hba_file)

    _add_line_to_remote_file("listen_addresses = '*'", postgres_conf_file)

    command = ['service', 'postgresql', 'restart']
    world.ssh_client_xivo.check_call(command)
    db_manager.init_db(world.config['db_uri'])


def _add_line_to_remote_file(line_text, file_name):
    command = ['grep', '-F', '"%s"' % line_text, file_name, '||', '$(echo "%s" >> %s)' % (line_text, file_name)]
    world.ssh_client_xivo.check_call(command)


def _xivo_service_restart_all():
    command = ['xivo-service', 'restart', 'all']
    world.ssh_client_xivo.check_call(command)


def _allow_agid_listen_on_all_interfaces():
    _add_line_to_remote_file('listen_address: 0.0.0.0', '/etc/xivo-agid/conf.d/acceptance.yml')


def _allow_provd_listen_on_all_interfaces():
    with session_scope() as session:
        query = 'UPDATE provisioning SET net4_ip_rest = \'0.0.0.0\''
        session.execute(query)
    common.open_url('commonconf')


def _install_packages(packages):
    command = ['apt-get', 'update', '&&', 'apt-get', 'install', '-y']
    command.extend(packages)
    world.ssh_client_xivo.check_call(command)


def _configure_consul():
    copy_asset_to_server('public_consul.json', '/etc/consul/xivo/public_consul.json')
    command = 'service consul restart'.split()
    world.ssh_client_xivo.check_call(command)


def _configure_xivo_auth():
    _copy_daemon_config_file('xivo-auth')


def _configure_xivo_ctid():
    _copy_daemon_config_file('xivo-ctid')


def _copy_daemon_config_file(daemon_name):
    asset_filename = '{}-acceptance.yml'.format(daemon_name)
    remote_path = '/etc/{}/conf.d'.format(daemon_name)
    copy_asset_to_server(asset_filename, remote_path)
