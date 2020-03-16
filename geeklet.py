#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
geeklet
imports, set variables, defs
"""

from __future__ import print_function

# Futures
from __future__ import unicode_literals

# Generic/Built-in
import os
import re
import socket
import subprocess

# Other Libs
from typing import List, Any

import pexpect
from sty import fg, ef, rs

# Owned
# from {path} import {class}

__author__ = "Buckley Collum"
__copyright__ = "Copyright 2020, QuoinWorks"
__credits__ = ["Buckley Collum"]
__license__ = "GNU General Public License v3.0"
__version__ = "1.0.0"
__maintainer__ = "Buckley Collum"
__email__ = "buckleycollum@gmail.com"
__status__ = "Dev"

LOCALHOST = socket.gethostname()
logfile: str = "/var/tmp/geektool_LocateMe.txt"
pattern = "\<([+-]?[\d.]+),([+-]?[\d.]+)\>\s+\+\/\-\s([\d.]+m)\s\(.*\)\s\@\s([\d\/]+),\s([\d:]+ [AP]M)\s([\w ]+)"
active_ip = {}

port = {
    "lpss-serial1": "LPSS Serial Adapter (1)",
    "lpss-serial2": "LPSS Serial Adapter (2)",
    "fw0": "Display Firewire",
    "en0": "Wi-Fi",
    "en1": "Thunderbolt 1",
    "en2": "Thunderbolt 1",
    "en3": "Thunderbolt 13",
    "en4": "Thunderbolt 14",
    "en6": "Bluetooth PAN",
    "en7": "iPhone USB",
    "en9": "Display Ethernet",
    "bridge0": "Thunderbolt Bridge",
    "lo0": "loopback",
    "ppp0": "VPN",
    "utun0": "Back To My Mac",
    "utun1": "Back To My Mac",
}
port_len = max((len(v)) for k, v in port.items())

import locations

location = locations.location


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
            addr = entry.get("addr")
            if not addr:
                continue
            if not (iface.startswith("lo") or addr.startswith("127.")):
                public_ips.append(addr)
            elif not LOCALHOST:
                LOCALHOST = addr
            local_ips.append(addr)
    if not LOCALHOST:
        # we never found a loopback interface (can this ever happen?), assume common default
        LOCALHOST = "127.0.0.1"
        local_ips.insert(0, LOCALHOST)
    # local_ips.extend(['0.0.0.0', ''])

    # print(local_ips)
    # print(public_ips)

    return public_ips


# LOCAL_IPS[:] = _uniq_stable(local_ips)
# PUBLIC_IPS[:] = _uniq_stable(public_ips)


def cmd(cmd):
    return (
        subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        .stdout.read()
        .decode()
    )


def active():
    import netifaces

    for interface in netifaces.interfaces():
        # print interface
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET not in addresses:
            continue
        if interface == "lo0":
            continue
        if "utun" in interface:
            continue
        for address in addresses[netifaces.AF_INET]:
            for x in address:
                if x == "addr":
                    active_ip[interface] = address[x]
                    # print(interface, address[x])
    # print(active_ip)
    # for k,v in active_ip.iteritems(): print(k,v)
    port_len = max((len(port[k])) for k, v in active_ip.items())
    # print(f"port_len is {port_len}")
    primary = netifaces.gateways()["default"][netifaces.AF_INET][1]
    # print(f"primary gateway is {primary}")
    # print(f"active ip is {active_ip[primary]}")
    print(
        "%*s: %s"
        % (port_len, ef.bold + port[primary] + rs.bold_dim, active_ip[primary])
    )
    active_ip.pop(primary, 0)
    for i in active_ip:
        # print("%*s: %s" % (port_len, port[i], active_ip[i]))
        print("%*s: %s" % (port_len, port[i], active_ip[i]))
    return port_len


def online():
    ip_count = len(_load_ips_netifaces())
    # print("Checking online...")
    if ip_count:
        return True
    else:
        return False


def touch(fname, times=None):
    """
    Emulates the 'touch' command by creating the file at *fname* if it does not
    exist.  If the file exist its modification time will be updated.
    """
    import os
    import io

    with io.open(fname, "ab"):
        os.utime(fname, times)


def pub_ip3():
    import requests
    import re

    url = "http://checkip.dyndns.org"
    resp = requests.get(url)
    my_ip = re.findall(r"\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}", resp.text)
    return my_ip[0]  # .data.decode("utf-8")


def pub_ip2():
    import urllib3

    url = "http://ip.42.pl/raw"
    http = urllib3.PoolManager()
    my_ip = http.request("GET", url)
    return my_ip.data.decode("utf-8")


def pub_ip(inet6=False):
    from requests import get

    # Check if IPv4 or IPv6
    # Thank you, Randall Degges, https://github.com/rdegges
    if inet6:
        url = "https://api6.ipify.org"
    else:
        url = "https://api.ipify.org"
    ip = get(url).text
    return ip


def location_changed():
    import os
    locationChanged = True

    if os.path.exists(logfile) and os.path.getsize(logfile):
        """If logfile exists, then compare results, else create this needed logfile"""
        locateMeLog = [line.rstrip("\n") for line in open(logfile)]
        lat0, lon0 = get_lat_lon(locateMeLog[0])
        lat, lon = get_lat_lon(locate_me())
        # print(f"moved {distance(lat0,lon0,lat,lon)*1000:.1f} meters")
        if isclose(lat0, lat) and isclose(lon0, lon):
            locationChanged = False
        else:
            locationChanged = True
    else:
        locationChanged = True

    return locationChanged

def get_lat_lon(locateMeStr):
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


def known_location(latitude, longitude):
    for key, value in location.items():
        if distance(latitude, longitude, value[2], value[3]) < 0.2:
            """within 0.2 kilometers"""
            return key
        else:
            return False


def get_address(latitude, longitude):
    import geocoder

    where = known_location(latitude, longitude)
    if where:
        return where
    else:
        import requests

        try:
            g = geocoder.geocodefarm([latitude, longitude], method="reverse")
        except requests.exceptions.RequestException as e:
            return "Unknown"
    if g.address == None:
        return "Bad Request"
    else:
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


def distance(lat1, lon1, lat2, lon2):
    import math

    p = math.pi / 180  # 0.017453292519943295        # PI / 180
    a = (
        0.5
        - math.cos((lat2 - lat1) * p) / 2
        + math.cos(lat1 * p)
        * math.cos(lat2 * p)
        * (1 - math.cos((lon2 - lon1) * p))
        / 2
    )
    radius_equator = 6378.0
    radius_pole = 6357.0
    radius_avg = radius_equator - math.sin((lat2 - lat1) / 2.0) * (
        radius_equator - radius_pole
    )
    # print(f"average radius is {radius_avg:.2f} km")
    return (2.0 * radius_avg) * math.asin(math.sqrt(a))  # 2*R*asin...; R = 6371 km


def closest(data, v):
    return min(data, key=lambda p: distance(v["lat"], v["lon"], p["lat"], p["lon"]))


def locate_me():
    import subprocess
    import shutil

    locate_me_cmd = "LocateMe"
    if shutil.which(locate_me_cmd) is not None:
        try:
            locate_me_str = subprocess.run(
                locate_me_cmd, encoding="utf-8", check=True, stdout=subprocess.PIPE
            ).stdout
        except subprocess.CalledProcessError as e:
            print(f"{locate_me_cmd} {e.returncode} {e.output}")

        try:
            return locate_me_str.rstrip("\n")
        except IOError:
            assert False, "Got some IO error"
        else:
            assert True, "Didn't raise any exception"
    else:
        print("Please install {locate_me_cmd} in your path (e.g., '~/bin/'")
        raise SystemExit()


def update_log(linenumber=0, line_update=""):

    if os.path.exists(logfile) and os.path.getsize(logfile) and linenumber > 0:
        """If logfile exists, then update logfile"""
        import fileinput

        for line in fileinput.input(logfile, inplace=True):
            if linenumber == fileinput.filelineno():
                line = line_update
            print(line, end="")
        fileinput.close()
    else:
        """If logfile missing, then create needed logfile"""
        locate_me_str = locate_me()
        lat, lon = get_lat_lon(locate_me_str)
        # print(f"{lat},{lon}")
        address = get_address(lat, lon)
        pubip = pub_ip()
        # pubip += '\n'
        with open(logfile, "w+") as f:
            f.write(str(locate_me_str))
            f.write("\n")
            f.write(address)
            f.write("\n")
            f.write(pubip)
            f.write("\n")


def log_coordinates(locate_me_str):
    import os

    if os.path.exists(logfile) and os.path.getsize(logfile):
        """If logfile exists, then compare results, else create this needed logfile"""
        if location_changed():
            # address = get_address(lat, lon)
            # print("address is %s" % address)
            update_log(0)
        else:
            locateMeLog = [line.rstrip("\n") for line in open(logfile)]
            # address = locateMeLog[1]
            pubip = pub_ip()
            if pubip != locateMeLog[2]:
                update_log(3, pubip)
    else:
        update_log(0)


def vpn_enabled():
    import netifaces as ni

    # print(f"{ni.interfaces()}")
    for iface in ni.interfaces():
        addrinfo = ni.ifaddresses(iface)
        # print(f"{addrinfo}")
        if "utun" in iface and ni.AF_INET in addrinfo:
            return "🔒"  # ni.ifaddresses(iface)[ni.AF_INET][0]['addr']
    return "🔓"
