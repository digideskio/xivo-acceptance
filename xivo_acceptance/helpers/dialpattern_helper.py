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

from xivo_lettuce.remote_py_cmd import remote_exec
from execnet.gateway_base import RemoteError


def delete(dialpattern_id):
    try:
        remote_exec(_delete, dialpattern_id=dialpattern_id)
    except RemoteError:
        pass


def _delete(channel, dialpattern_id):
    from xivo_dao import dialpattern_dao

    dialpattern_dao.delete(dialpattern_id)
