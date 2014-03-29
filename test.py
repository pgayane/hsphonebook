from phonebook import *

def test_create():
    filepath = "phonebook_test.pb"
    params = [filepath]
    
    # create empty test phonebook file
    msg = create(params, filepath)
    if msg != get_msg(success_msg, "create"):
        print 'create test failed'
    else:
        print 'create test passed'


def test_add_lookup():
    filepath = "phonebook_test.pb"
    params = ["Anna Hall", "512 342 5745"]
    

    msg = add(params, filepath)
    if msg != get_msg(success_msg, "add"):
        print 'add test failed'
    else:
        print 'add test passed'

    msg = add(params, filepath)
    if msg == get_msg(success_msg, "add"):
        print 'add duplicate test failed'
    else:
        print 'add duplicate test passed'

    params = ["Ani Hall", "512 342 5745"]
    msg = add(params, filepath)
    if msg != get_msg(success_msg, "add"):
        print 'add1 test failed'
    else:
        print 'add1 test passed'

    contact_list = lookup('hall', filepath).split('\n')[:-1]
    if len(contact_list) == 2:
        print 'add-lookup test passed'
    else:
        print 'add-lookup test failed'


def test_change_reverse_lookup():
    filepath = "phonebook_test.pb"
    params = ["bla", "514 443 5555"]

    msg = change(params, filepath)
    if msg == get_msg(success_msg, "change"):
        print 'change not existing test failed'
    else:
        print 'change not existing test passed'

    params = ["anna hall", "514 443 5555"]
    msg = change(params, filepath)
    if msg != get_msg(success_msg, "change"):
        print 'change test failed'
    else:
        print 'change test passed'

    contact_list = reverse_lookup(params[1:], filepath).split('\n')[:-1]
    if len(contact_list) == 1:
        print 'change-lookup test passed'
    else:
        print 'change-lookup test failed'

    contact_list = reverse_lookup(['2312312312'], filepath)
    if 'error' in contact_list.lower():
        print 'change-lookup test passed'
    else:
        print 'change-lookup test failed'


def test_remove_lookup():
    filepath = "phonebook_test.pb"
    params = ["bla"]

    msg = remove(params, filepath)
    if msg == get_msg(success_msg, "remove"):
        print 'remove not existing test failed'
    else:
        print 'remove not existing test passed'

    params = ["anna hall"]
    msg = remove(params, filepath)
    if msg != get_msg(success_msg, "remove"):
        print 'remove test failed'
    else:
        print 'remove test passed'

    contact_list = lookup(params[:1], filepath)
    if 'error' in contact_list.lower():
        print 'remove-lookup test passed'
    else:
        print 'remove-lookup test failed'


def test():
    test_create()
    test_add_lookup()
    test_change_reverse_lookup()
    test_remove_lookup()

test()