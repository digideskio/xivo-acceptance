from lettuce.decorators import step
from lettuce.registry import world

from xivo_lettuce.manager import agent_manager
from xivo_lettuce.common import open_url, submit_form, element_is_in_list, \
    remove_line, element_is_not_in_list

@step(u'Given there is an agent "([^"]*)" with number "([^"]*)"')
def given_there_is_an_agent_1_with_number_2(step, firstname, number):
    agent_manager.delete_agent(number)
    agent_manager.insert_agent(firstname, '', number, '')

@step(u'Givent an agent "([^"]*)" "([^"]*)" "([^"]*)" "([^"]*)" in group default')
def givent_an_agent_in_group_default(step, firstname, lastname, number, password):
    agent_manager.delete_agent(number)
    agent_manager.insert_agent(firstname, lastname, number, password)

@step(u'Given I remove agent "([^"]*)"')
def given_i_remove_agent_group1(step, number):
    agent_manager.delete_agent(number)

@step(u'When I create a agent "([^"]*)" "([^"]*)" "([^"]*)"')
def when_i_create_a_agent(step, firstname, lastname, number):
    open_url('agent', 'addagent', {'group':'1'})
    agent_manager.type_agent_info(firstname, lastname, number)
    submit_form()

@step(u'When agent "([^"]*)" "([^"]*)" is removed')
def when_agent_is_removed(step, firstname, lastname):
    remove_line('%s %s' % (firstname, lastname))

@step(u'When I change the agent "([^"]*)" password to "([^"]*)"')
def when_i_change_the_agent_password_to_group1(step, number, password):
    agent_id = agent_manager.find_agent_id_from_number(number)
    open_url('agent', 'editagent', {'group':'1', 'id': agent_id})
    agent_manager.change_password(password)
    submit_form()

@step(u'Then agent "([^"]*)" is displayed in the list of default agent group')
def then_agent_is_displayed_in_the_list_of_agent_group(step, agent):
    assert element_is_in_list("agent", agent, {'group':'1'}, 'listagent') is True

@step(u'Then agent "([^"]*)" is not displayed in the list of default agent group')
def then_agent_is_not_displayed_in_the_list_of_default_agent_group(step, agent):
    assert element_is_not_in_list("agent", agent, {'group':'1'}, 'listagent') is True

@step(u'Then the agent "([^"]*)" password is "([^"]*)"')
def then_the_agent_password_is(step, number, password):
    current_password = agent_manager.get_password(number)
    assert current_password == password, 'passord was not changed : expected : %s current %s' % (password, current_password)