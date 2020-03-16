#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
geeklet-astral
Determine location then present astral information
Currently presents sunrise, sunset, blue hour, golden hour
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

full_moon_names = {
    1: ("Wolf", "Old", "Ice"),
    2: ("Snow",),
    3: ("Worm", "Crow", "Crust", "Sap", "Sugar"),
    4: ("Pink", "Fish", "Hare"),
    5: ("Flower", "Milk"),
    6: ("Strawberry", "Mead", "Rose"),
    7: ("Buck", "Thunder", "Wort", "Hay"),
    8: ("Sturgeon", "Fruit", "Grain"),
    9: ("Corn",),
    10: ("Hunter's", "Sanguine"),
    11: ("Beaver", "Frosty", "Mourning"),
    12: ("Cold",),
}


def phase_string(p):
    import bisect
    import random
    import datetime

    PRECISION = 0.05
    NEW = 0 / 4.0
    FIRST = 1 / 4.0
    FULL = 2 / 4.0
    LAST = 3 / 4.0
    NEXTNEW = 4 / 4.0
    phase_strings = (
        (NEW + PRECISION, "🌑 new"),
        (FIRST - PRECISION, "🌒 waxing crescent"),
        (FIRST + PRECISION, "🌓 first quarter"),
        (FULL - PRECISION, "🌔 waxing gibbous"),
        (
            FULL + PRECISION,
            f"🌕 full {random.choice(full_moon_names[datetime.datetime.now().month])}",
        ),
        (LAST - PRECISION, "🌖 waning gibbous"),
        (LAST + PRECISION, "🌗last quarter"),
        (NEXTNEW - PRECISION, "🌘waning crescent"),
        (NEXTNEW + PRECISION, "🌑 new"),
    )
    i = bisect.bisect([a[0] for a in phase_strings], p / 27.99)
    return phase_strings[i][1]


def magichours(lat, lon, place):
    import datetime
    import tzlocal  # $ pip install tzlocal
    from astral import sun, LocationInfo
    from astral import moon
    from astral.sun import SunDirection
    from sty import fg, ef, rs

    magicHour = {"golden": [], "blue": []}
    today = datetime.datetime.today()
    mytz = tzlocal.get_localzone()
    l = LocationInfo("local", "local", mytz.zone, lat, lon)
    sunrise = sun.sunrise(l.observer, datetime.datetime.today(), mytz)
    sunset = sun.sunset(l.observer, datetime.datetime.today(), mytz)
    for direction in [SunDirection.RISING, SunDirection.SETTING]:
        magicHour["golden"].extend(
            sun.golden_hour(l.observer, today, direction, tzinfo=mytz)
        )
        magicHour["blue"].extend(
            sun.blue_hour(l.observer, today, direction, tzinfo=mytz)
        )
    # print(magicHour)
    morning = "%s %s %s %s" % (
        fg.blue + magicHour["blue"][0].strftime("%H:%M:%S") + rs.fg,
        fg.yellow + magicHour["golden"][0].strftime("%H:%M:%S") + rs.fg,
        fg.red + ef.bold + sunrise.strftime("%H:%M:%S") + rs.bold_dim + rs.fg,
        fg.yellow + magicHour["golden"][1].strftime("%H:%M:%S") + rs.fg,
    )
    evening = "%s %s %s %s" % (
        fg.yellow + magicHour["golden"][2].strftime("%H:%M:%S") + rs.fg,
        fg.red + ef.bold + sunset.strftime("%H:%M:%S") + rs.bold_dim + rs.fg,
        fg.yellow + magicHour["golden"][3].strftime("%H:%M:%S") + rs.fg,
        fg.blue + magicHour["blue"][3].strftime("%H:%M:%S") + rs.fg,
    )
    dawn = f"🌅 : {morning}"
    dusk = f"🌅 : \t\t    {evening}"

    luna = f"{phase_string(moon.phase(today))} moon"
    jc = sun.jday_to_jcentury(sun.julianday(today))
    srta = sun.sun_rt_ascension(jc)
    sdec = sun.sun_declination(jc)
    fullday = f"{dawn}\n{dusk}"
    # print( "at %s" % place )
    print(fullday)
    print(luna.title())


def main():
    """main"""
    verbose = False
    locate_me_str = g.locate_me()
    lat, lon = g.get_lat_lon(locate_me_str)
    where = g.known_location(lat, lon)
    magichours(lat, lon, where)
    if g.online():
        """
		Check if location has changed using CoreLocation (via LocateMe)
		This will compare the current results versus an existing text file
		"""
        # g.log_coordinates(locate_me_str)

    else:
        print(fg.red + ef.bold + "Offline" + rs.bold_dim + rs.fg)
        locateMeLog = [line.rstrip("\n") for line in open(logfile)]

        address = locateMeLog[1]
        print("Last seen at: %s" % (address))


if __name__ == "__main__":
    main()
