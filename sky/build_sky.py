"""Write one sky file per day for the coming days: sky/days/YYYY-MM-DD.json.

Every slide's astrology must trace back to these files (positions are geocentric,
tropical, computed with ephem via manifest_sky.day). Run by .github/workflows/sky.yml.

    python sky/build_sky.py 21      # today (America/New_York) + 20 days
"""
import datetime as dt, json, pathlib, sys
from zoneinfo import ZoneInfo
import manifest_sky as S
import lunations as L

OUT = pathlib.Path(__file__).parent / "days"
OUT.mkdir(exist_ok=True)
n = int(sys.argv[1]) if len(sys.argv) > 1 else 21
today = dt.datetime.now(ZoneInfo("America/New_York")).date()
for k in range(n):
    d = today + dt.timedelta(days=k)
    s = S.day(d)
    moon = s["positions"]["Moon"]["sign"]
    # Sun-sign whole-sign houses (plan decision D3): where today's Moon falls for each sign
    s["moon_house_by_sign"] = {sign: L.solar_house(moon, sign) for sign in L.SIGNS}
    s["retrograde"] = [b for b in S.PLANETS if s["positions"][b]["retrograde"]]
    (OUT / f"{d.isoformat()}.json").write_text(json.dumps(s, indent=1))
    print(d, "Moon", moon, s["moon"]["phase"], "retro:", ",".join(s["retrograde"]) or "-")
