#! /usr/bin/env python

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint


osm_file = "san-diego_california.osm"

lower_colon = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
expected_street = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", "Trail", "Parkway", "Commons"]

def audit_steet_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected_street:
            street_types[street_type].add(street_name)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def audit_street(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=  ("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_steet_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


if __name__ == '__main__':
    st_types = audit_street(osm_file)
    pprint.pprint(dict(st_types))




