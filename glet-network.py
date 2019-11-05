#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
glet-network
{License_info}
"""

# Futures
from __future__ import unicode_literals
from __future__ import print_function

# Generic/Built-in
import os

# Other Libs
from typing import List, Any

import socket
import subprocess
import re
from ipify import get_ip
from sty import fg, bg, ef, rs
import pexpect

# Owned
# from {path} import {class}

__author__ = "Buckley Collum"
__copyright__ = "Copyright 2019, QuoinWorks"
__credits__ = ["Buckley Collum"]
__license__ = "GNU General Public License v3.0"
__version__ = "1.1.0"
__maintainer__ = "Buckley Collum"
__email__ = "buckleycollum@gmail.com"
__status__ = "Dev"

LOCALHOST = socket.gethostname()
logfile: str = '/var/tmp/geektool_LocateMe.txt'
pattern = "\<([+-]?[\d.]+),([+-]?[\d.]+)\>\s+\+\/\-\s([\d.]+m)\s\(.*\)\s\@\s([\d\/]+),\s([\d:]+ [AP]M)\s([\w ]+)"
port = {"lpss-serial1": "LPSS Serial Adapter (1)", "lpss-serial2": "LPSS Serial Adapter (2)", "fw0": "Display Firewire",
        "en0": "Wi-Fi", "en1": "Thunderbolt 1", "en2": "Thunderbolt 1", "en3": "Thunderbolt 13",
        "en4": "Thunderbolt 14",
        "en6": "Bluetooth PAN", "en9": "Display Ethernet", "bridge0": "Thunderbolt Bridge", "lo0": "loopback",
        "ppp0": "VPN",
        "utun0": "Back To My Mac", "utun1": "Back To My Mac"}
port_len = max((len(v)) for k, v in port.items())

location = {"Home": ('Home', 'SoCal', 34.0373, -118.3677, 'America/Los_Angeles', 100),
            "Studio": ('Studio', 'SoCal', 34.0373, -118.3677, 'America/Los_Angeles', 100)
            }
active_ip = {}


def _load_ips_netifaces():
    """load ip addresses with netifaces"""
    import netifaces
    global LOCALHOST
    local_ips = []
    public_ips: List[Any] = []

    # list of iface names, 'lo0', 'eth0', etc.
    for iface in netifaces.interfaces():
        # list of ipv4 addrinfo dicts
        ipv4s = netifaces.ifaddresses(iface).get(netifaces.AF_INET, [])
        for entry in ipv4s:
            addr = entry.get('addr')
            if not addr:
                continue
            if not (iface.startswith('lo') or addr.startswith('127.')):
                public_ips.append(addr)
            elif not LOCALHOST:
                LOCALHOST = addr
            local_ips.append(addr)
    if not LOCALHOST:
        # we never found a loopback interface (can this ever happen?), assume common default
        LOCALHOST = '127.0.0.1'
        local_ips.insert(0, LOCALHOST)
    # local_ips.extend(['0.0.0.0', ''])

    # print(local_ips)
    # print(public_ips)

    return public_ips

    # LOCAL_IPS[:] = _uniq_stable(local_ips)
    # PUBLIC_IPS[:] = _uniq_stable(public_ips)


def pub_ip():
    import socket
    import urllib3
    http = urllib3.PoolManager()
    my_ip = http.request('GET', 'http://ip.42.pl/raw')
    try:
        socket.inet_aton(my_ip.data)
        return my_ip
    except socket.error:
        return False


def touch(fname, times=None):
    """
    Emulates the 'touch' command by creating the file at *fname* if it does not
    exist.  If the file exist its modification time will be updated.
    """
    import os
    import io
    with io.open(fname, 'ab'):
        os.utime(fname, times)


def active():
    import netifaces
    for interface in netifaces.interfaces():
        # print interface
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET not in addresses:
            continue
        if interface == 'lo0':
            continue
        if "utun" in interface:
            continue
        for address in addresses[netifaces.AF_INET]:
            for x in address:
                if x == 'addr':
                    active_ip[interface] = address[x]
                    # print(interface, address[x])
    # print(active_ip)
    # for k,v in active_ip.iteritems(): print(k,v)
    port_len = max((len(port[k])) for k, v in active_ip.items())
    # print(f"port_len is {port_len}")
    primary = netifaces.gateways()['default'][netifaces.AF_INET][1]
    # print(f"primary gateway is {primary}")
    # print(f"active ip is {active_ip[primary]}")
    print(ef.bold + "%*s: %s" % (port_len, port[primary], active_ip[primary]) + rs.bold_dim)
    active_ip.pop(primary, 0)
    for i in active_ip:
        # print("%*s: %s" % (port_len, port[i], active_ip[i]))
        print("%*s: %s" % (port_len, port[i], active_ip[i]))
    return port_len


def online():
    ip_count = len(_load_ips_netifaces())
    if ip_count:
        return True
    else:
        return False


def locationChange():
    ip_count = len(_load_ips_netifaces())
    if ip_count:
        return True
    else:
        return False


def getLatLong(locateMeStr):
    pattern = "\<([+-]?[\d.]+),([+-]?[\d.]+)\>\s+\+\/\-\s([\d.]+m)\s\(.*\)\s\@\s([\d\/]+),\s([\d:]+ [AP]M)\s([\w ]+)"
    for line in iter(str(locateMeStr).splitlines()):
        match = re.search(pattern, line)
        if match:
            new_line = match.group()  # + '\n'
            latitude = float(match.group(1))
            longitude = float(match.group(2))
            return latitude, longitude
        else:
            return False


def getAddress(latitude, longitude):
    import geocoder
    g = geocoder.geocodefarm([latitude, longitude], method='reverse')
    return g.address


def isclose(a, b, rel_tol=0.0005, abs_tol=0.0):
    """
    Comparing for approximately the same location.
    from https://en.wikipedia.org/wiki/Decimal_degrees:
        decimal-degrees	DMS	            qualitative scale that can be identified    at equator  E/W at 23N/S
        0.0001          0° 00′ 0.36″	individual street, land parcel	            11.132 m	10.247 m
    So, the default of 0.0005 is about 50 meters.
    """
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def magichours(lat, lon):
    import astral
    magicHour = {'golden': [], 'blue': []}
    l = astral.Location(('Studio', 'SoCal', lat, lon, 'US/Pacific', 100))
    astral.solar_depression = 'civil'
    for direction in [astral.SUN_RISING, astral.SUN_SETTING]:
        start, end = l.golden_hour(direction)
        magicHour['golden'].append(start)
        magicHour['golden'].append(end)
        start, end = l.blue_hour(direction)
        magicHour['blue'].append(start)
        magicHour['blue'].append(end)
    # print(magicHour)
    print(ef.italic +
          "Dawn : %s %s %s %s" %
          (
              fg.blue + magicHour['blue'][0].strftime("%H:%M:%S") + rs.fg,
              fg.yellow + magicHour['golden'][0].strftime("%H:%M:%S") + rs.fg,
              fg.red + l.sunrise().strftime("%H:%M:%S") + rs.fg,
              fg.yellow + magicHour['golden'][1].strftime("%H:%M:%S") + rs.fg
          )
          + rs.italic
          )
    print("Dusk  : %s %s %s %s" %
          (
              fg.yellow + magicHour['golden'][2].strftime("%H:%M:%S") + rs.fg,
              fg.red + l.sunset().strftime("%H:%M:%S") + rs.fg,
              fg.yellow + magicHour['golden'][3].strftime("%H:%M:%S") + rs.fg,
              fg.blue + magicHour['blue'][3].strftime("%H:%M:%S") + rs.fg
          )
          )


def main():
    """main"""
    if online():
        """
        Check if location has changed using CoreLocation (via LocateMe)
        This will compare the current results versus an existing text file
        """
        print(fg.green + ef.bold + ef.underl + "Online" + rs.fg + rs.underl + rs.bold_dim)
        port_len = active()
        locationChanged = True
        #    myips = _load_ips_netifaces()
        #    for ip in myips:
        #        print(u" Ethernet IP : %s" % (ip))

        LocateMeCmd = '/Users/buckley/bin/LocateMe'
        try:
            locateMeStr = subprocess.run(LocateMeCmd, encoding='utf-8',
                                         check=True, stdout=subprocess.PIPE).stdout
            returncode = 0
        except subprocess.CalledProcessError as e:
            # output = e.output
            # returncode = e.returncode
            print(f"{cmd} {e.returncode} {e.output}")

        # print(f"{locateMeStr}")
        # print p
        # <+34.01765757,-118.48244492> +/- 65.00m (speed -1.00 mps / course -1.00) @ 6/7/17, 10:47:33 AM Pacific Daylight Time

        child = pexpect.spawn(LocateMeCmd)
        # Wait no more than 20 seconds for result.
        try:
            cexpect = child.expect('\<([+-]?[\d.]+),([+-]?[\d.]+)\>.*', timeout=20)
        except pexpect.TIMEOUT:
            print("LocateMe error. Timeout. Skipping")
        except pexpect.EOF:
            print("LocateMe error. EOF. Skipping")

        if os.path.exists(logfile) and os.path.getsize(logfile):
            """If logfile exists, then compare results, else create this needed logfile"""
            locateMeLog = [line.rstrip('\n') for line in open(logfile)]
            # print(locateMeLog)
            lat0, lon0 = getLatLong(locateMeLog[0])
            lat, lon = getLatLong(locateMeStr.rstrip('\n'))
            if isclose(lat0, lat) and isclose(lon0, lon):
                locationChanged = False

            if locationChanged:
                lat, lon = getLatLong(locateMeStr)
                address = getAddress(lat, lon)
                pubip = get_ip()

                # print "New location. Writing new logfile"
                with open(logfile, "w+") as f:
                    f.write(str(locateMeStr))
                    f.write("\n")
                    f.write(address)
                    f.write("\n")
                    f.write(pubip)
                    f.write("\n")
            else:
                address = locateMeLog[1]
                pubip = locateMeLog[2]
        else:
            """If logfile missing, then create needed logfile"""
            lat, lon = getLatLong(locateMeStr)
            # print(f"{lat},{lon}")
            address = getAddress(lat, lon)
            # print(address)
            pubip = get_ip()
            pubip += '\n'
            with open(logfile, "w+") as f:
                f.write(str(locateMeStr))
                f.write("\n")
                f.write(address)
                f.write("\n")
                f.write(pubip)
                f.write("\n")

        print(fg.blue + "%*s: %s" % (port_len, "Public", pubip) + rs.fg)
        if locationChanged:
            # print(fg.red + ef.bold + address + rs.bold_dim + rs.fg)
            print(address)
        else:
            print(ef.italic + address + rs.italic)

        # print(lat, lon)
        magichours(lat, lon)
    else:
        print(fg.red + ef.bold + "Offline" + rs.bold_dim + rs.fg)
        locateMeLog = [line.rstrip('\n') for line in open(logfile)]

        address = locateMeLog[1]
        print("Last seen at: %s" % (address))


if __name__ == '__main__':
    main()
