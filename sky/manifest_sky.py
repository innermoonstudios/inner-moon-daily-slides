"""The sky, day by day, for one Manifest cycle — computed, never written by hand.

The cosmic narrative tells the reader what is happening overhead each day and
what it means for their sign. That only has value if it is true, so every claim
a sky passage makes has to trace back to this module, the same way Assembly
rule 1 requires every Full Moon date and sign to come from the ephemeris.

Positions are GEOCENTRIC apparent ecliptic longitudes of date — the convention
astrology uses, and the same convention `lunations.moon_position` follows, so
degrees quoted from either module agree.

    .venv/bin/python manifest_sky.py 2026-09 Gemini      # the cycle's sky, as a table
"""
import datetime as dt
import sys
from zoneinfo import ZoneInfo

import ephem

import lunations as L

UTC = dt.timezone.utc
BODIES = {
    "Sun": ephem.Sun, "Moon": ephem.Moon, "Mercury": ephem.Mercury,
    "Venus": ephem.Venus, "Mars": ephem.Mars, "Jupiter": ephem.Jupiter,
    "Saturn": ephem.Saturn, "Uranus": ephem.Uranus, "Neptune": ephem.Neptune,
    "Pluto": ephem.Pluto,
}
PLANETS = [b for b in BODIES if b not in ("Sun", "Moon")]
ASPECTS = {"conjunct": 0, "sextile": 60, "square": 90, "trine": 120, "opposite": 180}
RULER = {"Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
         "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Pluto",
         "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Uranus",
         "Pisces": "Neptune"}
ELEMENT = {s: e for e, signs in {
    "Fire": ("Aries", "Leo", "Sagittarius"), "Earth": ("Taurus", "Virgo", "Capricorn"),
    "Air": ("Gemini", "Libra", "Aquarius"), "Water": ("Cancer", "Scorpio", "Pisces"),
}.items() for s in signs}
MODALITY = {s: m for m, signs in {
    "Cardinal": ("Aries", "Cancer", "Libra", "Capricorn"),
    "Fixed": ("Taurus", "Leo", "Scorpio", "Aquarius"),
    "Mutable": ("Gemini", "Virgo", "Sagittarius", "Pisces"),
}.items() for s in signs}

# Orbs for "in effect" when a passage cites an aspect on a day it isn't exact.
ORB = {"Moon": 6.0, "default": 3.0}


# ----------------------------------------------------------------- positions
def lon(body, when):
    d = ephem.Date(when.astimezone(UTC).replace(tzinfo=None))
    b = BODIES[body]()
    b.compute(d)
    ecl = ephem.Ecliptic(ephem.Equatorial(b.g_ra, b.g_dec, epoch=d), epoch=d)
    return float(ecl.lon) * 180.0 / ephem.pi % 360.0


def sign_of(longitude):
    i = int(longitude // 30)
    return L.SIGNS[i], longitude - 30 * i


def speed(body, when):
    """Degrees per day; negative means retrograde."""
    h = dt.timedelta(hours=6)
    return ((lon(body, when + h) - lon(body, when - h) + 540) % 360 - 180) * 2


def _bisect(f, a, b, steps=30):
    fa = f(a)
    for _ in range(steps):
        m = a + (b - a) / 2
        fm = f(m)
        if (fa < 0) == (fm < 0):
            a, fa = m, fm
        else:
            b = m
    return a + (b - a) / 2


def _wrap(x):
    return (x + 180) % 360 - 180


# ------------------------------------------------------------------ one day
def day(date, tz=UTC):
    """Everything overhead during one calendar day, midnight to midnight in `tz`.

    The default is a UTC day, which the printed products use (a stock book has
    no single reader). The daily Instagram posts are read in the US, so their
    sky file should pass tz=ZoneInfo("America/New_York"): several events fall on
    a different calendar date there (Mars into Leo is 27 Sep 2026 in New York,
    28 Sep in UTC; Pluto turns direct 15 Oct vs 16 Oct). Steps are taken in UTC
    so a daylight-saving change gives a 23- or 25-hour day, not a wrong one.
    """
    t0 = dt.datetime(date.year, date.month, date.day, tzinfo=tz).astimezone(UTC)
    t1 = dt.datetime.combine(date + dt.timedelta(days=1), dt.time(), tzinfo=tz).astimezone(UTC)
    noon = dt.datetime.combine(date, dt.time(12), tzinfo=tz).astimezone(UTC)
    n_hours = round((t1 - t0).total_seconds() / 3600)
    hours = [t0 + dt.timedelta(hours=h) for h in range(n_hours + 1)]
    out = {"date": date.isoformat(), "tz": str(tz), "positions": {}, "ingresses": [], "stations": [],
           "aspects": [], "lunar_event": None}

    for body in BODIES:
        l0, l1, ln = lon(body, t0), lon(body, t1), lon(body, noon)
        s_noon, d_noon = sign_of(ln)
        v = speed(body, noon)
        out["positions"][body] = {
            "sign": s_noon, "degree": round(d_noon, 2), "retrograde": v < 0,
            "sign_start": sign_of(l0)[0], "sign_end": sign_of(l1)[0],
            "signs_today": sorted({sign_of(l0)[0], s_noon, sign_of(l1)[0]},
                                  key=L.SIGNS.index),
        }
        if sign_of(l0)[0] != sign_of(l1)[0]:
            boundary = (int(l1 // 30) * 30) if v > 0 else (int(l0 // 30) * 30)
            t = _bisect(lambda x: _wrap(lon(body, x) - boundary), t0, t1)
            out["ingresses"].append({"body": body, "sign": sign_of(l1)[0],
                                     "from": sign_of(l0)[0], "utc": t.isoformat()})
        if body not in ("Sun", "Moon"):
            v0, v1 = speed(body, t0), speed(body, t1)
            if (v0 < 0) != (v1 < 0):
                t = _bisect(lambda x: speed(body, x), t0, t1)
                out["stations"].append({"body": body, "turns": "retrograde" if v1 < 0 else "direct",
                                        "sign": sign_of(lon(body, t))[0],
                                        "degree": round(sign_of(lon(body, t))[1], 2),
                                        "utc": t.isoformat()})

    names = list(BODIES)
    lons = {h: {b: lon(b, h) for b in names} for h in hours}
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            for asp, angle in ASPECTS.items():
                for target in {angle, (360 - angle) % 360}:
                    f = [_wrap(lons[h][a] - lons[h][b] - target) for h in hours]
                    for k in range(n_hours):
                        if (f[k] < 0) != (f[k + 1] < 0) and abs(f[k]) < 20:
                            t = _bisect(lambda x: _wrap(lon(a, x) - lon(b, x) - target),
                                        hours[k], hours[k + 1])
                            out["aspects"].append({"a": a, "aspect": asp, "b": b,
                                                   "utc": t.isoformat()})

    e = ephem.Date(t0.replace(tzinfo=None))   # t0 is already UTC
    for name, fn in (("New Moon", ephem.next_new_moon), ("First Quarter", ephem.next_first_quarter_moon),
                     ("Full Moon", ephem.next_full_moon), ("Last Quarter", ephem.next_last_quarter_moon)):
        t = L.to_dt(fn(e))
        if t0 <= t < t1:
            out["lunar_event"] = {"event": name, "utc": t.isoformat(),
                                  "sign": sign_of(lon("Moon", t))[0],
                                  "degree": round(sign_of(lon("Moon", t))[1], 2)}
    m = ephem.Moon(ephem.Date(noon.replace(tzinfo=None)))
    elong = (lon("Moon", noon) - lon("Sun", noon)) % 360
    out["moon"] = {"illumination": round(m.moon_phase * 100), "waxing": elong < 180,
                   "phase": phase_name(elong)}
    return out


def phase_name(elong):
    for limit, name in ((10, "New"), (80, "Waxing Crescent"), (100, "First Quarter"),
                        (170, "Waxing Gibbous"), (190, "Full"), (260, "Waning Gibbous"),
                        (280, "Last Quarter"), (350, "Waning Crescent"), (360, "New")):
        if elong < limit:
            return name


def cycle(dates, tz=UTC):
    return {d.isoformat(): day(d, tz) for d in dates}


def in_orb(sky_day, a, aspect, b):
    """Whether an aspect is exact today or within orb at noon."""
    for x in sky_day["aspects"]:
        if {x["a"], x["b"]} == {a, b} and x["aspect"] == aspect:
            return True
    tz = ZoneInfo(sky_day["tz"]) if sky_day.get("tz", "UTC") != "UTC" else UTC
    noon = dt.datetime.combine(dt.date.fromisoformat(sky_day["date"]), dt.time(12),
                               tzinfo=tz).astimezone(UTC)
    sep = abs(_wrap(lon(a, noon) - lon(b, noon)))
    orb = ORB["Moon"] if "Moon" in (a, b) else ORB["default"]
    return abs(sep - ASPECTS[aspect]) <= orb


# --------------------------------------------------------------------- report
if __name__ == "__main__":
    import manifest_architecture as A
    import make_manifest_master as MM
    ym, sign = sys.argv[1], sys.argv[2]
    opening, (new, _), closing = MM.cycle_instants(ym)
    plan = A.stage_plan(opening["utc"], new, closing["utc"])
    for d, stage in plan:
        s = day(d)
        p = s["positions"]
        moon = p["Moon"]
        house = L.solar_house(moon["sign"], sign)
        retro = [b for b in PLANETS if p[b]["retrograde"]]
        print(f"\n{d:%a %d %b}  [{stage}]  Moon {'/'.join(moon['signs_today'])} "
              f"(noon {moon['sign']} {moon['degree']:.0f}°, {L.ORDINAL_HOUSE[house]} house)  "
              f"{s['moon']['phase']} {s['moon']['illumination']}%")
        print("   " + "  ".join(f"{b[:3]} {p[b]['sign'][:3]} {p[b]['degree']:.0f}{'R' if p[b]['retrograde'] else ''}"
                             for b in BODIES if b != "Moon"))
        for x in s["ingresses"]:
            print(f"   ingress  {x['body']} → {x['sign']}  {x['utc'][11:16]} UTC")
        for x in s["stations"]:
            print(f"   STATION  {x['body']} turns {x['turns']} at {x['sign']} {x['degree']:.1f}°  {x['utc'][11:16]} UTC")
        if s["lunar_event"]:
            e = s["lunar_event"]
            print(f"   LUNAR    {e['event']} in {e['sign']} {e['degree']:.1f}°  {e['utc'][11:16]} UTC")
        for x in s["aspects"]:
            if "Moon" not in (x["a"], x["b"]):
                print(f"   aspect   {x['a']} {x['aspect']} {x['b']}  {x['utc'][11:16]} UTC")
        moon_asp = [f"{x['b'] if x['a']=='Moon' else x['a']} ({x['aspect']})" for x in s["aspects"] if "Moon" in (x["a"], x["b"])]
        if moon_asp:
            print("   moon     " + ", ".join(moon_asp))
