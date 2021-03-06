# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
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

import time

from lettuce.registry import world
from xivo_acceptance.lettuce import common


def configure_proxies(config):
    fields = {
        'http_proxy': 'http proxy',
        'ftp_proxy': 'ftp proxy',
        'https_proxy': 'https proxy',
    }

    for input_name, config_name in fields.items():
        element = world.browser.find_element_by_name(input_name)
        element.clear()
        element.send_keys(config.get(config_name, ''))
        time.sleep(3)


def configure_rest_api(config):
    """
        VALID FIELDS:
            'net4_ip_rest',
            'rest_port',
            'private',
            'username',
            'password',
            'secure'
    """

    for input_name, input_value in config.items():
        element = world.browser.find_element_by_id('it-provd-%s' % input_name)
        element.clear()
        element.send_keys(input_value)


def type_plugin_server_url(url):
    world.browser.find_element_by_name('plugin_server', 'plugin_server form not loaded')
    input_plugin_server = world.browser.find_element_by_name('plugin_server')
    input_plugin_server.clear()
    input_plugin_server.send_keys(url)
    time.sleep(2)


def update_plugin_server_url(url):
    common.open_url('provd_general')
    type_plugin_server_url(url)
