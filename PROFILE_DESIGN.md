# QiuuDev / Cyber Futuristic

Public profile identity for QiuuDev (BoringDev).

- Graphite canvas, electric cyan, restrained violet, geometric Q monogram.
- Matching light and dark assets selected with GitHub's `picture` support.
- CSS animation lives inside SVG images. No JavaScript runs in the README.
- Motion respects `prefers-reduced-motion` where the viewer supports it.
- Project navigation and native expandable sections provide interaction.
- All image assets are stored in this repository; no external stats-image service.
- `assets/avatar.png` is the matching 512 px avatar.
- `schedule-*.svg` and `booking-*.svg` provide matching project README headers.

## Daily updates

`.github/workflows/profile.yml` refreshes the dashboard and contribution calendar daily at 01:23 UTC, on relevant code changes, or manually from Actions. The standard GitHub Actions token is sufficient; no personal token or other secret is required.

The dashboard counts public repositories, stars on non-fork repositories, followers, and distinct primary languages in public non-fork repositories. Recent pushes are repository-level dates, not a claim that every commit was authored by QiuuDev. The contribution calendar shows the available calendar returned by GitHub. It is not a skill score or a live presence indicator.

API failures leave existing cards intact and fail the workflow visibly. GitHub may cache README images or delay scheduled runs. Refresh dates appear on the cards.

## Editing

Edit `README.md` for biography, project descriptions, and links. SVG assets remain editable source files. Run `python3 scripts/check_profile.py` to check rendering. Run `GH_TOKEN=... python3 scripts/update_profile.py` only in an environment with an authorized GitHub token; never commit a token.

The profile links only to existing public projects. Add other social accounts only after their URLs have been verified.
