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

from lettuce import step

from xivo_acceptance.action.webi import directory as directory_action_webi
from xivo_acceptance.helpers import cti_helper
from xivo_acceptance.helpers import directory_helper
from xivo_acceptance.lettuce import assets, common, sysutils
from xivo_acceptance.lettuce.form import submit


@step(u'Given a reverse lookup test configuration')
def given_a_reverse_lookup_test_configuration(step):
    model_name = 'test'
    cti_helper.add_call_form_model(model_name, ['xivo-calleridnum',
                                                'xivo-calleridname'])
    cti_helper.set_call_form_model_on_event(model_name, 'Link')


@step(u'Given the following directory configurations exist:')
def given_the_following_directories_exist(step):
    for directory in step.hashes:
        directory_action_webi.add_or_replace_directory_config(directory)


@step(u'Given the following directories are used in reverse lookup:')
def given_the_following_directories_are_used_in_reverse_lookup(step):
    directories = [entry['directory'] for entry in step.hashes]
    directory_action_webi.set_reverse_directories(directories)
    submit.submit_form()


@step(u'Given the directory definition "([^"]*)" does not exist')
def given_the_directory_definition_does_not_exist(step, definition):
    directory_action_webi.remove_directory(definition)


@step(u'Given the CSV file "([^"]*)" is copied on the server into "([^"]*)"')
def given_the_csv_file_is_copied_on_the_server_into_group2(step, csvfile, serverpath):
    assets.copy_asset_to_server(csvfile, serverpath)


@step(u'Given the internal directory exists')
def given_the_internal_directory_exists(step):
    directory_helper.configure_internal_directory()


@step(u'Given the directory definition "([^"]*)" is included in the default directory')
def given_the_directory_definition_group1_is_included_in_the_default_directory(step, definition):
    directory_action_webi.assign_filter_and_directories_to_context(
        'default',
        'Display',
        [definition]
    )


@step(u'When I create the following directory configurations:')
def when_i_configure_the_following_directories(step):
    for directory in step.hashes:
        directory_action_webi.add_or_replace_directory_config(directory)


@step(u'When I edit and save the directory configuration "([^"]*)"')
def when_i_edit_and_save_the_directory(step, directory):
    common.open_url('directory_config', 'list')
    common.edit_line(directory)
    submit.submit_form()


@step(u'Given I add the following CTI directory definition:')
def given_i_add_the_following_cti_directory_definition(step):
    for directory in step.hashes:
        directory_action_webi.add_directory_definition(directory)


@step(u'Given I map the following fields and save the directory definition:')
def given_i_map_the_following_fields_and_save_the_directory_definition(step):
    for field in step.hashes:
        directory_action_webi.add_field(field['field name'], field['value'])
    submit.submit_form()


@step(u'When I include "([^"]*)" in the default directory')
def when_i_include_phonebook_in_the_default_directory(step, phonebook):
    directory_action_webi.assign_filter_and_directories_to_context(
        'default',
        'Display',
        [phonebook]
    )


@step(u'When I set the following directories for directory reverse lookup:')
def when_i_set_the_following_directories_for_directory_reverse_lookup(step):
    directories = [entry['directory'] for entry in step.hashes]
    directory_action_webi.set_reverse_directories(directories)
    sysutils.restart_service('xivo-dird')


@step(u'Then the directory configuration "([^"]*)" has the URI "([^"]*)"')
def then_the_directory_has_the_uri(step, directory, uri):
    line = common.get_line(directory)
    cells = line.find_elements_by_tag_name("td")
    uri_cell = cells[2]
    assert uri_cell.text == uri
