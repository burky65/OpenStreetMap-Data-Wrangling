# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 05:41:32 2017

@author: Burky
"""
import mapping
import cities
import re


# Dictionary of odd street name types from the OSM file partnered with uniform types
mapping = mapping.mapping

# Dictionary that contains misspelled city names from the OSM file parterned with correct spellings
cities = cities.cities


def street_check(elem_tag, element, child, tags):
    """Compare and fix street type tags to uniform set of types"""
    street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
    elem_tag['id'] = element.attrib['id']
    elem_tag['type'] = 'addr'
    elem_tag['key'] = 'street'
    m = street_type_re.search(child.attrib['v'])
    street_type=m.group()
    if street_type in mapping:
        elem_tag['value']=re.sub(street_type_re, mapping[street_type], child.attrib['v'])
    else:
        elem_tag['value']=child.attrib['v']
    tags.append(elem_tag)
    
def city_check(elem_tag, element, child, tags):
    """Compare and fix city names to account for misspellings and extra information"""
    elem_tag['id'] = element.attrib['id']
    elem_tag['type'] = 'addr'
    elem_tag['key'] = 'city'
    if child.attrib['v'] in cities:
        elem_tag['value']=cities[child.attrib['v']]
    else:
        elem_tag['value']=child.attrib['v']
    tags.append(elem_tag)
    
def zip_check(elem_tag, element, child, tags):
    """Compare and fix zip code so all entries are appropriate for US cities"""
    elem_tag['id'] = element.attrib['id']
    elem_tag['type'] = 'addr'
    elem_tag['key'] = 'postcode'
    if child.attrib['v']=='OH' or child.attrib['v']=='Ohio':
        elem_tag['value']= "00"
    else:
        elem_tag['value']=child.attrib['v'][:5]
    tags.append(elem_tag)

def final_check(elem_tag, element, child, tags):
    """Check and format all other tag types for conversion to CSV files"""
    elem_tag['id']=element.attrib['id']
    if ':' in child.attrib['k']:
        split_key=child.attrib['k'].split(':',1)
        elem_tag['type']=split_key[0]
        elem_tag['key']=split_key[1]
    else:
        elem_tag['key']=child.attrib['k']
        elem_tag['type']='regular'
    elem_tag['value'] = child.attrib['v']
    tags.append(elem_tag)
    
