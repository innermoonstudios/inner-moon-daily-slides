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

## Workflows
- **Test carousel post** (`.github/workflows/test-post.yml`): renders 5 placeholder slides, deploys them to Pages,
  creates the Instagram carousel, and publishes only when `publish` is ticked. Run it from the Actions tab.

## Scripts
- `scripts/make_test_slides.py`: placeholder 1080x1350 JPEG slides.
- `scripts/publish_carousel.py`: Instagram API flow (slide containers, carousel container, publish).
