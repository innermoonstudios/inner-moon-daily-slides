"""Mark queue/<date>.json as published with its permalink (so a second run never re-posts)."""
import json, pathlib, sys
date, link = sys.argv[1], sys.argv[2]
p = pathlib.Path(__file__).resolve().parent.parent / "queue" / f"{date}.json"
q = json.loads(p.read_text())
q["status"], q["permalink"] = "published", link
p.write_text(json.dumps(q, indent=1, ensure_ascii=False) + "\n")
