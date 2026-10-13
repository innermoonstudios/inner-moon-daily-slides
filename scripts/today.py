"""Decide whether today's post should go out, and render it if so.

Writes to $GITHUB_OUTPUT: post=true|false, date, slides (count). Renders slides to argv[1].
Rules: post only at/after 8:00 America/New_York (scheduled runs), only if queue/<date>.json
exists, has status "approved", and hasn't been published yet.
"""
import datetime as dt, json, os, pathlib, subprocess, sys
from zoneinfo import ZoneInfo

ROOT = pathlib.Path(__file__).resolve().parent.parent
now = dt.datetime.now(ZoneInfo("America/New_York"))
date = os.environ.get("POST_DATE") or now.date().isoformat()
out_dir = sys.argv[1]

def emit(**kv):
    with open(os.environ.get("GITHUB_OUTPUT", os.devnull), "a") as f:
        for k, v in kv.items():
            f.write(f"{k}={v}\n")

def skip(reason):
    print("SKIP:", reason)
    emit(post="false", date=date)
    sys.exit(0)

if os.environ.get("GITHUB_EVENT_NAME") == "schedule" and now.hour < 8:
    skip(f"it's {now:%H:%M} in New York; posting starts at 8:00")
qf = ROOT / "queue" / f"{date}.json"
if not qf.exists():
    skip(f"no queue file for {date}")
q = json.loads(qf.read_text())
if q.get("status") == "published":
    skip(f"{date} already published: {q.get('permalink', '')}")
if q.get("status") != "approved":
    skip(f"{date} status is '{q.get('status')}', not 'approved'")

r = subprocess.run([sys.executable, str(ROOT / "templates" / "render.py"), str(qf), out_dir])
if r.returncode != 0:
    sys.exit("Render QA failed; not posting.")
caption = q["caption"]
emit(post="true", date=date, slides=len(q["slides"]))
with open(os.environ.get("GITHUB_OUTPUT", os.devnull), "a") as f:
    f.write("caption<<__CAPTION__\n" + caption + "\n__CAPTION__\n")
print(f"Rendered {len(q['slides'])} slides for {date} ({q.get('element')})")
