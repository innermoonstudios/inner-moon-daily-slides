"""Week of 2026-10-20: content written from sky/days/*.json (houses = Sun-sign whole-sign, plan D3).
Run once to (re)write queue/<date>.json. Each day: status "approved" posts at 8am ET; set "hold" to skip.
Timing words are relative to the 8:00 am New York post.
"""
import json, pathlib

HERE = pathlib.Path(__file__).parent
TAGS = {"Fire": ["aries", "leo", "sagittarius"], "Earth": ["taurus", "virgo", "capricorn"],
        "Air": ["gemini", "libra", "aquarius"], "Water": ["cancer", "scorpio", "pisces"]}

DAYS = [
 dict(date="2026-10-20", element="Water",
      kicker="Tuesday · Waxing gibbous · Libra season",
      headline="Venus and Pluto had a little standoff overnight.",
      sky="Venus, retrograde in Scorpio, squared Pluto overnight, and the Moon in Aquarius opposes Jupiter in Leo tonight",
      signs=[
       ("Cancer", "The Moon is in your house of deep bonds. Tonight she faces generous Jupiter: give from the heart, and let others give back.",
        "Where can I let someone meet me halfway?"),
       ("Scorpio", "Venus, retrograde in your sign, squared Pluto overnight. The Moon rests in your home zone; give old feelings a soft place to land.",
        "What feeling am I finally ready to set down?"),
       ("Pisces", "The Moon drifts through your twelfth house, your space for rest. As she squares Mercury this afternoon, think less and dream more.",
        "What would I hear if I gave myself an hour of quiet?")],
      cta="Send this to your Water friend."),
 dict(date="2026-10-21", element="Fire",
      kicker="Wednesday · Waxing gibbous · Libra season",
      headline="The Moon dives into Pisces and goes all soft-focus.",
      sky="The Moon slips into Pisces today, trines Venus around lunchtime and squares Uranus this evening",
      signs=[
       ("Aries", "The Moon glides into your twelfth house, your private retreat, today. Saturn is retrograde in your sign: slow down and let plans steep.",
        "What do I need to hear from myself before I act?"),
       ("Leo", "The Moon enters your house of intimacy and trines Venus today. With Mars and Jupiter in your sign, lead with tenderness, not volume.",
        "Who deserves the softer side of my fire?"),
       ("Sagittarius", "The Moon arrives in your home zone today and squares Uranus tonight. If plans wobble, cozy up and let home be the adventure.",
        "Where do I feel most at home in myself?")],
      cta="Send this to your Fire friend."),
 dict(date="2026-10-22", element="Earth",
      kicker="Thursday · Waxing gibbous · Libra season",
      headline="The Moon is daydreaming in Pisces. Join her.",
      sky="The Moon spends the whole day in Pisces and trines Mercury in Scorpio late tonight",
      signs=[
       ("Taurus", "The Moon floats through your friendship house. Venus, your ruler, is retrograde, so reach out to someone you've missed.",
        "Which friendship would I love to rekindle?"),
       ("Virgo", "The Moon is in Pisces, your opposite sign, lighting your partnership house. Let someone else take care of you for once.",
        "What would I receive if I stopped fixing everything?"),
       ("Capricorn", "The Moon swims through your house of words and short trips. Late tonight she trines Mercury: send the note or the voice memo.",
        "Who could use a kind word from me tonight?")],
      cta="Save this for your next quiet evening."),
 dict(date="2026-10-23", element="Air",
      kicker="Friday · Waxing gibbous · Scorpio season",
      headline="Scorpio season arrived this morning, darling.",
      sky="The Sun moved into Scorpio this morning, the Moon enters Aries this afternoon, and the Sun meets retrograde Venus late tonight",
      signs=[
       ("Gemini", "The Moon is in your career house while Uranus is retrograde in your sign. Revisit a work idea you shelved; it may sparkle now.",
        "Which shelved idea still makes my heart beat faster?"),
       ("Libra", "The Moon tidies your house of daily routines. Late tonight Venus, your ruler, meets the Sun. Keep it simple and glow quietly.",
        "What small ritual makes me feel most like me?"),
       ("Aquarius", "The Moon is in your house of values before entering Aries this afternoon. Pluto is in your sign: honor who you've grown into.",
        "What do I value now that I didn't a year ago?")],
      cta="Send this to your Air friend."),
 dict(date="2026-10-24", element="Water",
      kicker="Saturday · Waxing gibbous · Scorpio season",
      headline="Mercury went retrograde overnight. Reread, then send.",
      sky="Mercury turned retrograde in Scorpio overnight, and the Moon in Aries meets Saturn today and trines Mars tonight",
      signs=[
       ("Cancer", "The Moon lights your career house and meets Saturn today. Steady effort is your love language right now; show up for yourself.",
        "What am I building that makes me proud?"),
       ("Scorpio", "Mercury, the planet of words, turned retrograde in your sign overnight. Slow down, reread your messages, and choose kind words.",
        "Which conversation deserves a gentler second draft?"),
       ("Pisces", "The Moon is in your house of values and self-worth. Tonight she trines Mars: take one confident step toward what you treasure.",
        "What makes me feel rich in ways that matter?")],
      cta="Send this to your Water friend."),
 dict(date="2026-10-25", element="Fire",
      kicker="Sunday · Waxing gibbous · Scorpio season",
      headline="Venus moonwalked into Libra overnight.",
      sky="Venus, moving retrograde, slipped into Libra overnight. The Moon in Aries trines Jupiter today and opposes Venus tonight",
      signs=[
       ("Aries", "The Moon is in your sign and trines lucky Jupiter today. Tonight she faces Venus in Libra: lead with charm, not speed.",
        "What do I want to begin, boldly and kindly?"),
       ("Leo", "The Moon visits your house of travel and big ideas, trining Jupiter in your sign today. Let your curiosity off the leash.",
        "What would I explore if I trusted I'd enjoy the ride?"),
       ("Sagittarius", "The Moon lights your house of joy and romance and trines Jupiter, your ruler, today. Flirt with life a little; play counts.",
        "What made me laugh hardest this week?")],
      cta="Send this to your Fire friend."),
 dict(date="2026-10-26", element="Earth",
      kicker="Monday · Full Moon · Scorpio season",
      headline="The Full Moon peaked in Taurus overnight. Gorgeous.",
      sky="The Moon turned full in Taurus overnight, and the Sun in Scorpio squares Pluto today",
      signs=[
       ("Taurus", "The Full Moon lit up your sign overnight. Celebrate how far you've come, then gently release one thing that no longer fits.",
        "What am I proud of that I haven't said out loud?"),
       ("Virgo", "The Full Moon is in your house of wisdom and wide horizons. Mercury, your ruler, is retrograde: revisit a lesson before a new one.",
        "What lesson keeps returning, and what is it asking?"),
       ("Capricorn", "The Full Moon glows in your house of creativity and joy. As she squares Mars tonight, play with heart, not pressure.",
        "Where can I trade pressure for play this week?")],
      cta="Save this for your Full Moon ritual."),
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
