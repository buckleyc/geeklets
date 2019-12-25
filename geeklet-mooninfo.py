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
import sys
import subprocess
import datetime
import pexpect

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
            latitude = float(match.group(1))
            longitude = float(match.group(2))
            return latitude, longitude
        else:
            return False


def main():
    cmd = "/Users/buckley/bin/LocateMe"
    try:
        locate_me_str = subprocess.run(cmd, encoding='utf-8',
                                       check=True, stdout=subprocess.PIPE).stdout
    except subprocess.CalledProcessError as e:
        print(f'{cmd} {e.returncode} {e.output}', file=sys.stderr)
        sys.exit(e)

    lat, lon = get_lat_lon(locate_me_str.rstrip('\n'))

    # print(f"{lat},{lon}")

    #
    adjustment: datetime.timedelta = datetime.timedelta(hours=20)
    when: datetime.datetime = datetime.datetime.now() + adjustment
    mi = pylunar.MoonInfo(dd2dms(lat), dd2dms(lon))
    mi.update(datetime.date.timetuple(when)[0:6])

    phase_name = mi.phase_name().replace("_", " ").title()

    print(f'The {phase_name} Moon is at {mi.fractional_phase():.0%} and is {mi.age():.1f} days old.')


if __name__ == '__main__':
    main()
