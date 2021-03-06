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

from hamcrest import assert_that
from hamcrest import equal_to
from lettuce import step, world

from xivo_acceptance.action.webi import user as user_action_webi
from xivo_acceptance.lettuce import common

import logging

logger = logging.getLogger(__name__)


@step(u'Given the user "([^"]*)" with the following func keys:')
def given_the_user_firstname_with_the_following_func_keys(step, username):
    firstname, lastname = username.split()
    user = world.confd_client.users.list(firstname=firstname, lastname=lastname)['items'][0]
    for line_number, line in enumerate(step.hashes, 1):
        funckey = _build_funckey(line)
        world.confd_client.users(user['uuid']).update_funckey(line_number, funckey)


def _build_funckey(line):
    type_ = line['destination_type']
    if type_ == 'forward':
        exten = line['destination_exten'] if line['destination_exten'] else None
        destination = {'type': type_,
                       'forward': line['destination_forward'],
                       'exten': exten}
    elif type_ == 'service':
        destination = {'type': type_,
                       'service': line['destination_service']}

    str_bool = {'true': True,
                'false': False}

    return {'blf': str_bool.get(line.get('blf')),
            'label': line.get('label'),
            'destination': destination}


@step(u'Then the user "([^"]*)" has the following func keys:')
def then_the_user_group1_has_the_following_func_keys(step, user):
    common.open_url('user', 'search', {'search': user})
    common.edit_line(user)
    common.go_to_tab('Func Keys')
    for line_number, line in enumerate(step.hashes, 1):
        _check_func_key(line, line_number)


def _check_func_key(info, line_number):
    line = user_action_webi.find_func_key_line(line_number)

    key_num = info['Key']
    key_type = info['Type']
    key_label = info['Label']
    key_destination = info['Destination']
    key_supervision = info['Supervision']

    key_num_field = user_action_webi.find_key_number_field(line)
    value = _extract_dropdown_value(key_num_field)
    assert_that(value, equal_to(key_num), "func key num differs (%s instead of %s)" % (value, key_num))

    key_type_field = user_action_webi.find_key_type_field(line)
    value = _extract_dropdown_value(key_type_field)
    assert_that(value, equal_to(key_type), "func key type differs (%s instead of %s)" % (value, key_type))

    destination_value = _extract_destination_value(key_type, line)
    assert_that(destination_value, equal_to(key_destination), "func key destination differs (%s instead of %s)" % (value, key_destination))

    key_label_field = user_action_webi.find_key_label_field(line)
    value = key_label_field.get_attribute('value')
    assert_that(value, equal_to(key_label), "func key label differs (%s instead of %s)" % (value, key_label))

    key_supervision_field = user_action_webi.find_key_supervision_field(line)
    value = _extract_dropdown_value(key_supervision_field)
    assert_that(value, equal_to(key_supervision), "func key supervision differs (%s instead of %s)" % (value, key_supervision))


def _extract_dropdown_value(dropdown):
    return dropdown.first_selected_option.text


def _extract_destination_value(key_type, line):
    key_destination_field = user_action_webi.find_key_destination_field(key_type, line)
    if key_type == 'Filtering Boss - Secretary':
        value = _extract_dropdown_value(key_destination_field)
    else:
        value = key_destination_field.get_attribute('value')

    return value
