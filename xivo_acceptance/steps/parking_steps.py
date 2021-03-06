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

from lettuce import step

from xivo_acceptance.action.webi import parking as parking_action_webi


@step(u'When I change the parking configuration to be:')
def when_i_change_the_parking_configuration_to_be(step):
    parking_configuration = step.hashes[0]
    parking_action_webi.set_parking_config(parking_configuration)


@step(u'Then asterisk should have the following parking configuration:')
def then_asterisk_should_have_the_following_parking_configuration(step):
    expected_parking_info = step.hashes[0]
    parking_action_webi.check_parking_info(expected_parking_info)
