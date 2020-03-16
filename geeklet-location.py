#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
geeklet-location
Determine location then present relevant location information
Currently presents address, any known location
{License_info}
"""

import geeklet as g

__author__ = "Buckley Collum"
__copyright__ = "Copyright 2020, QuoinWorks"
__credits__ = ["Buckley Collum"]
__license__ = "GNU General Public License v3.0"
__version__ = "1.0.0"
__maintainer__ = "Buckley Collum"
__email__ = "buckleycollum@gmail.com"
__status__ = "Dev"


def main():
    """main"""
    verbose = False
    locate_me_str = g.locate_me()
    g.log_coordinates(locate_me_str)
    lat, lon = g.get_lat_lon(locate_me_str)
    where = g.known_location(lat, lon)
    if where == False:
        if online():
            address = g.get_address(lat, lon)
        else:
            address = f"{lat},{lon}"
    else:
        address = f"{where}"

    print(f"{address}")


if __name__ == "__main__":
    main()
