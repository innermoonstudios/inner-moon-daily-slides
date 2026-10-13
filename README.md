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

## Scripts
- `scripts/make_test_slides.py`: placeholder 1080x1350 JPEG slides.
- `scripts/publish_carousel.py`: Instagram API flow (slide containers, carousel container, publish).
