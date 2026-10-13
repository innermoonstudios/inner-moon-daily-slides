"""Publish a carousel to Instagram via the Instagram API with Instagram Login.

Env:
  IG_ACCESS_TOKEN   long-lived token (GitHub secret, never printed)
  IMAGE_BASE_URL    public URL folder holding slide-1.jpg ... slide-N.jpg
  SLIDE_COUNT       number of slides (2-10), default 5
  CAPTION           post caption
  PUBLISH           "true" to publish; anything else stops after containers are ready (dry run)
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


def wait_ready(container_id, label):
    for _ in range(30):
        status = call("GET", container_id, fields="status_code").get("status_code")
        if status == "FINISHED":
            return
        if status in ("ERROR", "EXPIRED"):
            sys.exit(f"{label} container {container_id} failed with status {status}")
        time.sleep(5)
    sys.exit(f"{label} container {container_id} not ready after 150s")


def main():
    base = os.environ["IMAGE_BASE_URL"].rstrip("/")
    n = int(os.environ.get("SLIDE_COUNT", "5"))
    caption = os.environ.get("CAPTION", "")
    publish = os.environ.get("PUBLISH", "false").lower() == "true"
    if not 2 <= n <= 10:
        sys.exit("Carousels need 2-10 slides")

    me = call("GET", "me", fields="user_id,username")
    ig_id = me["user_id"]
    print(f"Connected account: @{me['username']}")

    # 1. One container per slide
    children = []
    for i in range(1, n + 1):
        url = f"{base}/slide-{i}.jpg"
        c = call("POST", f"{ig_id}/media", image_url=url, is_carousel_item="true")
        print(f"Slide {i} container: {c['id']}")
        children.append(c["id"])
    for cid in children:
        wait_ready(cid, "Slide")

    # 2. Carousel container
    carousel = call("POST", f"{ig_id}/media", media_type="CAROUSEL",
                    children=",".join(children), caption=caption)
    wait_ready(carousel["id"], "Carousel")
    print(f"Carousel container ready: {carousel['id']}")

    if not publish:
        print("Dry run: containers are ready, nothing published.")
        return

    # 3. Publish
    post = call("POST", f"{ig_id}/media_publish", creation_id=carousel["id"])
    link = call("GET", post["id"], fields="permalink").get("permalink", "")
    print(f"Published post {post['id']} {link}")
    gh_out = os.environ.get("GITHUB_OUTPUT")
    if gh_out:
        with open(gh_out, "a") as f:
            f.write(f"permalink={link or post['id']}\n")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a") as f:
            f.write(f"Published: {link or post['id']}\n")


if __name__ == "__main__":
    main()
