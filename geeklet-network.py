#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
glet-network
{License_info}
"""

import geeklet as g

__author__ = "Buckley Collum"
__copyright__ = "Copyright 2019, QuoinWorks"
__credits__ = ["Buckley Collum"]
__license__ = "GNU General Public License v3.0"
__version__ = "1.2.0"
__maintainer__ = "Buckley Collum"
__email__ = "buckleycollum@gmail.com"
__status__ = "Dev"


def main():
    """main"""
    from sty import fg, ef, rs

    locate_me_str = g.locate_me()
    lat, lon = g.get_lat_lon(locate_me_str)
    where = g.known_location(lat, lon)
    if where == False:
        if g.online():
            address = g.get_address(lat, lon)
        else:
            address = f"{lat},{lon}"
    else:
        address = f"{where}"

    print(f"{address}")
    """main"""
    verbose = False
    if g.online():
        """
		Check if location has changed using CoreLocation (via LocateMe)
		This will compare the current results versus an existing text file
		"""
        print(
            fg.green + ef.bold + ef.underl + "Online" + rs.fg + rs.underl + rs.bold_dim
        )
        port_len = g.active()
        pubip = g.pub_ip()
        locationChanged = False

        g.log_coordinates(locate_me_str)

        if verbose:
            message = (
                f"lat,lon = {lat:.2f},{lon:.2f}\n"
                f"address = {address}\n"
                f"pubip = {pubip}\n"
            )
            print(message)

        print(
            "%*s: %s %s"
            % (port_len, fg.blue + "Public" + rs.fg, g.vpn_enabled(), pubip)
        )
        if locationChanged:
            print(fg.red + ef.bold + address + rs.bold_dim + rs.fg)
            # print(address)
        else:
            print(ef.italic + ef.bold + address + rs.bold_dim + rs.italic)

        # print(lat, lon)

    else:
        print(fg.red + ef.bold + "Offline" + rs.bold_dim + rs.fg)
        locateMeLog = [line.rstrip("\n") for line in open(logfile)]
        address = locateMeLog[1]
        print("Last seen at: %s" % (address))


if __name__ == "__main__":
    main()
