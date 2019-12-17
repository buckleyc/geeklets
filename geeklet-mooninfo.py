#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
mooninfo.py
{License_info}
"""

# Futures
from __future__ import unicode_literals

# Generic/Built-in
import re
import subprocess
import pexpect
import datetime

# Other Libs
from typing import Any, Union

import pylunar

# Owned
# from {path} import {class}

__author__ = "Buckley Collum"
__copyright__ = "Copyright 2019, QuoinWorks"
__credits__ = ["Buckley Collum"]
__license__ = "GNU General Public License v3.0"
__version__ = "1.0.0"
__maintainer__ = "Buckley Collum"
__email__ = "buckleycollum@gmail.com"
__status__ = "Dev"


def dd2dms(decimaldegrees):
    """Convert decimal degrees to degrees-minutes-seconds"""
    is_positive = (decimaldegrees >= 0)
    decimaldegrees = abs(decimaldegrees)
    degrees: Union[int, Any]
    minutes: Union[int, Any]
    seconds: Union[float, Any]
    minutes, seconds = divmod(decimaldegrees * 3600, 60)
    degrees, minutes = divmod(minutes, 60)
    degrees = degrees if is_positive else -degrees
    return degrees, minutes, seconds


def get_lat_lon(mylocation):
    pattern = "\<([+-]?[\d.]+),([+-]?[\d.]+)\>\s+\+\/\-\s([\d.]+m)\s\(.*\)\s\@\s([\d\/]+),\s([\d:]+ [AP]M)\s([\w ]+)"
    for line in iter(str(mylocation).splitlines()):
        match = re.search(pattern, line)
        if match:
            new_line = match.group()  # + '\n'
            latitude = float(match.group(1))
            longitude = float(match.group(2))
            return latitude, longitude
        else:
            return False


def main():
    cmd = '/Users/buckley/bin/LocateMe'
    try:
        locateMeStr = subprocess.run(cmd, encoding='utf-8',
                                     check=True, stdout=subprocess.PIPE).stdout
        returncode = 0
    except subprocess.CalledProcessError as e:
        # output = e.output
        # returncode = e.returncode
        print(f"{cmd} {e.returncode} {e.output}")

    child = pexpect.spawn(cmd)
    # Wait no more than 20 seconds for result.
    try:
        cexpect = child.expect('\<([+-]?[\d.]+),([+-]?[\d.]+)\>.*', timeout=20)
    except pexpect.TIMEOUT:
        print("LocateMe error. Timeout. Skipping")
    except pexpect.EOF:
        print("LocateMe error. EOF. Skipping")

    lat, lon = get_lat_lon(locateMeStr.rstrip('\n'))

    # print(f"{lat},{lon}")

    when = datetime.datetime.now()

    mi = pylunar.MoonInfo(dd2dms(lat), dd2dms(lon))
    mi.update(datetime.date.timetuple(when)[0:6])
    age = mi.age()
    phase = mi.fractional_phase()
    phase_name = mi.phase_name().replace("_", " ").title()

    print(f"The {phase_name} Moon is at {phase:.0%} and is {age:.1f} days old.")


if __name__ == '__main__':
    main()
