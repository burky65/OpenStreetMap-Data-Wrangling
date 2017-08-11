# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 20:32:32 2017

@author: Burky
"""
import xml.etree.cElementTree as ET
import pprint
from collections import defaultdict
import re

filename = 'cleveland_ohio.osm'

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_types = defaultdict(set)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Circle", 
            "Cove", "Cut", "Downs", "East", "Esplanade", "Lane", "Lorain", 
            "Middleton", "North", "Northeast", "Northwest", "Parkway", "Path", 
            "Plaza", "Ridge", "Road", "Shoreway", "South", "Southeast", 
            "Square", "Terrace", "Trail", "Way", "Weigh", "West", "Arlington",
            "Pike", "Southwest"]
# Expected list is the list of appropriately spelled street names
# List was adjusted based on data in the file to make identification of
# errors easier

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
            
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def audit():
    for event, elem in ET.iterparse(filename, events=("start",)):
        if elem.tag == 'way' or elem.tag == 'node':
            for tag in elem.iter('tag'):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    pprint.pprint(street_types)
    
audit()