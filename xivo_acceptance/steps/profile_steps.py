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

from hamcrest import *
from lettuce import step
from selenium.common.exceptions import NoSuchElementException

from xivo_acceptance.action.webi import profile as profile_action_webi
from xivo_acceptance.lettuce import common, form
from xivo_acceptance.helpers import cti_helper


@step(u'Given there is a profile "([^"]*)" with no services and xlets:')
def given_there_is_a_profile_1_with_no_services_and_xlets(step, profile_name):
    profile_action_webi.delete_profile_if_exists(profile_name)
    common.open_url('profile', 'add')
    profile_action_webi.type_profile_names(profile_name)
    profile_action_webi.remove_all_services()
    common.go_to_tab('Xlets')
    cti_profile_config = step.hashes
    for cti_profile_element in cti_profile_config:
        xlet_name = cti_profile_element['xlet']
        xlet_position = cti_profile_element.get('position', 'dock')
        profile_action_webi.add_xlet(xlet_name, xlet_position)
    form.submit.submit_form()


@step(u'When I add Xlet "([^"]*)" to profile "([^"]*)"')
def when_i_add_xlet_to_profile(step, xlet_name, profile_name):
    common.open_url('profile', 'list')
    common.edit_line(profile_name)
    common.go_to_tab('Xlets')
    profile_action_webi.add_xlet(xlet_name)
    form.submit.submit_form()


@step(u'When I add the CTI profile "([^"]*)"')
def when_i_add_the_cti_profile_1(step, profile_name):
    common.open_url('profile', 'add')
    profile_action_webi.type_profile_names(profile_name)
    form.submit.submit_form()


@step(u'Then I can\'t remove profile "([^"]*)"')
def then_i_see_errors(step, profile_label):
    common.open_url('profile', 'list')
    table_line = common.get_line(profile_label)
    try:
        table_line.find_element_by_xpath(".//a[@title='Delete']")
    except NoSuchElementException:
        pass
    else:
        raise Exception('CTI profile %s should not be removable' % profile_label)


@step(u'Then I don\'t see xlet "([^"]*)"')
def then_i_don_t_see_xlet_group1(step, xlet):
    res = cti_helper.get_xlets()
    assert_that(res['xlets'], not has_item(xlet))


@step(u'Then I see xlet "([^"]*)"')
def then_i_see_xlet_group1(step, xlet):
    res = cti_helper.get_xlets()
    assert_that(res['xlets'], has_item(xlet))
