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

from xivo_acceptance.helpers import asterisk_helper
from xivo_acceptance.lettuce import form, common


def set_parking_config(config_map):
    common.open_url('extenfeatures')
    common.go_to_tab('Advanced', 'Parking')

    form.input.set_text_field_with_label('Extension', config_map['Extension'])

    form.select.set_select_field_with_label('Wait delay', config_map['Wait delay'])

    range_start = config_map['Range start']
    range_end = config_map['Range end']

    parking_range = '-'.join([range_start, range_end])
    form.input.set_text_field_with_label('Extension to park calls', parking_range)

    enable_hints = config_map['Parkings hints'] == 'enabled'
    common.the_option_is_checked('Parkings hints', None, given=enable_hints)

    form.submit.submit_form()


def check_parking_info(expected_parking_info):
    output = asterisk_helper.check_output_asterisk_cli('parking show')
    parking_info = _parse_parking_info(output)

    assert_that(parking_info, has_entries(expected_parking_info))


def _parse_parking_info(asterisk_output):
    parking_info = {}
    for line in asterisk_output.split('\n'):
        if ':' not in line:
            continue
        field, value = line.split(':', 1)
        field = field.strip()
        value = value.strip()
        parking_info[field] = value

    return parking_info
