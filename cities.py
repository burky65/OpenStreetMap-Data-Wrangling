# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 06:00:59 2017

@author: Burky
"""

#Dictionary mapping incorrect city spellings in the OSM file with
#their correct spellings to make the csv files more uniform.

cities = { "Arkan": "Akron",
           "Avon Ohio": "Avon",
           "Chardom": "Chardon",
           "Clevalnd": "Cleveland",
           "Cleveland OH": "Cleveland",
           "Clevland": "Cleveland",
           "Hinckley, Medina County": "Hinckley",
           "Mayfield Hts": "Mayfield Heights",
           "Mentor, Ohio": "Mentor",
           "Stromgsville": "Strongsville",
           "cleveland": "Cleveland",
           "garrettsville": "Garrettsville",
           "madison": "Madison",
           "painesville": "Painesville",
           "valley View": "Valley View",
           "Middleburgs Hts.": "Middleburg Heights",
           "kent": "Kent",
           "Champion, Ohio": "Champion",
           "Cleveland, OH": "Cleveland",
           "Perry, OH": "Perry",
           "Wooster, OH": "Wooster",
           "hudson": "Hudson",
           "oberlin": "Oberlin",
           "rocky river": "Rocky River",
           "solon": "Solon",
           "warrensville heights": "Warrensville Heights"}