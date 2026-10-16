# QiuuDev / Portfolio identity

Public profile identity for QiuuDev (BoringDev).

- Portfolio canvas `#020609`, electric cyan `#00f5ff`, pale text `#e4f2f8`, geometric Q monogram.
- Responsive desktop/mobile artwork selected with GitHub's `picture` support. Identity panels preserve the portfolio's dark canvas in either GitHub theme.
- CSS animation lives inside SVG images. No JavaScript runs in the README.
- Motion respects `prefers-reduced-motion` where the viewer supports it.
- Project navigation and native expandable sections provide interaction.
- All image assets are stored in this repository; no external stats-image service.
- Orbitron heading glyphs are converted to paths, preserving the portfolio typography without external font requests. The font's SIL Open Font License is included in `assets/fonts/OFL.txt`.
- Existing avatar, social cards and legacy project headers remain available; this revision changes the profile README artwork.

## Content

The profile leads with Muhammad Qodri / QiuuDev, part-time Front-End Developer at Talikama Creative, studying Computer Science at Universitas Bumigora. The quotation matches the approved portfolio: "Lazy by nature. Efficient by choice. Automated by design."

Core stacks are PHP, Dart/Flutter and Python. Supporting tools are grouped separately without numeric skill ratings. Five cards cover client websites and public projects. Stride is labeled an MVP and its coach is described as rule-based. Seven verified public repositories are linked. Private projects are not listed.

The old anchor menu is replaced by two clear entry points: portfolio and repositories. Biography and project panels have consistent padding and descriptive text alternatives; an expandable Indonesian biography remains selectable text. Professional contact links use the existing portfolio, LinkedIn, Instagram, email and WhatsApp URLs.

## Daily updates

`.github/workflows/profile.yml` refreshes the dashboard and contribution calendar daily at 01:23 UTC, on relevant code changes, or manually from Actions. The standard GitHub Actions token is sufficient; no personal token or other secret is required.

The dashboard counts public repositories, stars on non-fork repositories, followers, and distinct primary languages in public non-fork repositories. Recent pushes are repository-level dates, not a claim that every commit was authored by QiuuDev. The contribution calendar shows the available calendar returned by GitHub. It is not a skill score or a live presence indicator.

API failures leave existing cards intact and fail the workflow visibly. GitHub may cache README images or delay scheduled runs. Refresh dates appear on the cards.

## Editing

Edit `scripts/build_identity.py` for biography, project descriptions, links and static art. With the development-only `fonttools` package installed, run `python3 scripts/build_identity.py` to regenerate `README.md` and `assets/portfolio-*.svg`. The daily workflow does not rebuild static identity artwork and requires no additional dependency. `scripts/update_profile.py` owns the matching colors of daily cards. Run `python3 scripts/check_profile.py` to check privacy filtering, escaping and calendar placement. Run `GH_TOKEN=... python3 scripts/update_profile.py` only in an environment with an authorized GitHub token; never commit a token.

The profile links only to existing public projects. Add other social accounts only after their URLs have been verified.

## Responsive refinement

Mobile visitors receive larger typography, a two-column toolkit, project cards, and a readable telemetry dashboard. The mobile contribution card retains the yearly total and shows the most recent 12 weeks. Desktop displays the full-year matrix. Native expandable sections provide interaction without JavaScript.
