"""Week of 2026-11-03: content written from sky/days/*.json (houses = Sun-sign whole-sign, plan D3).
Run once to (re)write queue/<date>.json. Each day: status "approved" posts at 8am ET; set "hold" to skip.
Timing words are relative to the 8:00 am New York post.
"""
import json, pathlib

HERE = pathlib.Path(__file__).parent
TAGS = {"Fire": ["aries", "leo", "sagittarius"], "Earth": ["taurus", "virgo", "capricorn"],
        "Air": ["gemini", "libra", "aquarius"], "Water": ["cancer", "scorpio", "pisces"]}

DAYS = [
 dict(date="2026-11-03", element="Earth",
      kicker="Tuesday · Waning crescent · Scorpio season",
      headline="The Moon slipped into Virgo overnight, all business.",
      sky="The Moon slipped into Virgo overnight and squares retrograde Uranus late this morning",
      signs=[
       ("Taurus", "The Moon lights your house of joy and creativity. She squares Uranus, a tense angle, late this morning: let a surprise spark an idea.",
        "What would I create if it didn't have to be perfect?"),
       ("Virgo", "The Moon entered your sign overnight, so today is about you. Her tense square to Uranus late this morning asks for flexible plans.",
        "Where could a little flexibility set me free?"),
       ("Capricorn", "The Moon visits your house of travel and big ideas. When she squares Uranus late this morning, welcome the unexpected detour.",
        "Which belief am I ready to stretch a little?")],
      cta="Send this to your Earth friend."),
 dict(date="2026-11-04", element="Air",
      kicker="Wed · Waning crescent · Scorpio season",
      headline="Mercury is whispering in the Sun's ear today.",
      sky="The Moon in Virgo traded friendly glances with the Sun and Mercury overnight, and the Sun meets retrograde Mercury mid-morning",
      signs=[
       ("Gemini", "The Moon is in your home zone. Uranus is retrograde in your sign, moving backward: rethink one small thing about how you live.",
        "What would make my space feel more like me?"),
       ("Libra", "The Moon rests in your twelfth house, your quiet zone. Venus, retrograde in your sign, met Jupiter kindly overnight: dream softly.",
        "What wish have I been too shy to say out loud?"),
       ("Aquarius", "The Moon visits your house of deep bonds. Pluto is in your sign, and the Sun meets Mercury mid-morning: let one honest talk happen.",
        "Who do I trust enough to let all the way in?")],
      cta="Save this for a quiet evening."),
 dict(date="2026-11-05", element="Water",
      kicker="Thu · Waning crescent · Scorpio season",
      headline="The Moon swaps Virgo for Libra today. Pretty choice.",
      sky="The Moon moves from Virgo into Libra today, opposes Neptune and trines Pluto this afternoon, and trines Uranus this evening",
      signs=[
       ("Cancer", "The Moon enters Libra today and lights your home zone. She trines Pluto this afternoon, a friendly angle: refresh one corner.",
        "Which corner of my life is asking for tender care?"),
       ("Scorpio", "Mercury is retrograde in your sign, and the Moon slips into your quiet twelfth house today. Rest is productive too, darling.",
        "What am I ready to quietly let go of?"),
       ("Pisces", "The Moon enters your house of deep bonds today and faces Neptune, your ruling planet, this afternoon. Let feelings be clear.",
        "Where would gentle, clear boundaries help me most?")],
      cta="Send this to your Water friend."),
 dict(date="2026-11-06", element="Fire",
      kicker="Friday · Waning crescent · Scorpio season",
      headline="The Moon and Saturn had a stare-down overnight.",
      sky="The Moon in Libra opposed retrograde Saturn overnight, while Mars and Jupiter keep company in Leo",
      signs=[
       ("Aries", "The Moon is in Libra, your opposite sign, lighting your partnership house. She faced Saturn, retrograde in your sign, overnight.",
        "What do I need from the people closest to me?"),
       ("Leo", "The Moon chats through your house of words and short trips. Mars and Jupiter are in your sign: speak with warmth and heart.",
        "Which kind words have I been saving for later?"),
       ("Sagittarius", "The Moon visits your friendship house, home of your circle and your hopes. Make plans with someone who makes you laugh.",
        "Which hope for the future feels brightest now?")],
      cta="Send this to your Fire friend."),
 dict(date="2026-11-07", element="Earth",
      kicker="Sat · Waning crescent · Scorpio season",
      headline="The Moon and Venus shared a secret overnight.",
      sky="The Moon in Libra met retrograde Venus overnight, makes a friendly sextile to Jupiter today and slips into Scorpio this evening",
      signs=[
       ("Taurus", "The Moon tidies your house of daily routines and met Venus, your ruling planet, overnight. Make your to-do list a little prettier.",
        "Which daily ritual could feel more like a treat?"),
       ("Virgo", "The Moon is in your house of values and self-worth, and winks at Jupiter today. Treat your talents like the treasure they are.",
        "Which quality of mine deserves more credit?"),
       ("Capricorn", "The Moon lights your career house until she moves into Scorpio this evening. Polish one goal, then log off and enjoy.",
        "Which goal would I love to be known for?")],
      cta="Send this to your Earth friend."),
 dict(date="2026-11-08", element="Air",
      kicker="Sunday · Waning crescent · Scorpio season",
      headline="The Moon has a quiet word with Mercury today.",
      sky="The Moon in Scorpio, just 1% lit, meets retrograde Mercury today",
      signs=[
       ("Gemini", "The Moon tidies your house of daily routines and meets Mercury, your ruling planet, today. Rest and review before you restart.",
        "What would make my mornings feel gentler?"),
       ("Libra", "The Moon sits in your house of values and self-worth. With Venus retrograde in your sign, notice what makes you feel rich inside.",
        "What makes me feel valued without anyone saying it?"),
       ("Aquarius", "The Moon lights your career house and meets Mercury today. Pluto is in your sign: let your work show who you are becoming.",
        "Where would I love my work to take me next?")],
      cta="Send this to your Air friend."),
 dict(date="2026-11-09", element="Water",
      kicker="Monday · New Moon · Scorpio season",
      headline="New Moon in Scorpio overnight. Make a wish, darling.",
      sky="The New Moon arrived in Scorpio overnight, and the Moon squares Mars this afternoon and Jupiter this evening",
      signs=[
       ("Cancer", "The New Moon arrived overnight in your house of joy and romance. Plant one playful intention and give it room to grow.",
        "What joy am I ready to invite in?"),
       ("Scorpio", "The New Moon arrived in your sign overnight, beside retrograde Mercury. Write a wish about the person you're becoming.",
        "Who am I ready to become, starting today?"),
       ("Pisces", "The New Moon arrived overnight in your house of travel and big ideas. Her tense square to Jupiter this evening says: dream, then plan.",
        "What adventure would I love to say yes to?")],
      cta="Save this for your New Moon wishes."),
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
