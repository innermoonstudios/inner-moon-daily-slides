"""Week of 2026-10-13: content written from sky/days/*.json (houses = Sun-sign whole-sign, plan D3).
Run once to (re)write queue/<date>.json. Each day: status "approved" posts at 8am ET; set "hold" to skip.
"""
import json, pathlib

HERE = pathlib.Path(__file__).parent
TAGS = {"Fire": ["aries", "leo", "sagittarius"], "Earth": ["taurus", "virgo", "capricorn"],
        "Air": ["gemini", "libra", "aquarius"], "Water": ["cancer", "scorpio", "pisces"]}

DAYS = [
 dict(date="2026-10-13", element="Fire",
      kicker="Tuesday · Waxing crescent · Libra season",
      headline="Venus is retrograde and the Moon is keeping secrets.",
      sky="The Moon is in Scorpio with Venus, who is retrograde there, and she squares Jupiter in Leo",
      signs=[
       ("Aries", "The Moon slips into your house of intimacy. Let someone see the soft part you usually guard; trust grows slowly and surely.",
        "Who have I been ready to trust a little more?"),
       ("Leo", "The Moon settles into your home zone while squaring Jupiter in your sign. Big plans can wait. Tonight, nest.",
        "What would make my home feel like a hug tonight?"),
       ("Sagittarius", "The Moon drifts through your quiet, dreamy corner before arriving in your sign tonight. Rest now; the next idea will find you.",
        "What am I ready to whisper to myself before I say it out loud?")],
      cta="Send this to your Fire friend."),
 dict(date="2026-10-14", element="Earth",
      kicker="Wednesday · Waxing crescent · Libra season",
      headline="The Moon is in Sagittarius and she wants an adventure.",
      sky="The Moon is in Sagittarius, trining Mars and Saturn and opposing Uranus",
      signs=[
       ("Taurus", "The Moon lights up your house of deep bonds. Venus, your ruler, is retrograde, so revisit an old promise before making a new one.",
        "Which promise to myself deserves a second look?"),
       ("Virgo", "The Moon warms your home zone and teases you to loosen the schedule. A long dinner at home counts as productive.",
        "Where can I let comfort win over perfect?"),
       ("Capricorn", "The Moon wanders through your most private house. Step back, dream a little, and let your next goal reveal itself.",
        "What do I want when no one is watching?")],
      cta="Send this to your Earth friend."),
 dict(date="2026-10-15", element="Air",
      kicker="Thursday · Waxing crescent · Libra season",
      headline="The Sun and Jupiter are flirting, and everyone's invited.",
      sky="The Sun in Libra sextiles Jupiter in Leo, and the Moon in Sagittarius trines Jupiter too",
      signs=[
       ("Gemini", "The Moon sits in your partnership house, opposite your sign. Let someone else lead the conversation; you'll learn something lovely.",
        "Who do I want to know better this season?"),
       ("Libra", "It's your season, and the Sun is high-fiving lucky Jupiter. The Moon in your house of words says: send the message.",
        "What would I say if I trusted it would land well?"),
       ("Aquarius", "The Moon lights your friendship house while Jupiter beams from your opposite sign. Say yes to the group plan.",
        "Which friend makes me feel most like myself?")],
      cta="Send this to your Air friend."),
 dict(date="2026-10-16", element="Water",
      kicker="Friday · Waxing crescent · Libra season",
      headline="Pluto stops sulking and turns direct today.",
      sky="Pluto stations direct in Aquarius, Mars trines Saturn, and the Moon moves into Capricorn this morning",
      signs=[
       ("Cancer", "The Moon, your ruler, moves into your partnership house. Ask for what you need in love and friendship, plainly and sweetly.",
        "What do I need from the people closest to me?"),
       ("Scorpio", "Pluto, your ruler, turns direct while Venus is retrograde in your sign. Say the honest thing gently; this time it sticks.",
        "What truth am I ready to say kindly?"),
       ("Pisces", "The Moon settles into your friendship house. A practical friend has the grounding advice you've been craving.",
        "Who helps me turn a dream into a plan?")],
      cta="Send this to your Water friend."),
 dict(date="2026-10-17", element="Fire",
      kicker="Saturday · Waxing crescent · Libra season",
      headline="The Moon puts on her blazer: Capricorn mode.",
      sky="The Moon is in Capricorn and squares Saturn in Aries",
      signs=[
       ("Aries", "The Moon climbs to your career house and squares Saturn in your sign. Slow and steady wins: pick one ambition and tend it.",
        "Which goal deserves my patience this week?"),
       ("Leo", "The Moon tidies your house of daily rhythms. Mars in your sign wants action, so pour it into one small, satisfying routine.",
        "What tiny habit would make tomorrow easier?"),
       ("Sagittarius", "The Moon moves into your house of values. Treat yourself kindly and take stock of everything you already have.",
        "What feels truly abundant in my life right now?")],
      cta="Save this for your weekend reset."),
 dict(date="2026-10-18", element="Earth",
      kicker="Sunday · First Quarter Moon · Libra season",
      headline="Half lit and fully decided: the First Quarter Moon.",
      sky="The Moon reaches First Quarter in Capricorn, squaring the Sun in Libra",
      signs=[
       ("Taurus", "The First Quarter Moon lights your house of big ideas and journeys. Book the class, plan the trip, or simply wander.",
        "Where is my curiosity pulling me?"),
       ("Virgo", "The Moon hits First Quarter in your house of joy and creativity. Make something just for fun. No grading allowed.",
        "When did I last play without a goal?"),
       ("Capricorn", "The First Quarter Moon is in your sign. A gentle push: choose, commit, and let the rest of the plan catch up.",
        "What am I ready to decide today?")],
      cta="Send this to your Earth friend."),
 dict(date="2026-10-19", element="Air",
      kicker="Monday · First Quarter Moon · Libra season",
      headline="The Moon is in Aquarius and feeling delightfully odd.",
      sky="The Moon is in Aquarius, meeting Pluto and trining Uranus in Gemini",
      signs=[
       ("Gemini", "The Moon trines Uranus in your sign from your house of adventure. An unusual idea is worth chasing today.",
        "What new idea keeps tapping me on the shoulder?"),
       ("Libra", "The Moon dances through your house of romance and play. Venus, your ruler, is retrograde, so an old flame of an idea may return.",
        "What used to light me up that I could revisit?"),
       ("Aquarius", "The Moon meets Pluto in your sign. You're shedding an old skin; let the new you stay a little mysterious.",
        "What am I outgrowing, sweetly and surely?")],
      cta="Send this to your Air friend."),
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
