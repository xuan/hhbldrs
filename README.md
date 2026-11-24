# H&H Builders: redesign preview

A static preview of the proposed redesign for [hhbldrs.com](https://www.hhbldrs.com). The design follows the recommendations in the Digital Marketing & Content Audit. Once the client approves it, it will be converted into a native WordPress block theme for their existing site.

**Live preview:** https://xuan.github.io/hhbldrs/
**What changed & why:** https://xuan.github.io/hhbldrs/whats-changed.html

> All photography is licensed Unsplash stock used as placeholders (see [`src/assets/img/CREDITS.md`](src/assets/img/CREDITS.md)). None of it shows H&H projects. Anything marked **Placeholder** / **Confirm** in the preview needs client input.

## Structure

```
src/
  layout.html          page shell (head, header, footer)
  partials/            reusable sections, included with {{> name}}
  pages/               one file per page; first line is <!--meta {json}-->
  assets/css/site.css  design tokens + components (map to theme.json later)
  assets/js/site.js    progressive enhancement only (nav, before/after, filter, demo form)
  assets/img/          WebP images, 1600w + 800w (-sm)
build.py               stdlib-only builder -> dist/
scripts/check.py       broken links/anchors, duplicate ids, one <h1>, img alt
```

## Build & preview locally

```sh
python3 build.py && python3 scripts/check.py
python3 -m http.server 8000 -d dist   # open http://localhost:8000
```

Pushing to `main` builds and deploys to GitHub Pages via `.github/workflows/pages.yml`.

## Next phase: WordPress

- Convert `site.css` tokens to `theme.json` (colors, font sizes, spacing)
- Turn each section (hero, trust strip, service cards, before/after, steps, FAQ, CTA band) into block patterns
- Header and footer become template parts. Case studies become a `project` post type with fields for location, scope, timeline and budget.
- Forms: Gravity Forms or WPForms, with conversion tracking
- 301 redirects from the old URLs (e.g. `/denver-remodel-album/*`, `/innovative/`) to the new pages
- Deploy to a staging copy of the existing self-hosted install first
