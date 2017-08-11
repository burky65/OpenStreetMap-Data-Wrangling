# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 21:11:16 2017

@author: Burky
"""

import xml.etree.cElementTree as ET

filename = 'cleveland_ohio.osm'

addr_street= 0
tiger_street= 0

for event, elem in ET.iterparse(filename):
    if elem.tag == 'way':
        for tag in elem.findall('tag'):
            if tag.attrib['k']=='addr:postcode':
                addr_street += 1
            elif tag.attrib['k'] == 'tiger:name_type':
                tiger_street += 1
            else:
                pass
            
print "addr:street tags =", addr_street
print "Tiger:name_type tags =", tiger_street