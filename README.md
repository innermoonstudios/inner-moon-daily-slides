# Inner Moon Daily Slides

Automated daily Instagram carousels for [@innermoonstore](https://www.instagram.com/innermoonstore/).

## How it fits together
- **Code** lives here. **Slide images** are hosted on GitHub Pages (public JPEG URLs, which Instagram's API requires).
- **GitHub Actions** runs the jobs on GitHub's servers.
- **Secrets** (Settings > Secrets and variables > Actions):
  - `IG_ACCESS_TOKEN`: Instagram long-lived token (60 days, auto-refresh planned).
- Never commit tokens or keys to this repo; it is public.

## Workflows
- **Test carousel post** (`.github/workflows/test-post.yml`): renders 5 placeholder slides, deploys them to Pages,
  creates the Instagram carousel, and publishes only when `publish` is ticked. Run it from the Actions tab.

## Scripts
- `scripts/make_test_slides.py`: placeholder 1080x1350 JPEG slides.
- `scripts/publish_carousel.py`: Instagram API flow (slide containers, carousel container, publish).
