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

from xivo_lettuce.postgres import exec_sql_request


def create_speeddial_for_user(user):
    func_key_id = _create_func_key('speeddial', 'user')
    _associate_user_func_key(func_key_id, user.id)


def _create_func_key(func_key_type, destination):
    type_id = _find_type_id(func_key_type)
    destination_type_id = _find_destination_type_id(destination)
    query = 'INSERT INTO func_key(type_id, destination_type_id) VALUES (:type_id, :destination_type_id) RETURNING id'

    result = exec_sql_request(query,
                              type_id=type_id,
                              destination_type_id=destination_type_id)

    row = result.fetchone()
    return row[0]


def _associate_user_func_key(func_key_id, user_id):
    destination_type_id = _find_destination_type_id('user')

    query = 'INSERT INTO func_key_dest_user(func_key_id, user_id, destination_type_id) VALUES (:func_key_id, :user_id, :destination_type_id)'
    exec_sql_request(query,
                     func_key_id=func_key_id,
                     user_id=user_id,
                     destination_type_id=destination_type_id)


def _find_type_id(type_name):
    query = 'SELECT id FROM func_key_type WHERE name = :name'
    result = exec_sql_request(query, name=type_name)
    row = result.fetchone()
    return row[0]


def _find_destination_type_id(destination_type):
    query = 'SELECT id FROM func_key_destination_type WHERE name = :name'
    result = exec_sql_request(query, name=destination_type)
    row = result.fetchone()
    return row[0]


def delete_func_keys_for_user(user_id):
    query = 'DELETE FROM func_key_dest_user WHERE user_id = :user_id'
    exec_sql_request(query, user_id=user_id)