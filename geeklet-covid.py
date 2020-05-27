#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
check COVID-19 numbers
see https://github.com/novelcovid/api for endpoints
"""

import requests
import json
import pprint
from bs4 import BeautifulSoup

__author__ = "Buckley Collum"
__copyright__ = "Copyright 2020, QuoinWorks"
__credits__ = ["Buckley Collum"]
__license__ = "GNU General Public License v3.0"
__version__ = "0.1.0"
__maintainer__ = "Buckley Collum"
__email__ = "buckleycollum@gmail.com"
__status__ = "Dev"


def main():
	"""main"""
	from sty import fg, ef, rs

	url = "https://corona.lmao.ninja/countries/USA"

	params = dict(
		origin='Chicago,IL',
		destination='Los+Angeles,CA',
		waypoints='Joplin,MO|Oklahoma+City,OK',
		sensor='false'
	)

	response = requests.get(url=url)
	# soup = BeautifulSoup(response.text, "html.parser")

	data = response.json()  # Check the JSON Response Content documentation below
	for key, value in data.items():
		if key != "countryInfo":
			print("%s: %s" % (key, value))
	# print(json.dumps(data, indent=4, sort_keys=True))

	url = "https://corona.lmao.ninja/states"
	response = requests.get(url=url)
	data = response.json()  # Check the JSON Response Content documentation below
	print(data)
	if data['state'] == "California":
		print(json.dumps(dda, indent=4, sort_keys=True))


if __name__ == "__main__":
	main()

