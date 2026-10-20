"""Mark queue/<date>.json as published with its permalink (so a second run never re-posts).

Optional third argument: the queue folder, e.g. reels/queue (default queue)."""
import json, pathlib, sys
date, link = sys.argv[1], sys.argv[2]
folder = sys.argv[3] if len(sys.argv) > 3 else "queue"
p = pathlib.Path(__file__).resolve().parent.parent / folder / f"{date}.json"
q = json.loads(p.read_text())
q["status"], q["permalink"] = "published", link
p.write_text(json.dumps(q, indent=1, ensure_ascii=False) + "\n")
