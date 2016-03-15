# -*- coding: utf-8 -*-

# Copyright (C) 2013-2016 Avencall
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
import os
import tempfile
import sys

from lettuce import before, after, world
from selenium.common.exceptions import NoSuchElementException
from xivo_acceptance.helpers import asterisk_helper
from xivo_acceptance.lettuce import asterisk
from xivo_acceptance.lettuce import common
from xivo_acceptance.lettuce import debug
from xivo_acceptance.lettuce import setup
from xivo_acceptance.lettuce.phone_register import PhoneRegister


logger = logging.getLogger('acceptance')


@before.all
def xivo_acceptance_lettuce_before_all():
    initialize()


@before.each_scenario
def xivo_acceptance_lettuce_before_each_scenario(scenario):
    scenario.phone_register = PhoneRegister()
    setup.setup_browser()
    _check_webi_login_root()
    world.deleted_device = None


@after.each_step
def xivo_acceptance_lettuce_after_each_step(step):
    sys.stdout.flush()


@after.each_scenario
def xivo_acceptance_lettuce_after_each_scenario(scenario):
    asterisk.stop_ami_monitoring()
    scenario.phone_register.clear()
    xc = getattr(scenario, '_pseudo_xivo_client', None)
    if xc:
        xc.stop()
    _logout_agents()


@after.all
def xivo_acceptance_lettuce_after_all(total):
    deinitialize()


def initialize():
    setup.setup_config()
    setup.setup_logging()

    logger.info("Initializing acceptance tests...")
    logger.info('xivo_host: %s', world.config['xivo_host'])

    setup.setup_xivo_acceptance_config()

    logger.debug("setup ssh client...")
    setup.setup_ssh_client()
    logger.debug("setup ws...")
    setup.setup_ws()
    logger.debug("setup provd...")
    setup.setup_provd()
    logger.debug("setup browser...")
    setup.setup_browser()
    logger.debug("setup auth token...")
    setup.setup_auth_token()
    logger.debug("setup agentd client...")
    setup.setup_agentd_client()
    logger.debug("setup consul...")
    setup.setup_consul()
    world.logged_agents = []
    world.dummy_ip_address = '10.99.99.99'


@debug.logcall
def _check_webi_login_root():
    if world.config['browser']['enable'] and world.xivo_acceptance_config.xivo_configured:
        try:
            element = world.browser.find_element_by_xpath('//h1[@id="loginbox"]/span[contains(.,"Login")]/b')
            username = element.text
        except NoSuchElementException:
            common.webi_login_as_default()
        else:
            if username != "root":
                common.webi_logout()
                common.webi_login_as_default()


@debug.logcall
def _logout_agents():
    asterisk_helper.logoff_agents(world.logged_agents)
    world.logged_agents = []


@debug.logcall
def deinitialize():
    setup.teardown_browser()


@debug.logcall
@world.absorb
def dump_current_page(dirname='lettuce-dump-'):
    """
    Use this if you want to debug your test.
    Call it with world.dump_current_page().
    """
    dump_dir = tempfile.mkdtemp(prefix=dirname, dir=world.config['output_dir'])

    source_file_name = os.path.join(dump_dir, 'page-source.html')
    with open(source_file_name, 'w') as fobj:
        fobj.write(world.browser.page_source.encode('utf-8'))

    image_file_name = os.path.join(dump_dir, 'screenshot.png')
    world.browser.save_screenshot(image_file_name)

    logger.info('Debug files dumped in {}'.format(dump_dir))
