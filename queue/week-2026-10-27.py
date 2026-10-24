"""Week of 2026-10-27: content written from sky/days/*.json (houses = Sun-sign whole-sign, plan D3).
Run once to (re)write queue/<date>.json. Each day: status "approved" posts at 8am ET; set "hold" to skip.
Timing words are relative to the 8:00 am New York post.
"""
import json, pathlib

HERE = pathlib.Path(__file__).parent
TAGS = {"Fire": ["aries", "leo", "sagittarius"], "Earth": ["taurus", "virgo", "capricorn"],
        "Air": ["gemini", "libra", "aquarius"], "Water": ["cancer", "scorpio", "pisces"]}

DAYS = [
 dict(date="2026-10-27", element="Air",
      kicker="Tuesday · Waning gibbous · Scorpio season",
      headline="The Moon packs her bags for Gemini tonight.",
      sky="The Moon in Taurus squares Jupiter today and slips into Gemini tonight, while Mercury is retrograde in Scorpio",
      signs=[
       ("Gemini", "The Moon rests in your twelfth house, your quiet zone, before she enters your sign tonight. Nap now; sparkle later.",
        "What would I love to begin once I feel rested?"),
       ("Libra", "The Moon visits your house of deep bonds. Venus is retrograde in your sign, moving backward: revisit what you truly treasure.",
        "Which bond feels worth a second, slower look?"),
       ("Aquarius", "The Moon settles into your home zone and squares big-hearted Jupiter today. Feelings may swell; let them be generous ones.",
        "What small change would make home feel softer?")],
      cta="Send this to your Air friend."),
 dict(date="2026-10-28", element="Water",
      kicker="Wed · Waning gibbous · Scorpio season",
      headline="The Moon met Uranus overnight. Sparks flew.",
      sky="The Moon in Gemini met retrograde Uranus overnight and makes a friendly sextile to Saturn this afternoon",
      signs=[
       ("Cancer", "The Moon drifts through your twelfth house, your space for rest and dreams. Lighter plans and an early night suit you.",
        "What would I dream up if no one was watching?"),
       ("Scorpio", "Mercury is retrograde in your sign, and the Moon visits your house of deep bonds. Say the tender thing slowly, and mean it.",
        "Who have I been meaning to truly open up to?"),
       ("Pisces", "The Moon is in your home zone and makes a friendly angle to Saturn this afternoon. Small, steady nesting goes a long way.",
        "Where in my home could I make room for calm?")],
      cta="Save this for your next cozy night in."),
 dict(date="2026-10-29", element="Fire",
      kicker="Thursday · Waning gibbous · Scorpio season",
      headline="The Moon is winking at Jupiter and Venus today.",
      sky="The Moon in Gemini makes friendly angles to Jupiter at lunchtime and Venus this evening, then slips into Cancer tonight",
      signs=[
       ("Aries", "The Moon chats through your house of words and short trips. Saturn is retrograde in your sign: say less, mean more, smile often.",
        "What message would I love to send today?"),
       ("Leo", "Jupiter is in your sign, and the Moon in your friendship house sends it a friendly wink at lunchtime. Call in your people.",
        "Who in my circle deserves a big thank-you?"),
       ("Sagittarius", "The Moon is in Gemini, your opposite sign, lighting your partnership house. She winks at Venus this evening: let someone charm you.",
        "Who would I love to know a little better?")],
      cta="Send this to your Fire friend."),
 dict(date="2026-10-30", element="Earth",
      kicker="Friday · Waning gibbous · Scorpio season",
      headline="The Sun and Moon are holding hands today.",
      sky="The Moon in Cancer trines the Sun in Scorpio today and squares Saturn this afternoon, as retrograde Mercury squares Mars",
      signs=[
       ("Taurus", "The Moon nests in your house of words and short trips. Retrograde Mercury squares Mars today: pause before you hit send.",
        "What do I want to say once my heart is calm?"),
       ("Virgo", "The Moon visits your friendship house and makes a sweet trine to the Sun today. Let a friend fuss over you a little.",
        "Who in my life feels like a soft landing?"),
       ("Capricorn", "The Moon is in Cancer, your opposite sign, lighting your partnership house. She squares Saturn this afternoon: be patient with love.",
        "Where could I meet someone with more patience?")],
      cta="Send this to your Earth friend."),
 dict(date="2026-10-31", element="Air",
      kicker="Saturday · Waning gibbous · Scorpio season",
      headline="Happy Halloween. The Moon is pouting prettily in Cancer.",
      sky="The Moon in Cancer trined retrograde Mercury overnight and squares retrograde Venus this evening",
      signs=[
       ("Gemini", "The Moon is in your house of values and self-worth. Uranus is retrograde in your sign: rethink what helps you feel secure.",
        "What helps me feel safe, steady and supported?"),
       ("Libra", "The Moon lights your career house and squares Venus, retrograde in your sign, this evening. Be as kind to yourself as to others.",
        "Where can I give myself the grace I give others?"),
       ("Aquarius", "The Moon tidies your house of daily routines. Pluto is in your sign: trade one old habit for one that fits who you are now.",
        "Which daily habit am I ready to outgrow?")],
      cta="Send this to your Air friend."),
 dict(date="2026-11-01", element="Water",
      kicker="Sun · Last Quarter Moon · Scorpio season",
      headline="Last Quarter Moon in Leo this afternoon. Time to edit.",
      sky="The Moon slipped into Leo overnight and reaches her Last Quarter, half lit and waning, this afternoon, when she also trines Saturn",
      signs=[
       ("Cancer", "The Moon entered Leo overnight, lighting your house of self-worth. At this afternoon's Last Quarter, release one thing you've outgrown.",
        "What could I release to feel more like myself?"),
       ("Scorpio", "Mercury is retrograde in your sign as the Moon reaches her Last Quarter in your career house. Review before you reach higher.",
        "Which goal deserves a fresh, honest look?"),
       ("Pisces", "The Moon is in your house of daily routines, and this afternoon's Last Quarter invites a gentle clear-out. Start with one drawer.",
        "What small clear-out would make me feel lighter?")],
      cta="Save this for your next Last Quarter."),
 dict(date="2026-11-02", element="Fire",
      kicker="Monday · Waning crescent · Scorpio season",
      headline="The Moon has a date with Mars and Jupiter today.",
      sky="The Moon in Leo meets Mars today and Jupiter this evening, then makes a friendly sextile to Venus tonight",
      signs=[
       ("Aries", "The Moon lights your house of joy and romance and meets Mars today. Saturn is retrograde in your sign, so play first, plan later.",
        "What would I do today purely for the fun of it?"),
       ("Leo", "The Moon is in your sign and meets Mars today and Jupiter this evening, both in Leo. You're the main character; be a generous one.",
        "How can I share my glow with someone today?"),
       ("Sagittarius", "The Moon visits your house of travel and big ideas and meets Jupiter this evening. Let one bold idea out to play.",
        "Which horizon keeps calling my name lately?")],
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
