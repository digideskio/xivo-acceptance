from lettuce.registry import world

from selenium.common.exceptions import NoSuchElementException

USER_URL = '/service/ipbx/index.php/pbx_settings/users/%s'


def open_add_user_form():
    URL = USER_URL % '?act=add'
    world.browser.get('%s%s' % (world.url, URL))
    world.browser.find_element_by_id('it-userfeatures-firstname', 'User add form not loaded')

def open_edit_user_form(id):
    URL = USER_URL % '?act=edit&id=%d'
    world.browser.get('%s%s' % (world.url, URL % id))
    world.browser.find_element_by_id('it-userfeatures-firstname', 'User edit form not loaded')

def open_list_user_url():
    URL = USER_URL % '?act=list'
    world.browser.get('%s%s' % (world.url, URL))
    world.browser.find_element_by_id('table-main-listing', 'User list not loaded')

def type_user_names(firstName, lastName):
    world.browser.find_element_by_id('it-userfeatures-firstname', 'User form not loaded')
    input_firtName = world.browser.find_element_by_id('it-userfeatures-firstname')
    input_lastName = world.browser.find_element_by_id('it-userfeatures-lastname')
    input_firtName.clear()
    input_firtName.send_keys(firstName)
    input_lastName.clear()
    input_lastName.send_keys(lastName)

def type_user_in_group(groupName):
    group = world.browser.find_element_by_xpath("//li[@id='dwsm-tab-7']//a[@href='#groups']")
    group.click()
    world.browser.find_element_by_id('sb-part-groups', 'Group tab not loaded')
    select_group = world.browser.find_element_by_xpath('//select[@id="it-grouplist"]//option[@value="%s"]' % groupName)
    select_group.click()
    add_button = world.browser.find_element_by_id('bt-ingroup')
    add_button.click()

def delete_all_users():
    from webservices.user import WsUser
    wsu = WsUser()
    wsu.clear()

def user_is_saved(firstname, lastname):
    open_list_user_url()
    try:
        user = world.browser.find_element_by_xpath("//table[@id='table-main-listing']//tr[contains(.,'%s %s')]" % (firstname, lastname))
        return user is not None
    except NoSuchElementException:
        return False

def insert_user(firstname, lastname):
    from webservices.user import WsUser
    import json
    with open('xivojson/userwithline.json') as f:
        datajson = f.read()  % {'firstname': firstname,
                'lastname': lastname}
        data = json.loads(datajson)
    wsu = WsUser()
    wsu.add(data)

def delete_user(firstname, lastname):
    from webservices.user import WsUser
    wsu = WsUser()
    for id in find_user_id(firstname, lastname):
        wsu.delete(id)

def find_user_id(firstname, lastname):
    from webservices import user
    wsu = user.WsUser()
    user_list = wsu.list()
    return [userinfo['id'] for userinfo in user_list
        if userinfo['firstname'] == firstname and userinfo['lastname'] == lastname]

def is_in_group(group_name, user_id):
    from webservices import group
    wsg = group.WsGroup()
    group_list = wsg.list()
    group_id = [group['id'] for group in group_list if group['name'] == group_name]
    if len(group_id) > 0:
        group_view = wsg.view(group_id[0])
        for user in group_view['user']:
            if user['userid'] == user_id:
                return True
    return False

def insert_group_with_user(group_name, user_list=[]):
    from webservices import group
    import json
    with open('xivojson/group.json') as f:
        data = f.read()
        users = ""
        if len(user_list) > 0:
            users = r', "user": [%s]' % ', '.join(['"%s"' % str(id) for id in user_list])
        data = data % {'user_list': users,
                'groupname': group_name}
        data = json.loads(data)
    wsg = group.WsGroup()
    wsg.clear()
    wsg.add(data)