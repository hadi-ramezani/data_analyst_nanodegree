#! /usr/bin/env python

import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint
import re

osm_file = "san-diego_california.osm"

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def count_tags(filename):
        osm_file = open(filename, "r")
        tags = defaultdict(int)
        for event, elem in ET.iterparse(osm_file):
            tags[elem.tag] += 1
        return tags

def key_type(element, keys):
    if element.tag == "tag":
        k_attrib = element.attrib['k']
        if lower.search(k_attrib):
            keys["lower"] += 1
        elif lower_colon.search(k_attrib):
            keys["lower_colon"] += 1
        elif problemchars.search(k_attrib):
            keys["problemchars"] += 1
        else:
            keys["other"] += 1
    return keys


def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys


if __name__ == '__main__':
    tags = count_tags(osm_file)
    print tags
    keys = process_map(osm_file)
    pprint.pprint(keys)
