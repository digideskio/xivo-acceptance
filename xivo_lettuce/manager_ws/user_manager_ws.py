# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
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

from lettuce import world
from xivo_ws import User, UserLine, UserVoicemail
from xivo_lettuce.exception import NoSuchProfileException
from xivo_lettuce.manager_ws import group_manager_ws
from xivo_lettuce.manager_ws import device_manager_ws
from xivo_lettuce.manager_dao import user_manager_dao, voicemail_manager_dao


def add_user(data_dict):
    user = User()
    user.firstname = data_dict['firstname']

    if 'lastname' in data_dict:
        user.lastname = data_dict['lastname']
    if 'agentid' in data_dict:
        user.agent_id = int(data_dict['agentid'])
    if 'language' in data_dict:
        user.language = data_dict['language']
    if 'enable_client' in data_dict:
        user.enable_client = bool(data_dict['enable_client'])
    if 'client_username' in data_dict:
        user.client_username = data_dict['client_username']
    if 'client_password' in data_dict:
        user.client_password = data_dict['client_password']
    if 'client_profile' in data_dict:
        user.client_profile = data_dict['client_profile']
    if 'bsfilter' in data_dict:
        user.bsfilter = data_dict['bsfilter']

    if 'line_number' in data_dict and 'line_context' in data_dict:
        user.line = UserLine()
        user.line.number = data_dict['line_number']
        user.line.context = data_dict['line_context']
        if 'protocol' in data_dict:
            user.line.protocol = data_dict['protocol']
        if 'device' in data_dict:
            device_id = str(device_manager_ws.find_device_id_with_mac(data_dict['device']))
            user.line.device_id = device_id

    if 'voicemail_name' in data_dict and 'voicemail_number' in data_dict:
        user.voicemail = UserVoicemail()
        user.voicemail.name = data_dict['voicemail_name']
        user.voicemail.number = data_dict['voicemail_number']

    if 'mobile_number' in data_dict:
        user.mobile_number = data_dict['mobile_number']

    ret = world.ws.users.add(user)
    if not ret:
        return False

    return int(ret)


def add_or_replace_user(data_dict):
    firstname = data_dict['firstname']
    lastname = data_dict.get('lastname', '')

    user_manager_dao.delete_user_line_extension_with_firstname_lastname(firstname, lastname)
    user_manager_dao.delete_all_user_with_firstname_lastname(firstname, lastname)

    if 'line_number' in data_dict:
        number = data_dict['line_number']
        context = data_dict.get('line_context', 'default')
        user_manager_dao.delete_user_line_extension_with_exten_context(number, context)

    if 'voicemail_name' in data_dict and 'voicemail_number' in data_dict and 'line_context' in data_dict:
        voicemail_manager_dao.delete_voicemail_with_number_context(data_dict['voicemail_number'], data_dict['line_context'])

    return add_user(data_dict)


def delete_users_with_profile(profile_name):
    users = world.ws.users.list()
    profiles = [profile for profile in world.ws.cti_profiles.list() if profile.name == profile_name]

    if not profiles:
        raise NoSuchProfileException('The CTI profile %s does not exist.' % profile_name)

    profile_id = profiles[0].id
    for user in users:
        if user.client_profile_id == profile_id:
            if user.voicemail:
                voicemail_manager_dao.delete_voicemail_with_user_id(user.id)
            user_manager_dao.delete_user_line_extension_with_user_id(user.id)


def user_id_is_in_group_name(group_name, user_id):
    group = group_manager_ws.get_group_with_name(group_name)
    for id in group.user_ids:
        if id == user_id:
            return True
    return False


def disable_cti_client(firstname, lastname):
    users = _search_users_with_firstname_lastname(firstname, lastname)
    for user in users:
        user.enable_client = False
        world.ws.users.edit(user)


def enable_cti_client(firstname, lastname):
    users = _search_users_with_firstname_lastname(firstname, lastname)
    for user in users:
        user.enable_client = True
        world.ws.users.edit(user)


def _search_users_with_firstname_lastname(firstname, lastname):
    users = world.ws.users.search('%s %s' % (firstname, lastname))
    return [user for user in users if
            user.firstname == firstname and
            user.lastname == lastname]
