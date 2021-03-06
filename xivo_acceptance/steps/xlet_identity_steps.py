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

from hamcrest import assert_that, is_not, equal_to, is_
from lettuce import step, world


@step(u'Then the Xlet identity shows name as "([^"]*)" "([^"]*)"')
def then_the_xlet_identity_shows_name_as_1_2(step, firstname, lastname):
    assert world.xc_identity_infos['fullname'] == '%s %s' % (firstname, lastname)


@step(u'Then the Xlet identity shows a voicemail "([^"]*)"')
def then_the_xlet_identity_shows_a_voicemail_1(step, vm_number):
    assert_that(world.xc_identity_infos['voicemail_num'], is_not(equal_to('')))
    assert_that(world.xc_identity_infos['voicemail_button'], is_(True))


@step(u'Then the Xlet identity shows an agent')
def then_the_xlet_identity_shows_an_agent_1(step):
    assert_that(world.xc_identity_infos['agent_button'], is_(True))


@step(u'Then the Xlet identity does not show any agent')
def then_the_xlet_identity_does_not_show_any_agent(step):
    assert_that(world.xc_identity_infos['agent_button'], is_(False))
