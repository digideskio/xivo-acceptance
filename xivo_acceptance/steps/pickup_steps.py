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

from xivo_acceptance.action.webi import pickup as pickup_action_webi
from xivo_acceptance.lettuce import common, form


@step(u'Given there are pickups:$')
def given_there_are_pickup(step):
    for data in step.hashes:
        _delete_pickup(data['name'])
        pickup_action_webi.add_pickup(data)


def _delete_pickup(name):
    common.open_url('pickup')
    _pickup_search(name)
    common.remove_element_if_exist('pickup', name)
    _pickup_search('')


def _pickup_search(term):
    form.input.set_text_field_with_id('it-toolbar-search', term)
    form.submit.submit_form('it-toolbar-subsearch')
