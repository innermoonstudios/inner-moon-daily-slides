"""Week of 2026-12-01: content written from sky/days/*.json (houses = Sun-sign whole-sign, plan D3).
Run once to (re)write queue/<date>.json. Each day: status "approved" posts at 8am ET; set "hold" to skip.
Timing words are relative to the 8:00 am New York post.
"""
import json, pathlib

HERE = pathlib.Path(__file__).parent
TAGS = {"Fire": ["aries", "leo", "sagittarius"], "Earth": ["taurus", "virgo", "capricorn"],
        "Air": ["gemini", "libra", "aquarius"], "Water": ["cancer", "scorpio", "pisces"]}

DAYS = [
 dict(date="2026-12-01", element="Earth",
      kicker="Tue · Last Quarter · Sagittarius season",
      headline="The Last Quarter Moon tidied up overnight.",
      sky="The Moon reached her Last Quarter in Virgo overnight, a half-lit pause to clear space. She stays in Virgo all day, alongside Mars",
      signs=[
       ("Taurus", "The Moon is in Virgo, lighting your house of joy. She reached her Last Quarter overnight: drop one chore and play.",
        "What would I make just for the fun of it?"),
       ("Virgo", "The Moon is in your sign, and so is Mars. She reached her Last Quarter overnight: clear one thing off your plate.",
        "What am I ready to set down with love?"),
       ("Capricorn", "The Moon lights your house of travel and big ideas. Saturn, your ruler, is retrograde: revisit an old dream gently.",
        "Where would I love to wander next?")],
      cta="Save this for your next Last Quarter."),
 dict(date="2026-12-02", element="Air",
      kicker="Wed · Waning crescent · Sagittarius season",
      headline="The Moon sashays into Libra this afternoon.",
      sky="The Moon starts the day in Virgo and moves into Libra this afternoon. Tonight she sends Uranus and Pluto friendly trines",
      signs=[
       ("Gemini", "The Moon starts the day in your home zone. Tonight she sends Uranus, in your sign, a friendly trine: try a new idea.",
        "What fresh idea wants room in my life?"),
       ("Libra", "The Moon rests in your quiet zone, then moves into your sign this afternoon, where Venus, your ruler, waits. Glow.",
        "What would I love to be known for?"),
       ("Aquarius", "The Moon visits your house of deep bonds. Tonight she sends Pluto, in your sign, a friendly trine: open up a little.",
        "Who do I feel safe letting in?")],
      cta="Send this to your Air friend."),
 dict(date="2026-12-03", element="Water",
      kicker="Thu · Waning crescent · Sagittarius season",
      headline="The Sun and Moon swap smiles at lunchtime.",
      sky="The Moon is in Libra all day. She faced Saturn early this morning, and the Sun sends her a friendly sextile around lunchtime",
      signs=[
       ("Cancer", "The Moon, your ruler, is in your home zone. Around lunchtime the Sun sends her a friendly sextile: nest a little.",
        "Where at home do I want more light?"),
       ("Scorpio", "The Moon drifts through your quiet zone, and Mercury is in your sign. Write down what your intuition whispers.",
        "What is my intuition trying to tell me?"),
       ("Pisces", "The Moon lights your house of deep bonds. Neptune, your modern ruler, is retrograde, so it seems to drift backward.",
        "Who deserves a more honest heart-to-heart?")],
      cta="Send this to your Water friend."),
 dict(date="2026-12-04", element="Fire",
      kicker="Fri · Waning crescent · Sagittarius season",
      headline="Venus slipped into Scorpio overnight. Mysterious.",
      sky="Venus moved into Scorpio overnight. The Moon is in Libra, Mars squares Uranus this afternoon, and the Moon sends Jupiter a friendly sextile this evening",
      signs=[
       ("Aries", "The Moon is in your partnership house. This afternoon Mars, your ruler, squares Uranus, a tense angle: stay flexible.",
        "Where could I let a plan bend a little?"),
       ("Leo", "The Moon is in your house of words. This evening she sends Jupiter, in your sign, a friendly sextile: say the big thing.",
        "What compliment have I been holding back?"),
       ("Sagittarius", "The Sun is in your sign, and the Moon lights your friendship house. Plan something fun with the people who get you.",
        "Who makes me laugh the hardest?")],
      cta="Send this to your Fire friend."),
 dict(date="2026-12-05", element="Earth",
      kicker="Sat · Waning crescent · Sagittarius season",
      headline="The Moon and Venus cuddled up overnight.",
      sky="The Moon is in Scorpio all day. She met Venus overnight, then sent Mars a friendly sextile early this morning",
      signs=[
       ("Taurus", "The Moon is in your partnership house, across from your sign. Overnight she met Venus, your ruler: be sweet to your person.",
        "Who do I want to spoil a little this weekend?"),
       ("Virgo", "The Moon lights your house of words. Early this morning she sent Mars, in your sign, a friendly sextile: speak up warmly.",
        "What do I want to ask for, plainly and kindly?"),
       ("Capricorn", "The Moon visits your friendship house. Saturn, your ruler, is retrograde, so it seems to drift backward: call an old friend.",
        "Who from my past would love to hear from me?")],
      cta="Save this for a slow Saturday."),
 dict(date="2026-12-06", element="Air",
      kicker="Sun · Waning crescent · Sagittarius season",
      headline="Mercury hopped into Sagittarius overnight.",
      sky="Mercury moved into Sagittarius overnight. The Moon is a slim waning crescent in Scorpio all day, lovely for rest",
      signs=[
       ("Gemini", "Mercury, your ruler, moved into Sagittarius overnight. The Moon tends your house of routines: reset one small habit.",
        "What small habit would make my week sweeter?"),
       ("Libra", "The Moon lights your house of values, and Venus, your ruler, is in Scorpio. Spend Sunday on what feels truly yours.",
        "What feels most precious to me right now?"),
       ("Aquarius", "The Moon is in your career house, and Pluto is in your sign. Dream about the week ahead, then let Sunday be Sunday.",
        "Where do I want my work to take me?")],
      cta="Send this to your Air friend."),
 dict(date="2026-12-07", element="Water",
      kicker="Mon · Waning crescent · Sagittarius season",
      headline="The Moon trades Scorpio for Sagittarius today.",
      sky="The Moon moves from Scorpio into Sagittarius mid-morning and meets Mercury this afternoon. Early this morning Mercury sent Neptune a friendly trine",
      signs=[
       ("Cancer", "The Moon, your ruler, moves into your house of routines mid-morning. Give your Monday a gentle, doable shape.",
        "What would make this week feel manageable?"),
       ("Scorpio", "The Moon leaves your sign mid-morning for your house of values. Venus is in your sign: treat yourself like a treasure.",
        "What do I value most about myself?"),
       ("Pisces", "The Moon lights your career house. Early this afternoon she trines Neptune, your modern ruler, a friendly angle: dream big.",
        "Where would I go if I trusted my dreams?")],
      cta="Send this to your Water friend."),
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
