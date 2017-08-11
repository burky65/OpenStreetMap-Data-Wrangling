# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 21:35:14 2017

@author: Burky
"""


import csv
import codecs
import re
import xml.etree.cElementTree as ET
import pprint

import schema
import cerberus
import cities
import mapping
import tag_fixes

OSM_PATH = "cleveland_ohio.osm"
# This is the local file location for the OSM data file

# CSV files to be created
NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

# Regex to identify tags with problem characters
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# Regex to identify the last component of street tags, for cleaning purposes
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# Identify the appropriate schema for the corresponding output CSV files
SCHEMA = schema.schema

# Create dictionaries to contain the information for each CSV output file
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

# Dictionary that contains misspelled city names from the OSM file parterned with correct spellings
cities = cities.cities

# Dictionary of odd street name types from the OSM file partnered with uniform types
mapping = mapping.mapping

# Pull the appropriate tag fields from the XML file and convert to python dictionaries
def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []

    
    if element.tag == 'node':
        for fields in node_attr_fields:
            node_attribs[fields] = element.attrib[fields]
        for child in element:
            if child.tag == 'tag':
                elem_tag = {}
                if child.attrib['k'] == 'addr:street':
                    tag_fixes.street_check(elem_tag, element, child, tags)
                elif child.attrib['k'] =='addr:city':
                    tag_fixes.city_check(elem_tag, element, child, tags)
                elif child.attrib['k'] == 'addr:postcode':
                    tag_fixes.zip_check(elem_tag, element, child, tags)
                else:
                    if problem_chars.match(child.attrib['k']):
                        pass
                    else:
                        tag_fixes.final_check(elem_tag, element, child, tags)
        return {'node': node_attribs, 'node_tags': tags}
    
    elif element.tag == 'way':
        for fields in way_attr_fields:
            way_attribs[fields] = element.attrib[fields]
        for i,nodes in enumerate(element.findall('nd')):
            way_n={}
            way_n['id']=element.attrib['id']
            way_n['node_id']=nodes.attrib['ref']
            way_n['position']=i
            way_nodes.append(way_n)
        for child in element:
            if child.tag == 'tag':
                elem_tag = {}
                if child.attrib['k'] == 'addr:street':
                    tag_fixes.street_check(elem_tag, element, child, tags)
                elif child.attrib['k'] =='addr:city':
                    tag_fixes.city_check(elem_tag, element, child, tags)
                elif child.attrib['k'] == 'addr:postcode':
                    tag_fixes.zip_check(elem_tag, element, child, tags)
                else:
                    if problem_chars.match(child.attrib['k']):
                        pass
                    else:
                        tag_fixes.final_check(elem_tag, element, child, tags)

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

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

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
    process_map(OSM_PATH, validate=True)
# Validation should be set to True to run this with the validator
# Runtime with validation was around 2.5 hours, and without was about 3 minutes
