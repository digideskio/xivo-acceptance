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

from lettuce import step, world

from xivo_acceptance.lettuce import common, form


@step(u'Then ([a-z ]*) "([^"]*)" is displayed in the list$')
def then_value_is_displayed_in_the_list(step, module, search):
    query = {'search': search.encode('utf-8')}
    try:
        assert common.element_is_in_list(module, search, query)
    except AssertionError:
        world.dump_current_page()
        raise


@step(u'Then ([a-z ]*) "([^"]*)" is not displayed in the list$')
def then_value_is_not_displayed_in_the_list(step, module, search):
    query = {'search': search.encode('utf-8')}
    try:
        assert common.element_is_not_in_list(module, search, query)
    except AssertionError:
        world.dump_current_page()
        raise


@step(u'Then the search results are:')
def then_the_search_results_are(step):
    expected_list = [info['present'] for info in step.hashes if info['present']]
    not_expected_list = [info['not present'] for info in step.hashes if info['not present']]

    for expected in expected_list:
        assert common.find_line(expected) is not None

    for not_expected in not_expected_list:
        assert common.find_line(not_expected) is None, 'element %s unexpectedly found' % not_expected


@step(u'Then I see no errors')
def then_i_see_no_errors(step):
    # this step is there mostly for test readability; it's a no-op in most cases
    # since it's already checked when a form is submitted
    form.submit.assert_no_form_errors()


@step(u'Then I see errors')
def then_i_see_errors(step):
    form.submit.assert_form_errors()


@step(u'When I submit the form')
def when_i_submit_the_form(step):
    form.submit.submit_form()
