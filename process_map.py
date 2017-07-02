#! /usr/bin/env python

import xml.etree.cElementTree as ET
from collections import defaultdict
import cleaning
import re
import pprint
import csv
import codecs
import cerberus
import schema

osm_file = "sample.osm"
nodes_csv = "nodes.csv"
node_tag_csv = "nodes_tags.csv"
ways_csv = "ways.csv"
way_nodes_csv = "ways_nodes.csv"
way_tags_csv = "ways_tags.csv"


lower_colon = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

node_fields = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
node_tags_fields = ['id', 'key', 'value', 'type']
way_fields = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
way_tags_fields = ['id', 'key', 'value', 'type']
way_nodes_fields = ['id', 'node_id', 'position']

def shape_element(element, node_attr_fields=node_fields, way_attr_fields=way_fields,
                  problem_chars=problemchars, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    if element.tag == 'node':
        node_attribs['id'] = element.attrib['id']
        node_attribs['user'] = element.attrib['user']
        node_attribs['uid'] = element.attrib['uid']
        node_attribs['version'] = element.attrib['version']
        node_attribs['lat'] = element.attrib['lat']
        node_attribs['lon'] = element.attrib['lon']
        node_attribs['timestamp'] = element.attrib['timestamp']
        node_attribs['changeset'] = element.attrib['changeset']
        for tag in element.iter("tag"):
            if not problemchars.search(tag.attrib['k']):
                sec_tag = {}
                sec_tag['id'] = element.attrib['id']
                if cleaning.is_phone(tag):
                    sec_tag['value'] = cleaning.update_phone(tag.attrib['v'])
                elif cleaning.is_street_name(tag):
                    sec_tag['value'] = cleaning.update_street_name(tag.attrib['v'], cleaning.mapping)
                else:
                    sec_tag['value'] = tag.attrib['v']
                if lower_colon.search(tag.attrib['k']):
                    sec_tag['type'] = tag.attrib['k'].split(':', 1)[0]
                    sec_tag['key'] = tag.attrib['k'].split(':', 1)[1]
                else:
                    sec_tag['key'] = tag.attrib['k']
                    sec_tag['type'] = default_tag_type
                tags.append(sec_tag)
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        way_attribs['id'] = element.attrib['id']
        way_attribs['user'] = element.attrib['user']
        way_attribs['uid'] = element.attrib['uid']
        way_attribs['version'] = element.attrib['version']
        way_attribs['timestamp'] = element.attrib['timestamp']
        way_attribs['changeset'] = element.attrib['changeset']
        for tag in element.iter("tag"):
            if not problemchars.search(tag.attrib['k']):
                sec_tag = {}
                sec_tag['id'] = element.attrib['id']
                sec_tag['value'] = tag.attrib['v']
                if lower_colon.search(tag.attrib['k']):
                    sec_tag['type'] = tag.attrib['k'].split(':', 1)[0]
                    sec_tag['key'] = tag.attrib['k'].split(':', 1)[1]
                else:
                    sec_tag['key'] = tag.attrib['k']
                    sec_tag['type'] = default_tag_type
                tags.append(sec_tag)
        for i, tag in enumerate(element.iter("nd")):
            sec_tag = {}
            sec_tag['id'] = element.attrib['id']
            sec_tag['node_id'] = tag.attrib['ref']
            sec_tag['position'] = i
            way_nodes.append(sec_tag)
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}

# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)

        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(nodes_csv, 'w') as nodes_file, \
         codecs.open(node_tag_csv, 'w') as nodes_tags_file, \
         codecs.open(ways_csv, 'w') as ways_file, \
         codecs.open(way_nodes_csv, 'w') as way_nodes_file, \
         codecs.open(way_tags_csv, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, node_fields)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, node_tags_fields)
        ways_writer = UnicodeDictWriter(ways_file, way_fields)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, way_nodes_fields)
        way_tags_writer = UnicodeDictWriter(way_tags_file, way_tags_fields)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])

if __name__ == '__main__':
    process_map(osm_file, validate=False)



