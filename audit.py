#! /usr/bin/env python

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import cleaning


osm_filename = "san-diego_california.osm"

lower_colon = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
expected_street = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", "Trail", "Parkway", "Commons"]

def audit_steet_type(street_types, street_name):
    """Audits the street types. Add the type to a dictionary if it doesn't exist in our list of expected street types"""

    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected_street:
            street_types[street_type].add(street_name)

def audit_street(osm_filename):
    """Finds all different types of streets in the dataset"""

    osm_file = open(osm_filename, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=  ("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if cleaning.is_street_name(tag):
                    audit_steet_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types

def show_improved_st_names(st_types):
    """Prints the improved street names if an improvement has been performed"""

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = cleaning.update_street_name(name, cleaning.mapping)
            if name != better_name:
                print name, "=>", better_name

def audit_phone(osm_filename):
    """Obtains the phone numbers and saves them into a list"""

    osm_file = open(osm_filename, "r")
    phone_types = []
    for event, elem in ET.iterparse(osm_file, events=  ("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if cleaning.is_phone(tag):
                    phone_types.append(tag.attrib['v'])
    osm_file.close()
    return phone_types

def show_improved_phones(phone_types):
    """Shows the improved phone numbers if an improvement has been performed"""

    for phone in phone_types:
        better_phone = cleaning.update_phone(phone)
        if phone != better_phone:
            print phone, "=>", better_phone

if __name__ == '__main__':
    st_types = audit_street(osm_filename)
    show_improved_st_names(st_types)
    phone_types = audit_phone(osm_filename)
    show_improved_phones(phone_types)


