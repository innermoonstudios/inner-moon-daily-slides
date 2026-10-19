# Inner Moon Daily Slides

Automated daily Instagram carousels for [@innermoonstore](https://www.instagram.com/innermoonstore/).

## How it fits together
- **Code** lives here. **Slide images** are hosted on GitHub Pages (public JPEG URLs, which Instagram's API requires).
- **GitHub Actions** runs the jobs on GitHub's servers.
- **Secrets** (Settings > Secrets and variables > Actions):
  - `IG_ACCESS_TOKEN`: Instagram long-lived token for @innermoonstore, from Meta app "Inner Moon Daily".
    Generated 2026-10-11, expires ~2026-12-10 unless refreshed (auto-refresh workflow planned).
  - `GH_TOKEN`: fine-grained GitHub token, used by the planned refresh workflow to rewrite `IG_ACCESS_TOKEN`
    (needs "Secrets: Read and write" on this repo).
- **Pages** source is set to *GitHub Actions* (Settings > Pages). Images are served at
  `https://innermoonstudios.github.io/inner-moon-daily-slides/runs/<run id>/slide-N.jpg`.
- Never commit tokens or keys to this repo; it is public.

## Status
- 2026-10-12: pipeline proven end to end. Dry run (run 38201841810) and live test post (run 38202049186) both succeeded.
- Full plan and task statuses: Inner Moon Store project, `plans/instagram-daily-carousel-automation.md`.

## Daily content (since 2026-10-12)
- `sky/`: ephemeris code (from inner-moon-interior). `sky/days/<date>.json` is computed daily, 21 days ahead, by **Compute sky**.
  Each file covers one New York calendar day (midnight to midnight ET, `"tz"` field), so events land on the
  date US readers see; use `phase_label` for the kicker. Copy may only state what a sky file says (no durations,
  event order or future positions), with timing words relative to the 8:00 am ET post.
- `queue/<date>.json`: one post per day (rotating Fire → Earth → Air → Water). `"status": "approved"` posts at 8:00 New York time;
  set `"hold"` to skip a day. After posting, the bot sets `"published"` and the permalink. Weekly batches are written by a Claude
  scheduled task from the sky files and `brand/voice.md`.
- `brand/`: tokens.json (colours, type, sizes, character limits), voice.md, brand.md, fonts, moon mascot.
- `templates/`: hook/sign/CTA HTML + `render.py` (renders 1080x1350 JPEGs and fails on QA: limits, wrapping, safe zone).

## Workflows
- **Daily post** (`daily-post.yml`): 8:00 New York time. Renders today's queue file, deploys to Pages, publishes, marks published.
  Run by hand with a date (and publish unticked for a dry run).
- **Compute sky** (`sky.yml`): daily, writes the next 21 sky files.
- **Preview queue** (`preview.yml`): renders upcoming days on every queue change; slides are in the run's "preview" artifact.
- **Refresh Instagram token** (`refresh-token.yml`): Mondays, refreshes `IG_ACCESS_TOKEN` and saves it back with `GH_TOKEN`.
- **Test carousel post** (`.github/workflows/test-post.yml`): renders 5 placeholder slides, deploys them to Pages,
  creates the Instagram carousel, and publishes only when `publish` is ticked. Run it from the Actions tab.
- **Reel post** (`reel-post.yml`): manual. Copies one MP4 from `reels/` to Pages, creates an Instagram REELS container,
  waits until Instagram has processed it (status `FINISHED`), and publishes only when `publish` is ticked.
  See *Reels* below.

## Scripts
- `scripts/make_test_slides.py`: placeholder 1080x1350 JPEG slides.
- `scripts/publish_carousel.py`: Instagram API flow (slide containers, carousel container, publish).
- `scripts/publish_reel.py`: Instagram API flow for Reels (REELS container with `video_url`, poll status, publish).

## Reels
- **Files**: commit the MP4 under `reels/` (e.g. `reels/aries/aries-03-tarot-card-reel.mp4`). Optional caption file
  with the same name and `.txt` (`aries-03-tarot-card-reel.txt`); the run's `caption` box overrides it.
- **Specs** Instagram accepts: MP4, H.264 video + AAC audio, 9:16 (1080x1920 ideal, 720x1280 works), 3 s to 15 min, under 300 MB.
- **Run**: Actions > *Reel post* > Run workflow. Fill `video` with the repo path, leave `publish` unticked for a dry run.
  A dry run creates the container and waits for `FINISHED` (proves Instagram can fetch and process the video), then stops.
  Unused containers expire after 24 h. Tick `publish` to post; the permalink goes in the run summary.
- The video is served at `https://innermoonstudios.github.io/inner-moon-daily-slides/runs/<run id>/reel.mp4`
  until the next Pages deploy replaces the site (Instagram copies the file when the container is created).
- `reels/test/aries-03-tarot-card-reel.mp4` is the pipeline test (caption says it will be removed). Default `video` input.
- Videos stay in git history even after deletion (~6 MB each). Fine for dozens; move to release assets if it grows to hundreds.
