"""Write one sky file per day for the coming days: sky/days/YYYY-MM-DD.json.

Every slide's astrology must trace back to these files (positions are geocentric,
tropical, computed with ephem via manifest_sky.day). Run by .github/workflows/sky.yml.

    python sky/build_sky.py 21      # today (America/New_York) + 20 days

Each file covers one New York calendar day (midnight to midnight ET), so ingresses,
stations and lunations land on the date US readers see. `phase_label` is the phase
name to print (crescent/gibbous by illumination; quarters only on their own day).
"""
import datetime as dt, json, pathlib, sys
from zoneinfo import ZoneInfo
import manifest_sky as S
import lunations as L

OUT = pathlib.Path(__file__).parent / "days"
OUT.mkdir(exist_ok=True)
n = int(sys.argv[1]) if len(sys.argv) > 1 else 21
ET = ZoneInfo("America/New_York")
today = dt.datetime.now(ET).date()


def phase_label(s):
    """The phase name readers will see elsewhere (USNO / timeanddate convention):
    a quarter, New or Full Moon only on the New York day it happens; otherwise
    crescent below 50% lit, gibbous above."""
    if s["lunar_event"]:
        return s["lunar_event"]["event"] + " Moon" if "Quarter" in s["lunar_event"]["event"] else s["lunar_event"]["event"]
    m = s["moon"]
    return ("Waxing " if m["waxing"] else "Waning ") + ("crescent" if m["illumination"] < 50 else "gibbous")


for k in range(n):
    d = today + dt.timedelta(days=k)
    # Days run midnight to midnight New York time, the readers' calendar: an event at
    # 10:36 pm ET on the 15th (Pluto direct, 16 Oct 02:36 UTC) belongs to the 15th.
    s = S.day(d, ET)
    s["phase_label"] = phase_label(s)
    moon = s["positions"]["Moon"]["sign"]
    # Sun-sign whole-sign houses (plan decision D3): where today's Moon falls for each sign
    s["moon_house_by_sign"] = {sign: L.solar_house(moon, sign) for sign in L.SIGNS}
    s["retrograde"] = [b for b in S.PLANETS if s["positions"][b]["retrograde"]]
    (OUT / f"{d.isoformat()}.json").write_text(json.dumps(s, indent=1))
    print(d, "Moon", moon, s["phase_label"], "retro:", ",".join(s["retrograde"]) or "-")
