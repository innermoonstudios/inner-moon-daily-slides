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
- **Reel post** (`reel-post.yml`): 18:00 New York time, on days with an approved queue file (planned Mon/Wed/Fri). Posts `reels/queue/<date>.json` (or any MP4 under `reels/`): copies the
  MP4 to Pages, creates an Instagram REELS container, waits for `FINISHED`, publishes only when `publish` is ticked,
  then marks the queue file published. See *Reels* below.

## Scripts
- `scripts/make_test_slides.py`: placeholder 1080x1350 JPEG slides.
- `scripts/publish_carousel.py`: Instagram API flow (slide containers, carousel container, publish).
- `scripts/publish_reel.py`: Instagram API flow for Reels (REELS container with `video_url`, poll status, publish).
- `scripts/reel_today.py`: picks the Reel (queue file or `video` input), checks its status, stages the MP4 for Pages.
- `scripts/mark_published.py`: marks a queue file published; optional third argument `reels/queue`.

## Reels
- **Cadence**: 2-3 a week (planned Mon/Wed/Fri, 18:00 New York), next to the daily 8:00 carousel. Carousels stay daily.
  The workflow checks daily at 18:00 and posts only when `reels/queue/<today>.json` is `approved`.
- **Videos**: `reels/<sign>/<sign>-<NN>-<design>-reel.mp4`, made with the product-reels skill (Higgsfield UGC via
  higgsfield-generate / Marketing Studio). Instagram accepts MP4, H.264 + AAC, 9:16 (1080x1920 ideal, 720x1280 works),
  3 s to 15 min, under 300 MB.
- **Queue**: `reels/queue/<date>.json` with `date`, `status`, `listing`, `video`, `share_to_feed`, `caption`.
  Status: `draft` (written, not approved) → `approved` (will post) → `published` (bot adds `permalink`). `hold` skips a day.
  Captions follow `brand/voice.md`; they say the model is AI-generated.
- **Run**: Actions > *Reel post* > Run workflow. Blank `video` = the queue file for `date`. Leave `publish` unticked for a
  dry run (container created and checked, nothing posted; it expires after 24 h). For a one-off, set `video` to any MP4
  under `reels/` with a `caption` (or a `.txt` with the same name next to it).
- The video is served at `https://innermoonstudios.github.io/inner-moon-daily-slides/runs/<run id>/reel.mp4`
  until the next Pages deploy replaces the site (Instagram copies the file when the container is created).
- Videos stay in git history even after deletion (~6 MB each). Fine for dozens; move to release assets if it grows to hundreds.
