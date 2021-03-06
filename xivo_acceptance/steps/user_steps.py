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
from hamcrest import is_
from lettuce import step
from lettuce.registry import world
from selenium.webdriver.support.select import Select

from xivo_acceptance.action.confd import user_action_confd
from xivo_acceptance.action.webi import user as user_action_webi
from xivo_acceptance.helpers import user_helper
from xivo_acceptance.helpers import user_line_extension_helper as ule_helper
from xivo_acceptance.lettuce import common, form


@step(u'^Given there are users with infos:$')
def given_there_are_users_with_infos(step):
    """step: Given there are users with infos:

    :param step: hashes
    :type step: list

    .. note::
        note

    :Example:

    Scenario: Create Users
        Given there are users with infos:
        | firstname | lastname | number | context | ... |

    Columns are:
        entity_name
        firstname
        lastname
        number
        context
        cti_profile
        cti_login
        cti_passwd
        agent_number
        language
        voicemail_name
        voicemail_number
        mobile_number
        group_name
        group_chantype
        protocol
        device
    """
    for user_data in step.hashes:
        user_helper.add_user_with_infos(user_data, step=step)


@step(u'Given I have the following users:')
def given_i_have_the_following_users(step):
    for userinfo in step.hashes:
        user_helper.add_or_replace_user(userinfo)


@step(u'Given there is no user "([^"]*)" "([^"]*)"$')
def given_there_is_a_no_user_1_2(step, firstname, lastname):
    ule_helper.delete_user_line_extension_voicemail(firstname, lastname)


@step(u'Given user "([^"]*)" "([^"]*)" has the following function keys:')
def given_user_has_the_following_function_keys(step, firstname, lastname):
    _add_func_keys_to_user(step.hashes, firstname, lastname)


def _add_func_keys_to_user(hashes, firstname, lastname):
    common.open_url('user', 'search', {'search': '%s %s' % (firstname, lastname)})
    common.edit_line("%s %s" % (firstname, lastname))
    name_map = {
        'Key': 'key_number',
        'Type': 'key_type',
        'Destination': 'destination',
        'Label': 'label',
        'Supervision': 'supervised',
    }
    for key_definition in hashes:
        key = dict((name_map[k], v) for k, v in key_definition.iteritems())
        user_action_webi.type_func_key(**key)
    form.submit.submit_form()


@step(u'Given "([^"]*)" has a dialaction on "([^"]*)" to "([^"]*)" "([^"]*)"')
def given_user_has_a_dialaction(step, fullname, event, dialaction, destination):
    _edit_user(*fullname.split(' ', 1))
    common.go_to_tab('No answer')

    if event == 'No answer':
        action_type = 'noanswer'
    elif event == 'Busy':
        action_type = 'busy'
    else:
        raise NotImplementedError('%s dialaction is not implemented' % event)

    if dialaction != 'User':
        raise NotImplementedError('%s dialaction destination is not implemented' % destination)

    action_type_id = 'it-dialaction-%s-actiontype' % action_type
    action_destination_id = 'it-dialaction-%s-user-actionarg1' % action_type

    _select(action_type_id, dialaction)
    _select(action_destination_id, destination)

    form.submit.submit_form()


@step(u'Given "([^"]*)" has a "([^"]*)" ringing time')
def given_user_has_a_n_ringing_time(step, fullname, delay_string):
    _edit_user(*fullname.split(' ', 1))

    _select('it-userfeatures-ringseconds', delay_string)

    form.submit.submit_form()


def _select(id_, text):
    form.select.set_select_field_with_id(id_, text)


def _edit_user(firstname, lastname):
    user_id = user_helper.get_user_id_with_firstname_lastname(firstname, lastname)
    common.open_url('user', 'edit', qry={'id': user_id})


@step(u'Given user "([^"]*)" has schedule "([^"]*)"')
def given_user_1_has_schedule_2(step, fullname, schedule):
    user_action_webi.add_schedule(fullname, schedule)


@step(u'When I create users with the following parameters:$')
def when_i_create_users_with_the_following_parameters(step):
    for userinfo in step.hashes:
        world.response = user_action_confd.create_user(userinfo)


@step(u'When I update user "([^"]*)" "([^"]*)" with the following parameters:')
def when_i_update_user_group1_group2_with_the_following_parameters(step, firstname, lastname):
    user = user_helper.get_by_firstname_lastname(firstname, lastname)
    userinfo = _get_user_info(step.hashes)
    world.response = user_action_confd.update_user(user['id'], userinfo)


@step(u'When I reorder "([^"]*)" "([^"]*)"s function keys such that:')
def when_i_reorder_group1_group2_s_function_keys_such_that(step, firstname, lastname):
    common.open_url('user', 'search', {'search': '%s %s' % (firstname, lastname)})
    common.edit_line("%s %s" % (firstname, lastname))
    pairs = [(k['Old'], k['New']) for k in step.hashes]
    user_action_webi.change_key_order(pairs)
    form.submit.submit_form()


@step(u'When I create a user with infos:$')
def when_i_create_a_user(step):
    common.open_url('user', 'add')
    user_properties = step.hashes[0]
    user_action_webi.type_user_names(user_properties['firstname'], user_properties.get('lastname', ''))
    if 'number' in user_properties and 'context' in user_properties and 'protocol' in user_properties:
        user_action_webi.user_form_add_line(
            linenumber=user_properties['number'],
            context=user_properties['context'],
            protocol=user_properties['protocol'].upper(),
            device=user_properties.get('device', None),
            entity_displayname=user_properties.get('entity_displayname', None),
        )
    form.submit.submit_form()


@step(u'When I add a new line to user "([^"]*)" "([^"]*)" with infos:$')
def when_i_add_a_new_line_to_a_user(step, firstname, lastname):
    _edit_user(firstname, lastname)
    user_properties = step.hashes[0]
    common.go_to_tab('Lines')
    user_action_webi.remove_line()
    user_action_webi.user_form_add_line(
        linenumber=user_properties['number'],
        context=user_properties['context'],
        protocol=user_properties['protocol'].upper(),
        device=user_properties.get('device', None),
        entity_displayname=user_properties.get('entity_displayname', None),
    )
    form.submit.submit_form()


@step(u'When I rename "([^"]*)" "([^"]*)" to "([^"]*)" "([^"]*)"$')
def when_i_rename_user(step, orig_firstname, orig_lastname, dest_firstname, dest_lastname):
    user_id = user_helper.get_user_id_with_firstname_lastname(orig_firstname, orig_lastname)
    ule_helper.delete_user_line_extension_voicemail(dest_firstname, dest_lastname)
    common.open_url('user', 'edit', {'id': user_id})
    user_action_webi.type_user_names(dest_firstname, dest_lastname)
    form.submit.submit_form()


@step(u'When I remove user "([^"]*)" "([^"]*)"$')
def remove_user(step, firstname, lastname):
    world.user_id = user_helper.get_user_id_with_firstname_lastname(firstname, lastname)
    common.open_url('user', 'search', {'search': '%s %s' % (firstname, lastname)})
    common.remove_line('%s %s' % (firstname, lastname))
    common.open_url('user', 'search', {'search': ''})


@step(u'When I search for user "([^"]*)" "([^"]*)"')
def when_i_search_for_user_firstname_lastname(step, firstname, lastname):
    common.open_url('user', 'search', {'search': '%s %s' % (firstname, lastname)})


@step(u'When I search for user with number "([^"]*)"')
def when_i_search_for_user_with_number_group1(step, number):
    common.open_url('user', 'search', {'search': '%s' % number})


@step(u'When I delete agent number "([^"]*)"$')
def when_i_delete_agent_number_1(step, agent_number):
    agent = world.ws.agents.search(agent_number)[0]
    world.ws.agents.delete(agent.id)


@step(u'When I add a user "([^"]*)" "([^"]*)" with a function key with type Customized and extension "([^"]*)"$')
def when_i_add_a_user_group1_group2_with_a_function_key(step, firstname, lastname, extension):
    common.open_url('user', 'add')
    user_action_webi.type_user_names(firstname, lastname)
    user_action_webi.type_func_key('Customized', extension)
    form.submit.submit_form()


@step(u'When I remove line from user "([^"]*)" "([^"]*)"$')
def when_i_remove_line_from_user(step, firstname, lastname):
    _edit_user(firstname, lastname)
    user_action_webi.remove_line()
    form.submit.submit_form()


@step(u'When I modify the mobile number of user "([^"]*)" "([^"]*)" to "([^"]*)"')
def when_i_modify_the_mobile_number_of_user_1_2_to_3(step, firstname, lastname, mobile_number):
    _edit_user(firstname, lastname)
    user_action_webi.type_mobile_number(mobile_number)
    form.submit.submit_form()


@step(u'When I remove the mobile number of user "([^"]*)" "([^"]*)"')
def when_i_remove_the_mobile_number_of_user_group1_group2(step, firstname, lastname):
    _edit_user(firstname, lastname)
    user_action_webi.type_mobile_number('')
    form.submit.submit_form()


@step(u'When I modify the device of user "([^"]*)" "([^"]*)" to "([^"]*)"$')
def when_i_modify_the_device_of_user_group1_group2_to_group3(step, firstname, lastname, device):
    _edit_user(firstname, lastname)
    user_action_webi.type_device(device)
    form.submit.submit_form()


@step(u'When I modify the device slot of user "([^"]*)" "([^"]*)" to "([^"]*)"$')
def when_i_modify_the_device_slot_of_user_group1_group2_to_group3(step, firstname, lastname, device_slot):
    _edit_user(firstname, lastname)
    user_action_webi.select_device_slot(device_slot)
    form.submit.submit_form()


@step(u'When I modify the device of user "([^"]*)" "([^"]*)" to "([^"]*)" with device slot "([^"]*)"$')
def when_i_modify_the_device_and_device_slot_of_user_group1_group2_to_group3(step, firstname, lastname, device, device_slot):
    _edit_user(firstname, lastname)
    user_action_webi.type_device(device)
    user_action_webi.select_device_slot(device_slot)
    form.submit.submit_form()


@step(u'When I modify the extension of user "([^"]*)" "([^"]*)" to "([^"]*)"$')
def when_i_modify_the_extension_of_user_name_to_extension(step, firstname, lastname, new_extension):
    _edit_user(firstname, lastname)
    user_action_webi.type_line_number(new_extension)
    form.submit.submit_form()


@step(u'When I modify the extension of user "([^"]*)" "([^"]*)" to "([^"]*)" with errors$')
def when_i_modify_the_extension_of_user_name_to_extension_with_errors(step, firstname, lastname, new_extension):
    _edit_user(firstname, lastname)
    user_action_webi.type_line_number(new_extension)
    form.submit.submit_form_with_errors()


@step(u'When I remove the device of user "([^"]*)" "([^"]*)"')
def when_i_remove_the_device_of_user_group1_group2(step, firstname, lastname):
    _edit_user(firstname, lastname)
    user_action_webi.type_device('')
    form.submit.submit_form()


@step(u'Then "([^"]*)" "([^"]*)" is in group "([^"]*)"$')
def then_user_is_in_group(step, firstname, lastname, group_name):
    user_id = user_helper.get_user_id_with_firstname_lastname(firstname, lastname)
    assert user_helper.user_id_is_in_group_name(group_name, user_id)


@step(u'Then I should be at the user list page$')
def then_i_should_be_at_the_user_list_page(step):
    world.browser.find_element_by_id('bc-main', 'User list page not loaded')
    world.browser.find_element_by_name('fm-users-list')


@step(u'When I edit the user "([^"]*)" "([^"]*)" without changing anything')
def when_i_edit_the_user_1_2_without_changing_anything(step, firstname, lastname):
    _edit_user(firstname, lastname)
    form.submit.submit_form()


@step(u'Then I see the user "([^"]*)" "([^"]*)" exists$')
def then_i_see_the_user_group1_group2_exists(step, firstname, lastname):
    common.open_url('user', 'search', {'search': '%s %s' % (firstname, lastname)})
    user_line = common.find_line("%s %s" % (firstname, lastname))
    assert user_line is not None, 'User: %s %s does not exist' % (firstname, lastname)
    common.open_url('user', 'search', {'search': ''})


@step(u'Then the user "([^"]*)" "([^"]*)" not exist')
def then_the_user_not_exist(step, firstname, lastname):
    common.open_url('user', 'search', {'search': '%s %s' % (firstname, lastname)})
    user_line = common.find_line("%s %s" % (firstname, lastname))
    assert user_line is None, 'User: %s %s exist' % (firstname, lastname)
    common.open_url('user', 'search', {'search': ''})


@step(u'Then I see a user with infos:')
def then_i_see_a_user_with_infos(step):
    user_expected_properties = step.hashes[0]
    fullname = user_expected_properties['fullname']
    common.open_url('user', 'search', {'search': '%s' % fullname})
    user_actual_properties = user_action_webi.get_user_list_entry(fullname)
    assert_that(fullname, equal_to(user_expected_properties['fullname']))
    for user_field, user_value in user_expected_properties.iteritems():
        assert_that(user_actual_properties[user_field], equal_to(user_value))
    common.open_url('user', 'search', {'search': ''})


@step(u'Then i see user with username "([^"]*)" "([^"]*)" has a function key with type Customized and extension "([^"]*)"$')
def then_i_see_user_with_username_group1_group2_has_a_function_key(step, firstname, lastname, extension):
    common.open_url('user', 'search', {'search': '%s %s' % (firstname, lastname)})
    common.edit_line("%s %s" % (firstname, lastname))
    common.go_to_tab('Func Keys')
    destination_field = world.browser.find_element_by_id('phonefunckey[typevalidentity][]')
    assert destination_field.get_attribute('value') == extension
    type_field = Select(world.browser.find_element_by_id('phonefunckey[type][]'))
    assert type_field.first_selected_option.text == "Customized"
    common.open_url('user', 'search', {'search': ''})


@step(u'Then there is no data about this user remaining in the database.$')
def then_there_is_no_data_about_this_user_remaining_in_the_database(step):
    assert user_helper.count_linefeatures(world.user_id) == 0, "Data is remaining in linefeatures after user deletion."
    assert user_helper.count_rightcallmember(world.user_id) == 0, "Data is remaining in rightcallmember after user deletion."
    assert user_helper.count_dialaction(world.user_id) == 0, "Data is remaining in dialaction after user deletion."
    assert user_helper.count_phonefunckey(world.user_id) == 0, "Data is remaining in phonefunckey after user deletion."
    assert user_helper.count_callfiltermember(world.user_id) == 0, "Data is remaining in callfiltermember after user deletion."
    assert user_helper.count_queuemember(world.user_id) == 0, "Data is remaining in queuemember after user deletion."
    assert user_helper.count_schedulepath(world.user_id) == 0, "Data is remaining in schedulepath after user deletion."


@step(u'When I modify the channel type of group "([^"]*)" of user "([^"]*)" to "([^"]*)"')
def when_i_modify_the_channel_type_of_group_group1_of_user_group2_to_group3(step, group, fullname, chantype):
    common.open_url('user', 'search', {'search': fullname})
    common.edit_line(fullname)
    user_action_webi.select_chantype_of_group(group, chantype)
    form.submit.submit_form()


@step(u'Then the channel type of group "([^"]*)" of user "([^"]*)" is "([^"]*)"')
def then_the_channel_type_of_group_group1_of_user_group2_is_group3(step, group, fullname, chantype):
    common.open_url('user', 'search', {'search': fullname})
    common.edit_line(fullname)
    assert_that(user_action_webi.get_chantype_of_group(group), equal_to(chantype))


@step(u'Then "([^"]*)" has an unconditional forward set to "([^"]*)"')
def then_user_has_an_unconditional_forward_set_to_group2(step, fullname, expected_destination):
    enabled, destination = user_helper.get_unconditional_forward(fullname)
    assert_that(enabled)
    assert_that(destination, equal_to(expected_destination))


@step(u'Then "([^"]*)" has no unconditional forward')
def then_user_has_no_unconditional_forward(step, fullname):
    enabled, _ = user_helper.get_unconditional_forward(fullname)
    assert_that(enabled, is_(False))


def _get_user_info(hashes):
    userinfo = hashes[0]

    if 'id' in userinfo:
        userinfo['id'] = int(userinfo['id'])

    return userinfo
