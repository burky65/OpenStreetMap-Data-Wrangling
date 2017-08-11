# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 21:27:29 2017

@author: Burky
"""

import xml.etree.cElementTree as ET
import pprint
from collections import defaultdict


filename = 'cleveland_ohio.osm'
cities = defaultdict(int)

for event, elem in ET.iterparse(filename):
    if elem.tag == 'way':
        for tag in elem.findall('tag'):
            if 'addr:city' in tag.attrib['k']:
                cities[tag.attrib['v']]+=1
pprint.pprint(cities)