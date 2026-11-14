"""Week of 2026-11-17: content written from sky/days/*.json (houses = Sun-sign whole-sign, plan D3).
Run once to (re)write queue/<date>.json. Each day: status "approved" posts at 8am ET; set "hold" to skip.
Timing words are relative to the 8:00 am New York post.
"""
import json, pathlib

HERE = pathlib.Path(__file__).parent
TAGS = {"Fire": ["aries", "leo", "sagittarius"], "Earth": ["taurus", "virgo", "capricorn"],
        "Air": ["gemini", "libra", "aquarius"], "Water": ["cancer", "scorpio", "pisces"]}

DAYS = [
 dict(date="2026-11-17", element="Water",
      kicker="Tue · First Quarter Moon · Scorpio season",
      headline="First Quarter Moon this morning. Time to commit.",
      sky="The First Quarter Moon in Aquarius arrived this morning. She faces Mars and Jupiter today and moves into Pisces this afternoon",
      signs=[
       ("Cancer", "The First Quarter Moon lit your house of deep bonds this morning. Let one heartfelt intention become a real commitment.",
        "Which bond am I ready to invest in more deeply?"),
       ("Scorpio", "The First Quarter Moon arrived in your home zone this morning, and Mercury is moving forward in your sign. Choose one cozy change.",
        "What would make home feel like a soft landing?"),
       ("Pisces", "The Moon moves into your sign this afternoon, after a First Quarter in your quiet zone this morning. Make a wish just for you.",
        "What would I ask for if no one was listening?")],
      cta="Send this to your Water friend."),
 dict(date="2026-11-18", element="Fire",
      kicker="Wed · Waxing gibbous · Scorpio season",
      headline="The Moon and Mercury swapped notes this morning.",
      sky="Early this morning the Moon in Pisces made a friendly trine to Mercury, and overnight the Sun squared Jupiter in Leo",
      signs=[
       ("Aries", "The Moon drifts through your twelfth house, your quiet zone. Saturn is retrograde in your sign: rest is part of the plan.",
        "What would rest look like if I let it be easy?"),
       ("Leo", "Overnight the Sun squared Jupiter, in your sign: a tense angle that asks you to share the spotlight. The Moon is in your bonds house.",
        "Who would I love to shine beside?"),
       ("Sagittarius", "The Moon settles into your home zone. Jupiter, your ruling planet, felt a tense square from the Sun overnight: go easy at home.",
        "Which small comfort could I give myself tonight?")],
      cta="Send this to your Fire friend."),
 dict(date="2026-11-19", element="Earth",
      kicker="Thu · Waxing gibbous · Scorpio season",
      headline="Tonight the Sun and Moon share a warm glance.",
      sky="The Sun squares Mars around lunchtime, a tense angle, and makes a friendly trine to the Moon in Pisces tonight",
      signs=[
       ("Taurus", "The Moon visits your friendship house, and tonight the Sun sends her a friendly trine. Let a good friend in on your plans.",
        "Which friend feels like a warm blanket?"),
       ("Virgo", "The Moon lights your partnership house, in your opposite sign. Tonight's friendly trine from the Sun invites a sweet one-on-one.",
        "What do I love receiving from the people close to me?"),
       ("Capricorn", "The Moon is in your house of words. The Sun squares Mars around lunchtime, so pause before you reply, then speak kindly.",
        "What would I say if I trusted it would land well?")],
      cta="Save this for your evening journal."),
 dict(date="2026-11-20", element="Air",
      kicker="Friday · Waxing gibbous · Scorpio season",
      headline="The Moon dashed into Aries overnight. Bold move.",
      sky="The Moon moved into Aries overnight, sent friendly sextiles to Pluto and Uranus this morning and meets Saturn this afternoon",
      signs=[
       ("Gemini", "The Moon visits your friendship house. This morning she sent Uranus, retrograde in your sign, a friendly sextile: try a new plan.",
        "Which friend would say yes to a spontaneous plan?"),
       ("Libra", "The Moon lights your partnership house, across from your sign. She meets Saturn this afternoon: talk about what you both want.",
        "What would a steady, sweet partnership feel like?"),
       ("Aquarius", "The Moon is in your house of words, and she sent Pluto, in your sign, a friendly sextile this morning. Speak from the heart.",
        "Which true thing am I ready to say out loud?")],
      cta="Send this to your Air friend."),
 dict(date="2026-11-21", element="Water",
      kicker="Saturday · Waxing gibbous · Scorpio season",
      headline="The Moon makes eyes at Venus tonight.",
      sky="The Moon in Aries faces Venus in Libra tonight, an opposition, and sends Jupiter a friendly trine later tonight",
      signs=[
       ("Cancer", "The Moon lights your career house. Tonight she makes a friendly trine to Jupiter: let yourself picture the bigger version.",
        "What would I go for if I felt fully ready?"),
       ("Scorpio", "The Moon tidies your house of daily routines, and Mercury is moving forward in your sign. Give one weekend habit a fresh start.",
        "Which weekend ritual would refill my cup?"),
       ("Pisces", "The Moon sits in your house of values. Facing Venus tonight, she asks what you treasure most: spend your time on that.",
        "Where does my time feel most well spent?")],
      cta="Send this to your Water friend."),
 dict(date="2026-11-22", element="Fire",
      kicker="Sun · Waxing gibbous · Sagittarius season",
      headline="Sagittarius season arrived overnight. Pack a dream.",
      sky="The Sun moved into Sagittarius overnight. The Moon moved into Taurus early this morning and squares Pluto late this morning",
      signs=[
       ("Aries", "The Moon moved into your house of values early this morning. Spend today on what makes you feel worthy, just as you are.",
        "What makes me feel rich that costs nothing?"),
       ("Leo", "The Moon sent Mars, in your sign, a friendly trine overnight, then moved into your career house. Aim your fire at one goal.",
        "Which ambition makes me sit up straighter?"),
       ("Sagittarius", "The Sun moved into your sign overnight: your birthday season is here. The Moon is in your routines house: plan a treat.",
        "How would I like to celebrate this new year of me?")],
      cta="Save this for your birthday season."),
 dict(date="2026-11-23", element="Earth",
      kicker="Mon · Waxing gibbous · Sagittarius season",
      headline="The Moon is nearly full and glowing in Taurus.",
      sky="The Moon is 99% lit in Taurus today. She faced Mercury overnight, and the Sun makes a friendly trine to Neptune tonight",
      signs=[
       ("Taurus", "The Moon glows in your sign all day, nearly full. Venus, your ruling planet, is moving forward in Libra: treat yourself kindly.",
        "What does treating myself well look like today?"),
       ("Virgo", "The Moon lights your house of travel and big ideas. She faced Mercury, your ruling planet, overnight: rethink one plan.",
        "Which plan deserves a fresh perspective?"),
       ("Capricorn", "The Moon glows in your house of joy and romance. Tonight the Sun sends Neptune a friendly trine: let yourself daydream.",
        "What daydream keeps coming back to me?")],
      cta="Send this to your Earth friend."),
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
