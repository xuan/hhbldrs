# CLAUDE.md

Static redesign preview for H&H Builders (hhbldrs.com), a Denver design-build and structural remodeler. It's based on the client's Digital Marketing & Content Audit (`docs/*.pdf`, local only). After the client approves the look, a second phase converts it into a native WordPress block theme for their **existing self-hosted WordPress** (not WordPress.com), via a staging copy first.

- Repo: `xuan/hhbldrs` (public). Preview: <https://xuan.github.io/hhbldrs/>
- Deploy: push to `main` → `.github/workflows/pages.yml` builds, checks and publishes `dist/`.

## Commands

- Build: `python3 build.py` (writes `dist/`, stdlib only)
- Check: `python3 scripts/check.py` (must pass; CI runs it)
- Serve: `python3 -m http.server 8000 -d dist`

## Structure

- `src/layout.html`: page shell. `src/partials/`: header, footer, CTA band, consultation form, project cards (`{{> name}}`).
- `src/pages/`: one file per page (home, services/*, projects/*, design-build, faq, about, contact, whats-changed, 404).
- `src/assets/css/site.css`: design tokens in `:root` (paper/stone backgrounds, brand green `#047832` from the logo, Fraunces + Inter). These map to `theme.json` in the WP phase.
- `src/assets/js/site.js`: progressive enhancement only (mobile nav, before/after toggle, project filter with `?type=`, demo form).

## Conventions

- Edit `src/`, never `dist/`. Pages start with `<!--meta {"title","description","nav"} -->`. Optional `"root"` overrides the relative root (used by 404).
- Use `{{root}}` for every internal URL; the site is served under `/hhbldrs/`.
- Exactly one `<h1>` per page. Before/after figures need the hidden `.ba__toggle` button for keyboard/touch users. No sliders/carousels (audit requirement).
- Keep text at WCAG AA contrast. `--brass` was darkened to `#7D6137` for this reason.
- Anything unverified (prices, timelines, quotes, testimonials) gets a `<span class="ph">…</span>` flag. Never present invented numbers or quotes as real. The list of what's still needed from the client is on `whats-changed.html`.
- Images: Unsplash stock placeholders (none show H&H work), WebP at 1600w + `-sm` 800w, credited in `src/assets/img/CREDITS.md`. `logo-mark.svg` is traced from their 270px PNG; replace it with the original when available.
- `docs/*.pdf` is the client's private audit and must not be committed (the repo is public).

## WordPress phase (after client approval)

Block theme with no page builder: tokens → `theme.json`, sections → block patterns, header/footer → template parts, case studies → `project` post type (location, scope, timeline, budget). Forms via Gravity Forms or WPForms. Add 301 redirects from old URLs (`/denver-remodel-album/*`, `/innovative/`, etc.).
