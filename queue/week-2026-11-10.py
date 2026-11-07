"""Week of 2026-11-10: content written from sky/days/*.json (houses = Sun-sign whole-sign, plan D3).
Run once to (re)write queue/<date>.json. Each day: status "approved" posts at 8am ET; set "hold" to skip.
Timing words are relative to the 8:00 am New York post.
"""
import json, pathlib

HERE = pathlib.Path(__file__).parent
TAGS = {"Fire": ["aries", "leo", "sagittarius"], "Earth": ["taurus", "virgo", "capricorn"],
        "Air": ["gemini", "libra", "aquarius"], "Water": ["cancer", "scorpio", "pisces"]}

DAYS = [
 dict(date="2026-11-10", element="Fire",
      kicker="Tuesday · Waxing crescent · Scorpio season",
      headline="The Moon ran off to Sagittarius overnight.",
      sky="The Moon moved into Sagittarius overnight, faces Uranus around midday and makes a friendly trine to Saturn tonight",
      signs=[
       ("Aries", "The Moon lights your house of travel and big ideas. Tonight she makes a friendly trine to Saturn, retrograde in your sign.",
        "Which big idea is ready for its first small step?"),
       ("Leo", "The Moon lights your house of joy and romance. Venus sent Mars, in your sign, a friendly sextile overnight: flirt with an idea.",
        "What would I make just because it delights me?"),
       ("Sagittarius", "The Moon arrived in your sign overnight, so the spotlight is yours. She faces Uranus around midday: leave room for a surprise.",
        "Where am I ready to be a beginner again?")],
      cta="Send this to your Fire friend."),
 dict(date="2026-11-11", element="Earth",
      kicker="Wed · Waxing crescent · Scorpio season",
      headline="The Moon is wandering through Sagittarius all day.",
      sky="The Moon spends the whole day in Sagittarius, with no major aspects to hurry her, while Mercury and Venus are retrograde",
      signs=[
       ("Taurus", "The Moon is in your house of deep bonds. Venus, your ruling planet, is retrograde, moving backward: revisit a promise gently.",
        "Which promise to myself deserves a second look?"),
       ("Virgo", "The Moon settles into your home zone. Mercury, your ruling planet, is retrograde, moving backward: tidy one old corner.",
        "What does home need from me right now?"),
       ("Capricorn", "The Moon drifts through your twelfth house, your quiet zone. Saturn, your ruling planet, is retrograde: slow down and listen in.",
        "What do I hear when I finally sit still?")],
      cta="Save this for a slow Wednesday."),
 dict(date="2026-11-12", element="Air",
      kicker="Thu · Waxing crescent · Scorpio season",
      headline="The Moon flirted with three planets before breakfast.",
      sky="Overnight the Moon in Sagittarius traded friendly glances with Venus, Mars and Jupiter. She moves into Capricorn this afternoon",
      signs=[
       ("Gemini", "The Moon lights your partnership house until she moves into Capricorn this afternoon. Say something sweet to your favorite person.",
        "Who makes me feel most like myself?"),
       ("Libra", "The Moon is in your house of words and sent Venus, your ruling planet, a friendly sextile overnight. Send that kind text.",
        "Which conversation would make my day lighter?"),
       ("Aquarius", "The Moon visits your friendship house. She made friendly trines to Mars and Jupiter overnight: say yes to a group plan.",
        "Which friend makes my wildest ideas feel possible?")],
      cta="Send this to your Air friend."),
 dict(date="2026-11-13", element="Water",
      kicker="Friday · Waxing crescent · Scorpio season",
      headline="Mercury and Venus stop walking backward today.",
      sky="Mercury turns direct (moving forward again) late this morning and Venus turns direct this evening, while the Moon is in Capricorn",
      signs=[
       ("Cancer", "The Moon lights your partnership house, and Venus turns direct this evening, moving forward again. Let love feel easier.",
        "What would make love feel lighter this season?"),
       ("Scorpio", "Mercury turns direct in your sign late this morning, moving forward again. The Moon is in your house of words: speak up kindly.",
        "What have I finally figured out how to say?"),
       ("Pisces", "The Moon visits your friendship house. Mercury turns direct late this morning: reply to the message you've been mulling over.",
        "Which friend deserves my reply today?")],
      cta="Save this for your next retrograde."),
 dict(date="2026-11-14", element="Fire",
      kicker="Sat · Waxing crescent · Scorpio season",
      headline="The Sun sends the Moon a friendly wave this afternoon.",
      sky="The Moon in Capricorn gets a friendly sextile from the Sun and a tense square to Venus, both this afternoon",
      signs=[
       ("Aries", "The Moon lights your career house, and the Sun sends her a friendly sextile this afternoon. Show one goal a little love.",
        "Which goal would make future me proud?"),
       ("Leo", "The Moon tidies your house of daily routines. Mars and Jupiter are both in your sign: give your energy to one good habit.",
        "Which small habit makes me feel strongest?"),
       ("Sagittarius", "The Moon sits in your house of values and self-worth. Her tense square to Venus this afternoon asks what you truly treasure.",
        "What do I value more than I admit?")],
      cta="Send this to your Fire friend."),
 dict(date="2026-11-15", element="Earth",
      kicker="Sunday · Waxing crescent · Scorpio season",
      headline="The Moon cozies up to Pluto late this morning.",
      sky="The Moon moved into Aquarius overnight, meets Pluto late this morning, trines Uranus around midday and sextiles Saturn tonight",
      signs=[
       ("Taurus", "The Moon moved into Aquarius overnight and lights your career house. She trines Uranus today, a friendly angle: try a fresh approach.",
        "What fresh approach could make my work feel new?"),
       ("Virgo", "The Moon tidies your house of daily routines. Her tense square to Mercury, your ruling planet, this afternoon says: one task at a time.",
        "Which one task deserves my full attention?"),
       ("Capricorn", "The Moon left your sign overnight for your house of values. Tonight she sends Saturn, your ruling planet, a friendly sextile.",
        "Which quiet win am I proud of this week?")],
      cta="Send this to your Earth friend."),
 dict(date="2026-11-16", element="Air",
      kicker="Monday · Waxing crescent · Scorpio season",
      headline="Mars and Jupiter got very close in Leo overnight.",
      sky="Mars and Jupiter met in Leo overnight, and the Moon spends the day in Aquarius",
      signs=[
       ("Gemini", "The Moon visits your house of travel and big ideas. Uranus is retrograde in your sign, moving backward: revisit an old dream.",
        "Which old dream still makes my heart race?"),
       ("Libra", "The Moon lights your house of joy and romance, and Venus, your ruling planet, is moving forward in your sign. Play a little.",
        "What lights me up that I've been too busy for?"),
       ("Aquarius", "The Moon spends the day in your sign, beside Pluto. Mars met Jupiter in Leo, your opposite sign, overnight: team up with someone bold.",
        "Who brings out the boldest version of me?")],
      cta="Save this for your next Monday reset."),
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
