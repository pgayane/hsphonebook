import sys
import json
import os.path


def invalid_params(params, func_name, count, phonebook = 'hsphonebook.hb'):
    if len(params) <= count-1:
        return 'Error: %s operation requires at least %d argument' %(func_name, count)

    if not os.path.isfile(phonebook):
        return 'Error: phone book does not exist'
    
    return None

def create(params, phonebook):
    with open(params[0], 'w+') as phonebook:
        phonebook.write('[]')
    
    return 'phonebook created'

def lookup(params, phonebook):
    error = invalid_params(params, 'lookup' , 1)
    if error:
        return error

    search_name = params[0]
    pb = json.load(open(phonebook, 'r'))
    contact_list = search(pb, 'name', search_name)
    if contact_list == '':
        return 'phone record with for %s cannot be found' % search_name
    else:
        return contact_list

def get_contact(pb, name):
    for c in pb:
        if c['name'] == name:
            return c
    return None

def search(pb, field, value):
    contact_list = ''
    for contact in pb:
        if value in contact[field]:
            contact_list += '%s %s\n' %(contact["name"], contact["phone"])
    
    return contact_list

def add(params, phonebook):
    error = invalid_params(params, 'add' , 2)
    if error:
        return error

    contact = {"name": params[0],
             "phone": params[1]}
    
    pb = json.load(open(phonebook, 'r'))

    if get_contact(pb, contact['name']) is not None:
        return "Contact already existed! Nothing added."

    pb.append(contact)

    json.dump(pb, open(phonebook, 'w'))

    return 'contact information added to a phone book'

def change(params, phonebook):
    error = invalid_params(params, 'chane' , 2)
    if error:
        return error

    name = params[0]
    phone = params[1]

    pb = json.load(open(phonebook, 'r'))

    contact = get_contact(pb, name)
    if contact is None:
        return 'Error: contact cannot be found'
    
    contact['phone'] = phone 
    json.dump(pb, open(phonebook, 'w'))

    return "Great! change was successful"

def remove(params, phonebook):
    error = invalid_params(params, 'remove' , 1)
    if error:
        return error
    
    name = params[0]

    pb = json.load(open(phonebook, 'r'))
    contact = get_contact(pb, name)
    if contact is None:
        return 'Error: contact cannot be found'

    pb.remove(contact)
    json.dump(pb, open(phonebook, 'w'))

    return "Great! contact deleted"

def reverse_lookup(params, phonebook):
    error = invalid_params(params, 'reverse lookup' , 1)
    if error:
        return error

    phone = params[0]

    pb = json.load(open(phonebook, 'r'))
    contact_list = search(pb, 'phone', phone)
    if contact_list is '':
        return 'No contact record are found'

    return contact_list


func_dict = {'create': create,
            'lookup': lookup,
            'add': add,
            'change': change,
            'remove': remove,
            'reverse-lookup': reverse_lookup}

def main():
    global func_dict
    if len(sys.argv) <= 1:
        print 'please provide operation'
    else:
        operation = sys.argv[1]
        params = []
        phonebook = '' # deafult

        for i in range(2, len(sys.argv)):
            if sys.argv[i] == '-b':
                phonebook = sys.argv[i+1]
                break # should be the last argument
            else:
                params.append(sys.argv[i])

    print func_dict[operation](params, phonebook)

if __name__ == '__main__':
    main()
