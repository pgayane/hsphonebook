#! /usr/bin/env python

import sys
import json
import os.path
from config import pb_path
import inspect
import functools
import re

SUCCESS_MSG = "Great! %s operation is successful"

FUNC_DICT = {}

class Phonebook(object):
    @classmethod
    def create(cls, filename):
        with open(filename, 'w+') as phonebook:
            phonebook.write('[]')
    def __init__(self, filename):
        self.filename = filename
    def __setitem__(self, name, phone):
        contact = {"name": name,
                   "phone": phone}
        with open(self.filename, 'r') as readfile:
            data = json.load(readfile)
            data.append(contact)
            with open(self.filename, 'w') as writefile:
                json.dumps(data, writefile)
    def __getitem__(self, name):
        with open(self.filename, 'r') as readfile:
            pb = json.load(readfile)
            return [(c['name'], c['phone']) for c in pb if name.lower() in c['name'].lower()]
    def __delitem__(self, contact):
        with open(self.filename, 'r') as readfile:
            data = json.load(readfile)
            data.remove(contact)
            with open(self.filename, 'w') as writefile:
                json.dumps(data, writefile)
    def reverse_lookup(self, phone):
        normalize = lambda x: re.sub(r'[^\d]', '', x)
        phone = normalize(phone)
        print 'normalized:', phone
        with json.load(open(self.filename, 'r')) as pb:
            return [(c['name'], c['phone']) for c in pb if phone == normalize(c['phone'])]

def cmd(func):
    @functools.wraps(func)
    def error_checked_cmd(*args):
        params = inspect.getargspec(func).args
        error = invalid_params(params, args, func.__name__)
        if error:
            return error
        if 'phonebook' in params:
            pb_index = params.index('phonebook')
            phonebook = args[pb_index]
            if not os.path.isfile(phonebook):
                return 'Error: phone book does not exist %s' % phonebook
            phonebook = Phonebook(phonebook)
            args = args[:pb_index] + (phonebook,) + args[pb_index+1:]
        result = func(*args)
        if result:
            return result
        return get_msg(func.__name__)
    FUNC_DICT[func.__name__.replace('_', '-')] = error_checked_cmd
    return error_checked_cmd

def get_msg(params):
    return SUCCESS_MSG % (params)

def invalid_params(params, args, func_name):
    if len(params) != len(args):
        print params
        print args
        return 'Error: %s operation requires at least %d argument' % (func_name, len(params))
    return None

@cmd
def set_default(default_phonebook):
    with open('config.py', 'w+') as config:
        config.write('pb_path = "%s"' % default_phonebook)

@cmd
def create(phonebook_name):
    Phonebook.create(phonebook_name)

@cmd
def lookup(search_name, phonebook):
    contact_list = phonebook[search_name]
    if not contact_list:
        return 'Error: phone record with for %s cannot be found' % search_name
    return ''.join(['%s %s\n' for c in contact_list])

@cmd
def add(name, phone, phonebook):
    if phonebook[name]:
        return "Error: Contact already existed! Nothing added."
    phonebook[name] = phone

@cmd
def change(name, phone, phonebook):
    contacts = phonebook[name]
    if not contacts:
        return 'Error: contact cannot be found'
    if len(contacts) > 1:
        return 'Error: multiple contacts match query: ' + ' '.join(c['name'] for c in contacts)
    phonebook[contacts[0]['name']] = phone

@cmd
def remove(name, phonebook):
    contacts = phonebook[name]
    if not contacts:
        return 'Error: contact cannot be found'
    if len(contacts) > 1:
        return 'Error: multiple contacts match query: ' + ' '.join(c['name'] for c in contacts)
    del phonebook[contacts[0]]

@cmd
def reverse_lookup(phone, phonebook):
    contact_list = phonebook.reverse_lookup(phone)
    if not contact_list:
        return 'Error: No contact record are found'
    return contact_list

def main():
    if len(sys.argv) <=1:
        print 'please provide operation (%s)' % ', '.join(FUNC_DICT.keys())
    else:
        operation = sys.argv[1]
        phonebook = pb_path # deafult

        args = sys.argv[2:]
        if '-b' in args:
            i = args.index('-b')
            phonebook = args.pop(i)
        command = FUNC_DICT[operation]
        if 'phonebook' in inspect.getargspec(command).args:
            print command(*args, phonebook=phonebook)
        else:
            print command(*args)

if __name__ == '__main__':
    main()
