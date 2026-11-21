"""Week of 2026-11-24: content written from sky/days/*.json (houses = Sun-sign whole-sign, plan D3).
Run once to (re)write queue/<date>.json. Each day: status "approved" posts at 8am ET; set "hold" to skip.
Timing words are relative to the 8:00 am New York post.
"""
import json, pathlib

HERE = pathlib.Path(__file__).parent
TAGS = {"Fire": ["aries", "leo", "sagittarius"], "Earth": ["taurus", "virgo", "capricorn"],
        "Air": ["gemini", "libra", "aquarius"], "Water": ["cancer", "scorpio", "pisces"]}

DAYS = [
 dict(date="2026-11-24", element="Air",
      kicker="Tue · Full Moon · Sagittarius season",
      headline="The Full Moon in Gemini has a lot to say.",
      sky="The Moon moved into Gemini early this morning and turns full there mid-morning. She meets Uranus around midday and sends Saturn a friendly sextile tonight",
      signs=[
       ("Gemini", "The Full Moon peaks in your sign this morning, then meets Uranus, also in Gemini, around midday. Let yourself be seen.",
        "What part of me is ready for the spotlight?"),
       ("Libra", "The Full Moon lights your house of travel and big ideas. Venus, your ruling planet, is in your sign: dream generously.",
        "Where would my heart travel if I let it?"),
       ("Aquarius", "The Full Moon glows in your house of joy. Late this morning she sends Pluto, in your sign, a friendly trine: play a little.",
        "What lights me up when no one is watching?")],
      cta="Save this for Full Moon night."),
 dict(date="2026-11-25", element="Water",
      kicker="Wed · Waning gibbous · Sagittarius season",
      headline="Mars packs his bags for Virgo this evening.",
      sky="The Moon is in Gemini all day. The Sun faces Uranus this evening, Mars moves into Virgo this evening, and the Moon sends Venus a friendly trine late tonight",
      signs=[
       ("Cancer", "The Moon drifts through your twelfth house, your quiet zone. Late tonight she sends Venus a sweet trine: rest, then dream.",
        "What would I dream about if I let myself rest?"),
       ("Scorpio", "The Moon is in your house of deep bonds, and Mercury is in your sign. Say the tender thing to someone you trust.",
        "Who has earned a little more of my trust?"),
       ("Pisces", "The Moon lights your home zone. Neptune, your modern ruler, is retrograde, so it seems to drift backward: slow down at home.",
        "Where at home do I feel most like myself?")],
      cta="Send this to your Water friend."),
 dict(date="2026-11-26", element="Fire",
      kicker="Thu · Waning gibbous · Sagittarius season",
      headline="The Moon came home to Cancer early this morning.",
      sky="The Moon moved into Cancer early this morning. She squares Neptune this morning and Saturn this evening, both in Aries",
      signs=[
       ("Aries", "The Moon moved into your home zone early this morning. This evening she squares Saturn, in your sign: keep table talk gentle.",
        "Who makes home feel warm for me?"),
       ("Leo", "The Moon rests in your quiet zone. Overnight she sent Jupiter, in your sign, a friendly sextile: count your blessings softly.",
        "Which quiet blessing am I most thankful for?"),
       ("Sagittarius", "The Sun is in your sign, and the Moon visits your house of deep bonds. Let someone close see how grateful you are.",
        "Who would I love to thank out loud today?")],
      cta="Send this to your Fire friend."),
 dict(date="2026-11-27", element="Earth",
      kicker="Fri · Waning gibbous · Sagittarius season",
      headline="The Moon wants a heart-to-heart this morning.",
      sky="The Moon is in Cancer all day and makes a friendly trine to Mercury in Scorpio this morning",
      signs=[
       ("Taurus", "The Moon is in your house of words, and this morning she trines Mercury, a friendly angle. Send the kind message.",
        "What kind words have I been saving for someone?"),
       ("Virgo", "The Moon lights your friendship house, and Mars is in your sign. Spend your energy on a friend who cheers you on.",
        "Who cheers me on without being asked?"),
       ("Capricorn", "The Moon is in your partnership house, across from your sign. Saturn, your ruling planet, is retrograde: go slow and sweet.",
        "What do I want to build with someone I trust?")],
      cta="Save this for a cozy night in."),
 dict(date="2026-11-28", element="Air",
      kicker="Sat · Waning gibbous · Sagittarius season",
      headline="The Moon strutted into Leo this morning.",
      sky="The Moon moved into Leo early this morning, and Venus sent Jupiter a friendly sextile around 7 am. The Sun makes a friendly trine to the Moon this evening",
      signs=[
       ("Gemini", "The Moon is in your house of words. Around midday she sends Uranus, in your sign, a friendly sextile: say the unexpected.",
        "What surprising idea wants to be shared?"),
       ("Libra", "The Moon lights your friendship house. Early this morning Venus, your ruler, sent Jupiter a friendly sextile: be generous.",
        "Which friend could use a little extra love?"),
       ("Aquarius", "The Moon is in your partnership house, across from your sign. Around noon she faces Pluto, in your sign: meet halfway.",
        "Where could I meet someone halfway?")],
      cta="Send this to your Air friend."),
 dict(date="2026-11-29", element="Water",
      kicker="Sun · Waning gibbous · Sagittarius season",
      headline="Uranus and Pluto traded friendly glances.",
      sky="Uranus made a friendly trine to Pluto early this morning. The Moon is in Leo all day and squares Mercury in Scorpio this afternoon",
      signs=[
       ("Cancer", "The Moon, your ruling planet, warms your house of values. Spend your Sunday on what you truly treasure.",
        "Which treasure of mine deserves more of my time?"),
       ("Scorpio", "The Moon lights your career house and squares Mercury, in your sign, this afternoon, a tense angle. Plan, then pause.",
        "Which goal deserves a calmer plan?"),
       ("Pisces", "The Moon tends your house of daily routines. Neptune, your modern ruler, is retrograde: keep today's rhythm slow and kind.",
        "Which small routine makes me feel held?")],
      cta="Send this to your Water friend."),
 dict(date="2026-11-30", element="Fire",
      kicker="Mon · Waning gibbous · Sagittarius season",
      headline="The Moon had a late-night date with Jupiter.",
      sky="Overnight the Sun made a friendly trine to Saturn and the Moon met Jupiter in Leo. She moves into Virgo this morning and meets Mars around lunchtime",
      signs=[
       ("Aries", "The Moon moves into your routines house this morning and meets Mars, your ruling planet, around lunchtime. Start one fresh habit.",
        "Which new habit would make Monday feel lighter?"),
       ("Leo", "Overnight the Moon met Jupiter in your sign. This morning she moves into your house of values: honor what you are worth.",
        "What am I worth that I sometimes forget?"),
       ("Sagittarius", "Overnight the Sun, in your sign, made a friendly trine to Saturn. The Moon lights your career house: take one steady step.",
        "What steady step moves my dream forward?")],
      cta="Send this to your Fire friend."),
]

for d in DAYS:
    names = [s[0] for s in d["signs"]]
    tags = " ".join("#" + t for t in [d["element"].lower() + "signs"] + TAGS[d["element"]] + ["moonjournal"])
    caption = (f"{d['headline']}\n\n{d['sky']}. Swipe for {names[0]}, {names[1]} and {names[2]}, "
               f"plus one question to journal on today.\n\nSave this for tonight, or send it to your "
               f"{d['element']} friend. 🌙\n\n{tags}")
    q = {"date": d["date"], "element": d["element"], "status": "approved",
         "sky_file": f"sky/days/{d['date']}.json", "caption": caption,
         "slides": [{"template": "hook", "kicker": d["kicker"], "headline": d["headline"],
                     "sub": f"Today's sky for the {d['element']} signs"}]
                   + [{"template": "sign", "element": d["element"], "sign": n, "body": b, "question": qu}
                      for n, b, qu in d["signs"]]
                   + [{"template": "cta", "headline": d["cta"], "sub": "Daily prompts and moon journals"}]}
    (HERE / f"{d['date']}.json").write_text(json.dumps(q, indent=1, ensure_ascii=False) + "\n")
    print(d["date"], d["element"], "written")
