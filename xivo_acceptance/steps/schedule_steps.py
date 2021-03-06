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

from lettuce import step

from xivo_acceptance.action.webi import schedule as schedule_action_webi
from xivo_acceptance.helpers import schedule_helper


@step(u'Given I have a schedule "([^"]*)" in "([^"]*)" with the following schedules:')
def given_i_have_a_schedule_group1_in_group2_with_the_following_schedules(step, name, timezone):
    schedule_helper.add_schedule(name, timezone, step.hashes)


@step(u'Given I have a schedule "([^"]*)" in "([^"]*)" towards user "([^"]*)" "([^"]*)" with the following schedules:')
def given_i_have_a_schedule_group1_in_group2_towards_user_group3_group4_with_the_following_schedules(step, name, timezone, firstname, lastname):
    destination = schedule_helper.ScheduleDestinationUser.from_name(firstname, lastname)
    schedule_helper.add_schedule(name, timezone, step.hashes, destination)


@step(u'Given there are schedules:')
def given_there_are_schedules(step):
    for data in step.hashes:
        schedule_helper.add_or_replace_schedule(data)


@step(u'When I delete the "([^"]*)" "([^"]*)" schedule from "([^"]*)"')
def when_i_delete_the_group1_group2_schedule(step, order, status, name):
    if order != 'Second':
        assert False, 'This step not completely implemented'
    if status == 'Closed':
        schedule_action_webi.remove_closed_schedule(name, 2)
    elif status == 'Opened':
        schedule_action_webi.remove_opened_schedule(name, 2)
    else:
        assert False, 'Unknown schedule status %s' % status


@step(u'Then I should have a schedule "([^"]*)" in "([^"]*)" with the following schedules:')
def then_i_should_have_a_schedule_group1_in_group2_with_the_following_schedules(step, name, timezone):
    schedule_helper.assert_schedule_exists(name, timezone, step.hashes)
