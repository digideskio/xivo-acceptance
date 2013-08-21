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

from xivo_dao import voicemail_dao, user_dao
from xivo_dao.alchemy.voicemail import Voicemail
from xivo_restapi.v1_0.restapi_config import RestAPIConfig
import random
from xivo_lettuce.restapi.v1_1 import ws_utils_session


class RestVoicemail(object):

    def __init__(self):
        self.ws_utils = ws_utils_session

    def create_voicemail(self, fullname=None, number=None, context="default"):
        voicemail = Voicemail()
        voicemail.fullname = fullname
        voicemail.mailbox = number
        voicemail.context = context
        voicemail_dao.add(voicemail)
        return voicemail.uniqueid

    def list(self):
        return self.ws_utils.rest_get(RestAPIConfig.XIVO_VOICEMAIL_SERVICE_PATH + "/")

    def update_voicemail(self, number, newnumber=None, newfullname=None, newdeleteaftersend=False):
        voicemail_id = voicemail_dao.id_from_mailbox(number, "default")
        data = {"mailbox": newnumber,
                "fullname": newfullname,
                "deleteaftersend": newdeleteaftersend}
        return self.update_voicemail_by_id(voicemail_id, data)

    def update_voicemail_by_id(self, voicemailid, data):
        return self.ws_utils.rest_put("%s/%d" % (RestAPIConfig.XIVO_VOICEMAIL_SERVICE_PATH, voicemailid),
                                      data)

    def update_voicemail_field(self, number, fieldname, fieldvalue):
        voicemail_id = voicemail_dao.id_from_mailbox(number, "default")
        data = {fieldname: fieldvalue}
        return self.update_voicemail_by_id(voicemail_id, data)

    def generate_non_existing_id(self):
        generated_id = random.randint(100, 9999)
        while(voicemail_dao.get(generated_id) is not None):
            generated_id = random.randint(100, 9999)
        return generated_id

    def delete_voicemail_from_db(self, voicemailid):
        users = user_dao.get_by_voicemailid(voicemailid)
        for user in users:
            user_dao.update(user.id, {'voicemailid': None})
        voicemail_dao.delete(voicemailid)
