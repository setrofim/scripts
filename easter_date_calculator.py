# Calculate the ecclesiastical date of Easter based on Gregorian Calendar in 
# a specified year.

# 4th century rule:
# "Easter is observed on the Sunday after the first full moon on or after 
# the day of the vernal equinox."
# 
# Assumptions made in ecclesiastical calculation:
#    * Full moon is the 14th day of a calendar lunar month
#    * Vernal equinox is on 21st March
#
# (Source: Wikipedia)

from math import floor
from datetime import date, timedelta

def easter_date(year):
    eastdate  = date(year, 3, 21)
    mnage = moon_age(eastdate.year, eastdate.month, eastdate.day)

    # Easter is the Sunday *after* the moon is 14 days old, hence 15
    if mnage < 15:
        eastdate += timedelta(round(15 - mnage))
    else:
        eastdate += timedelta(round(15 + 29.530588853 - mnage))
    
    # next Sunday
    eastdate += timedelta(6 - eastdate.weekday())

    return eastdate

# This function was cheeckily ripped from
# http://home.att.net/~srschmitt/script_moon_phase.html
def moon_age(year, month, day):
    yy = year - floor((12 - month) / 10)
    mm = month + 9
    if mm >= 12:
        mm = mm - 12

    k1 = floor(365.25 * (yy + 4712))
    k2 = floor(30.6 * mm + 0.5)
    k3 = floor(floor(yy / 100 + 49) * 0.75) - 38

    jd = k1 + k2 + day + 59
    if jd > 2299160:
        jd -= k3

    ip = (jd - 2451550.1) / 29.530588853
    ip = ip - floor(ip)
    if ip < 0:
        ip += 1
    return ip * 29.53


if __name__ == '__main__':
    import sys
    year = int(sys.argv[1])
    easter = easter_date(year)
    print "Easter in " + str(year) + " is on " + easter.strftime("%d %B")

