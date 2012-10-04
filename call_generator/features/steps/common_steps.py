# -*- coding: UTF-8 -*-

import time

from lettuce.decorators import step
from lettuce.registry import world
from datetime import datetime
from utils.func import extract_number_and_context_from_extension
from xivo_lettuce.common import open_url, element_is_in_list
from xivo_lettuce import form
from xivo_lettuce.checkbox import Checkbox


@step(u'Given there is "([^"]*)" activated in extenfeatures page')
def given_there_is_group1_activated_in_extensions_page(step, option_label):
    open_url('extenfeatures')
    option = Checkbox.from_label(option_label)
    option.check()
    form.submit_form()


@step(u'Then I see no recording file of this call in monitoring audio files page')
def then_i_not_see_recording_file_of_this_call_in_monitoring_audio_files_page(step):
    now = int(time.time())
    search = 'user-1100-1101-%d.wav'
    nbtries = 0
    maxtries = 5
    while nbtries < maxtries:
        assert not element_is_in_list('sounds', search % (now - nbtries), {'dir': 'monitor'})
        nbtries += 1


@step(u'Then I see rejected call to extension "([^"]+)" in asterisk log')
def then_i_see_rejected_call_in_asterisk_log(step, extension):
    number, context = extract_number_and_context_from_extension(extension)
    d = datetime.now()
    regex_date = d.strftime("%b %d %H:%M:([0-9]{2})")
    line_search = "\[%s\] NOTICE\[716\] chan_sip.c: Call from (.+) to extension '%s' rejected because extension not found in context '%s'." % (regex_date, number, context)
    command = ['less', '/var/log/asterisk/messages', '|', 'grep', '-E', '"%s"' % line_search]
    result = world.ssh_client_xivo.out_call(command)
    if not result:
        assert(False)


@step(u'Then i see the called extension "([^"]*)" in call logs page')
def then_i_see_the_called_extension_in_call_logs_page(step, exten):
    open_url('cel')
    form.submit_form()

    expected_exten = world.browser.find_element_by_xpath("//div[@id='sb-part-result']/div/table/tbody/tr[2]/td[3]").text
    assert expected_exten == exten
