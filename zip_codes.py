# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 20:51:11 2017

@author: Burky
"""

import xml.etree.cElementTree as ET
import pprint
from collections import defaultdict

filename = 'cleveland_ohio.osm'

zip_codes=defaultdict(int)
for event, elem in ET.iterparse(filename):
    if elem.tag == 'way':
        for tag in elem.findall('tag'):
            if tag.attrib['k']=='addr:postcode':
                zip_codes[tag.attrib['v']] += 1
pprint.pprint(zip_codes)