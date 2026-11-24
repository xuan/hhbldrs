# CLAUDE.md

Static redesign preview for H&H Builders (hhbldrs.com), deployed to GitHub Pages. A later phase converts it into a WordPress block theme for the client's existing self-hosted WordPress.

## Commands

- Build: `python3 build.py` (writes `dist/`, stdlib only)
- Check: `python3 scripts/check.py` (must pass; CI runs it)
- Serve: `python3 -m http.server 8000 -d dist`

## Conventions

- Edit `src/`, never `dist/`. Pages start with `<!--meta {"title","description","nav"} -->`.
- Use `{{root}}` for every internal URL; the site is served under `/hhbldrs/`.
- Exactly one `<h1>` per page. Before/after figures need the hidden `.ba__toggle` button for keyboard/touch users.
- Anything unverified (prices, timelines, quotes, testimonials) gets a `<span class="ph">…</span>` flag. Never present invented numbers or quotes as real.
- Images: WebP, 1600w + `-sm` 800w, credited in `src/assets/img/CREDITS.md`.
- `docs/*.pdf` is the client's private audit and must not be committed (the repo is public).
