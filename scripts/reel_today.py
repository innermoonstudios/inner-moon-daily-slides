"""Decide whether a Reel should go out, and stage its video for Pages if so.

Writes to $GITHUB_OUTPUT: post=true|false, date, caption, share_to_feed, queued=true|false.
Copies the MP4 to argv[1]/reel.mp4.

Two modes:
- Manual (VIDEO set): post that MP4 under reels/. Caption = CAPTION, else the .txt next to it.
- Queue (default): post reels/queue/<date>.json, only at/after 18:00 America/New_York on scheduled
  runs, only if it has status "approved" and hasn't been published yet.
"""
import datetime as dt, json, os, pathlib, shutil, sys
from zoneinfo import ZoneInfo

ROOT = pathlib.Path(__file__).resolve().parent.parent
REELS = ROOT / "reels"
now = dt.datetime.now(ZoneInfo("America/New_York"))
date = os.environ.get("POST_DATE") or now.date().isoformat()
out_dir = pathlib.Path(sys.argv[1])

def emit(**kv):
    with open(os.environ.get("GITHUB_OUTPUT", os.devnull), "a") as f:
        for k, v in kv.items():
            f.write(f"{k}={v}\n")

def skip(reason):
    print("SKIP:", reason)
    emit(post="false", date=date)
    sys.exit(0)

def resolve(rel):
    p = (ROOT / rel).resolve()
    if p.suffix != ".mp4" or REELS not in p.parents or not p.is_file():
        sys.exit(f"Video must be an existing .mp4 under reels/: {rel}")
    return p

video_input = os.environ.get("VIDEO", "").strip()
if video_input:
    video = resolve(video_input)
    caption = os.environ.get("CAPTION", "")
    sidecar = video.with_suffix(".txt")
    if not caption and sidecar.exists():
        caption = sidecar.read_text().strip()
    share, queued = os.environ.get("SHARE_TO_FEED", "true"), "false"
else:
    if os.environ.get("GITHUB_EVENT_NAME") == "schedule" and now.hour < 18:
        skip(f"it's {now:%H:%M} in New York; Reels post from 18:00")
    qf = REELS / "queue" / f"{date}.json"
    if not qf.exists():
        skip(f"no Reel queued for {date}")
    q = json.loads(qf.read_text())
    if q.get("status") == "published":
        skip(f"{date} Reel already published: {q.get('permalink', '')}")
    if q.get("status") != "approved":
        skip(f"{date} Reel status is '{q.get('status')}', not 'approved'")
    video, caption = resolve(q["video"]), q["caption"]
    share, queued = str(q.get("share_to_feed", True)).lower(), "true"

out_dir.mkdir(parents=True, exist_ok=True)
shutil.copy(video, out_dir / "reel.mp4")
emit(post="true", date=date, share_to_feed=share, queued=queued)
with open(os.environ.get("GITHUB_OUTPUT", os.devnull), "a") as f:
    f.write("caption<<__CAPTION__\n" + caption + "\n__CAPTION__\n")
print(f"Staged {video.relative_to(ROOT)} ({video.stat().st_size // 1024} KB) for {date}")
