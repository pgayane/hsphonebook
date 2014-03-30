#! /usr/bin/env python

import sys
import json
import os.path
from config import pb_path
import inspect

success_msg = "Great! %s operation is successful"

func_dict = {}

def cmd(func):
    def error_checked_cmd(*args):
        params = inspect.getargspec(func).args
        error = invalid_params(params, args, func.__name__)
        if error:
            return error
        return func(*args)
    func_dict[func.__name__.replace('_', '-')] = error_checked_cmd
    return error_checked_cmd

def get_msg(successful, params):
    return success_msg % (params)

def invalid_params(params, args, func_name):
    if len(params) != len(args):
        print params
        print args
        return 'Error: %s operation requires at least %d argument' % (func_name, len(params))
    if 'phonebook' in params:
        phonebook = args[params.index('phonebook')]
        if not os.path.isfile(phonebook):
            return 'Error: phone book does not exist %s' %phonebook
    return None

@cmd
def set_default(default_phonebook):
    with open('config.py', 'w+') as config:
        config.write('pb_path = "%s"' % default_phonebook)

@cmd
def create(phonebook_name):
    global success_msg

    with open(phonebook_name, 'w+') as phonebook:
        phonebook.write('[]')

    return get_msg(success_msg, "create")

@cmd
def lookup(search_name, phonebook):
    pb = json.load(open(phonebook, 'r'))
    contact_list = search(pb, 'name', search_name)
    if contact_list == '':
        return 'Error: phone record with for %s cannot be found' % search_name
    else:
        return contact_list

def get_contact(pb, name):
    for c in pb:
        if c['name'].lower() == name.lower():
            return c
    return None

def search(pb, field, value):
    contact_list = ''
    for contact in pb:
        if value.lower() in contact[field].lower():
            contact_list += '%s %s\n' %(contact["name"], contact["phone"])

    return contact_list

@cmd
def add(params, phonebook):
    error = invalid_params(params, 'add' , 2, phonebook)
    if error:
        return error

    contact = {"name": params[0],
             "phone": params[1]}

    pb = json.load(open(phonebook, 'r'))

    if get_contact(pb, contact['name']) is not None:
        return "Error: Contact already existed! Nothing added."

    pb.append(contact)

    json.dump(pb, open(phonebook, 'w'))

    return get_msg(success_msg, "add")

@cmd
def change(name, phone, phonebook):
    pb = json.load(open(phonebook, 'r'))

    contact = get_contact(pb, name)
    if contact is None:
        return 'Error: contact cannot be found'

    contact['phone'] = phone
    json.dump(pb, open(phonebook, 'w'))

    return get_msg(success_msg, "change")

@cmd
def remove(name, phonebook):
    pb = json.load(open(phonebook, 'r'))
    contact = get_contact(pb, name)
    if contact is None:
        return 'Error: contact cannot be found'

    pb.remove(contact)
    json.dump(pb, open(phonebook, 'w'))

    return get_msg(success_msg, "remove")

@cmd
def reverse_lookup(phone, phonebook):
    pb = json.load(open(phonebook, 'r'))
    contact_list = search(pb, 'phone', phone)
    if contact_list is '':
        return 'Error: No contact record are found'
    return contact_list

def main():
    global func_dict
    if len(sys.argv) <=1:
        print 'please provide operation (%s)' % ', '.join(func_dict.keys())
    else:
        operation = sys.argv[1]
        phonebook = pb_path # deafult

        args = sys.argv[2:]
        if '-b' in args:
            i = args.index('-b')
            phonebook = args.pop(i)
        command = func_dict[operation]
        if 'phonebook' in inspect.getargspec(command).args:
            print command(*args, phonebook=phonebook)
        else:
            print command(*args)

if __name__ == '__main__':
    main()
