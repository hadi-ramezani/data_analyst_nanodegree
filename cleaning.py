#! /usr/bin/env python

import re

# The mapping was completed according to auditing the data
mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Rd.": "Road",
            "Av": "Avenue",
            "Ave.": "Avenue",
            "Bl": "Boulevard",
            "Blvd": "Boulevard",
            "Blvd.": "Boulevard",
            "Ct": "Court",
            "Dr": "Drive",
            "Dr.": "Drive",
            "Pkwy": "Parkway",
            "Pl": "Place",
            "Wy": "Way"
            }

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

def is_street_name(elem):
    """ Checks if the tag's attribute value is street. Return True if it is and False otherwise"""

    return (elem.attrib['k'] == "addr:street")

def update_street_name(name, mapping):
    """Updates the street name by mapping the name with appropriate value in the dictionary mapping"""

    m = street_type_re.search(name)
    if m.group() in mapping.keys():
        name = re.sub(m.group(), mapping[m.group()], name)
    return name

def is_phone(elem):
    """ Checks if the tag's attribute value is phone. Return True if it is and False otherwise"""

    if elem.attrib['k'] == "phone":
        return True
    elif (len(elem.attrib['k'].split(':', 1)) > 1 and elem.attrib['k'].split(':', 1)[1] == "phone"):
        return True
    else:
        return False


def update_phone(phone_num):
    """Updates the phone numbers. Keeps the digits and drops the country code if it exists.
    Returns the original values if there are less than 10 digits in the phone value. This is possible if characters
    are used to represent phone numbers, quite rare these days"""

    only_digit_num = filter(str.isdigit, phone_num)
    if len(only_digit_num) > 10 and only_digit_num.startswith('1'):
        return only_digit_num[1:]
    elif len(only_digit_num) == 10:
        return only_digit_num
    else:
        return phone_num

