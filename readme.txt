File Descriptions:

addr_street_v_tiger_street.py - This file contains code used to compare the number of tiger street tags with the number
			        of addr:street tags for the purpose of auditing the OSM file and getting an idea of what
			        information was included in the file.

cities.py - file containing the final list of misspelled cities linked to correct spellings for use in fixing these errors
	    prior to conversion to CSV

cities_audit.py - Code used to find the City tags in the CSV and build the cities list

mapping.py - file containing the final list of incorrect street types linked to corrected versions for use in fixing errors
	     prior to conversion to CSV

osm_to_csv_clev.py - final conversion of the xml data in the OSM file to the 5 CSV files

schema.py - contains the formatting for each field in the CSV output files so they could be imported to SQL

street_types.py - code used to identify street types in the OSM file.  The expected list was adjusted after running the
		  code to make each subsequent run more concise and made errors easier to identify.

tag_fixes.py - code used to fix individual tag types, imported to main conversion file to fix city name, zip code, and
	       street types before conversion to CSV

zip_codes.py - code used to identify the zip codes present in the OSM file so errors could be identified and corrected