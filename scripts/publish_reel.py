"""Publish a Reel to Instagram via the Instagram API with Instagram Login.

Env:
  IG_ACCESS_TOKEN   long-lived token (GitHub secret, never printed)
  VIDEO_URL         public URL of the MP4 (H.264 + AAC, 9:16, 3 s to 15 min)
  CAPTION           post caption
  SHARE_TO_FEED     "true" (default) to also show the Reel in the profile grid
  PUBLISH           "true" to publish; anything else stops once the container is FINISHED (dry run)
  GRAPH_VERSION     API version, default v23.0
"""
import os
import sys
import time

import requests

TOKEN = os.environ["IG_ACCESS_TOKEN"]
VERSION = os.environ.get("GRAPH_VERSION", "v23.0")
API = f"https://graph.instagram.com/{VERSION}"


def call(method, path, **params):
    params["access_token"] = TOKEN
    r = requests.request(method, f"{API}/{path}", params=params, timeout=60)
    try:
        body = r.json()
    except ValueError:
        body = {"raw": r.text[:500]}
    if not r.ok or "error" in body:
        # Print only the API's error body, never the request URL (it contains the token).
        sys.exit(f"API error on {method} /{path}: {body.get('error', body)}")
    return body


def wait_ready(container_id):
    # Instagram downloads and transcodes the video; short Reels take ~30 s, long ones a few minutes.
    for _ in range(60):
        info = call("GET", container_id, fields="status_code,status")
        status = info.get("status_code")
        if status == "FINISHED":
            return
        if status in ("ERROR", "EXPIRED"):
            sys.exit(f"Reel container {container_id} failed with {status}: {info.get('status', '')}")
        print(f"Container {status}, waiting...")
        time.sleep(10)
    sys.exit(f"Reel container {container_id} not ready after 10 min")


def main():
    video_url = os.environ["VIDEO_URL"]
    caption = os.environ.get("CAPTION", "")
    share = os.environ.get("SHARE_TO_FEED", "true").lower() == "true"
    publish = os.environ.get("PUBLISH", "false").lower() == "true"

    me = call("GET", "me", fields="user_id,username")
    ig_id = me["user_id"]
    print(f"Connected account: @{me['username']}")

    # 1. Reel container
    reel = call("POST", f"{ig_id}/media", media_type="REELS", video_url=video_url,
                caption=caption, share_to_feed=str(share).lower())
    print(f"Reel container: {reel['id']}")
    wait_ready(reel["id"])
    print(f"Reel container ready: {reel['id']}")

    if not publish:
        print("Dry run: container is ready, nothing published. It expires unused after 24 h.")
        return

    # 2. Publish
    post = call("POST", f"{ig_id}/media_publish", creation_id=reel["id"])
    link = call("GET", post["id"], fields="permalink").get("permalink", "")
    print(f"Published Reel {post['id']} {link}")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a") as f:
            f.write(f"Published Reel: {link or post['id']}\n")
    gh_out = os.environ.get("GITHUB_OUTPUT")
    if gh_out:
        with open(gh_out, "a") as f:
            f.write(f"permalink={link or post['id']}\n")


if __name__ == "__main__":
    main()
