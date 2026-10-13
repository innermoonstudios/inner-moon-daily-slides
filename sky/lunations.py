"""Twelve Full Moons from a given start, with tropical sign, degree and
local time in whichever zone the edition prints.

Assembly rule 1 of the production master: verify each Full Moon's date and
sign from a reliable ephemeris, and include the degree only if verified.

The zone matters to more than the clock. A Full Moon near midnight falls on a
different calendar date in different zones, so a made-to-order Journal is
computed in the reader's own zone while a stock Guide, which has no single
reader, is computed in UTC.
"""
import datetime as dt
from zoneinfo import ZoneInfo
import ephem

ET = ZoneInfo("America/New_York")
UTC = ZoneInfo("UTC")

SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]


def to_dt(ephem_date):
    y, m, d, hh, mm, ss = ephem_date.tuple()
    whole = int(ss)
    micro = int(round((ss - whole) * 1e6))
    return dt.datetime(y, m, d, hh, mm, whole, micro, tzinfo=UTC)


def _ecliptic_longitude(body, when_utc):
    """Tropical ecliptic longitude of a body, apparent geocentric, of date.

    Astrology is geocentric: positions are measured from the centre of the
    Earth, not from a point on its surface. Computing a body against an
    ephem.Observer() gives the *topocentric* position instead, which for the
    Moon differs by up to ~0.85° of lunar parallax — enough to print the
    wrong degree, and occasionally the wrong sign. So compute the body bare
    and read its geocentric g_ra/g_dec rather than the observer's ra/dec.
    """
    d = ephem.Date(when_utc.astimezone(UTC).replace(tzinfo=None))
    body.compute(d)
    ecl = ephem.Ecliptic(ephem.Equatorial(body.g_ra, body.g_dec, epoch=d), epoch=d)
    return float(ecl.lon) * 180.0 / ephem.pi % 360.0


def moon_position(when_utc):
    """Tropical ecliptic longitude of the Moon, apparent geocentric."""
    lon = _ecliptic_longitude(ephem.Moon(), when_utc)
    idx = int(lon // 30)
    return SIGNS[idx], lon - idx * 30, lon


def sun_position(when_utc):
    """Tropical ecliptic longitude of the Sun, apparent geocentric."""
    lon = _ecliptic_longitude(ephem.Sun(), when_utc)
    idx = int(lon // 30)
    return SIGNS[idx], lon - idx * 30, lon


def full_moons(start, count=12, tz=ET):
    out = []
    cursor = ephem.Date(start.astimezone(UTC).replace(tzinfo=None))
    for _ in range(count):
        fm = ephem.next_full_moon(cursor)
        when = to_dt(fm)
        sign, deg, lon = moon_position(when)
        # A Full Moon *is* the exact opposition: the Moon's geocentric
        # longitude is the Sun's plus 180°. This catches a position computed
        # topocentrically by mistake, which parallax pulls off by up to 0.85°.
        opposition = (lon - sun_position(when)[2]) % 360.0
        if abs(opposition - 180.0) > 0.01:
            raise AssertionError(
                f"{when:%Y-%m-%d %H:%M} UTC: Moon is {opposition:.4f}° from the "
                f"Sun at Full Moon, expected 180° — position is not geocentric")
        local = when.astimezone(tz)
        out.append({
            "utc": when,
            "local": local,
            "sign": sign,
            "degree": deg,
            "longitude": lon,
            "tzname": local.tzname(),
        })
        cursor = ephem.Date(fm + 1.0)
    return out


def house_from(full_moon_sign, anchor_sign):
    """Which house a Full Moon falls in, counting forward from an anchor.

    Both house systems this project uses are the same arithmetic with a
    different anchor: whole-sign houses put the *rising* sign on the 1st,
    solar houses put the *Sun* sign there.
    """
    return (SIGNS.index(full_moon_sign) - SIGNS.index(anchor_sign)) % 12 + 1


def whole_sign_house(full_moon_sign, rising_sign):
    """Whole-sign houses — needs a birth time to know the rising sign."""
    return house_from(full_moon_sign, rising_sign)


def solar_house(full_moon_sign, sun_sign):
    """Solar houses — the standard convention when the birth time is not
    known. The Sun's sign is treated as the 1st house."""
    return house_from(full_moon_sign, sun_sign)


ORDINAL_HOUSE = ["", "1st", "2nd", "3rd", "4th", "5th", "6th",
                 "7th", "8th", "9th", "10th", "11th", "12th"]


def fmt_date(local):
    return local.strftime("%A, %B ") + str(local.day) + local.strftime(", %Y")


def fmt_time(local):
    # Round to the nearest minute, as published lunation tables do: the
    # September 2026 Full Moon falls at 16:48:57 UTC and is listed as 12:49
    # p.m. EDT, not 12:48.
    local = (local + dt.timedelta(seconds=30)).replace(second=0, microsecond=0)
    h = local.strftime("%I").lstrip("0")
    return f'{h}:{local.strftime("%M")} {"a.m." if local.hour < 12 else "p.m."} {local.tzname()}'


def fmt_degree(deg):
    d = int(deg)
    m = int(round((deg - d) * 60))
    if m == 60:
        d, m = d + 1, 0
    return f"{d}°{m:02d}′"


if __name__ == "__main__":
    rising = "Cancer"
    start = dt.datetime(2026, 9, 20, tzinfo=ET)
    for i, fm in enumerate(full_moons(start, 12), 1):
        h = whole_sign_house(fm["sign"], rising)
        print(f'{i:2d}  {fmt_date(fm["local"]):<28s} {fmt_time(fm["local"]):>18s}   '
              f'{fm["sign"]:<12s} {fmt_degree(fm["degree"]):>8s}   '
              f'house {ORDINAL_HOUSE[h]:<5s}  (UTC {fm["utc"]:%Y-%m-%d %H:%M})')
