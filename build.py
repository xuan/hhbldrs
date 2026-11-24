#!/usr/bin/env python3
"""Tiny static-site builder for the H&H Builders redesign demo (stdlib only).

src/layout.html          page shell ({{content}}, {{title}}, {{root}} ...)
src/partials/*.html      reusable sections, included with {{> name}}
src/pages/**/*.html      pages; first line is <!--meta {json} -->
src/assets/              copied as-is to dist/assets

Usage: python3 build.py            -> writes dist/
"""
import json, re, shutil
from pathlib import Path

ROOT = Path(__file__).parent
SRC, DIST = ROOT / "src", ROOT / "dist"
META_RE = re.compile(r"^\s*<!--meta\s+(\{.*?\})\s*-->\s*", re.S)
INCLUDE_RE = re.compile(r"\{\{>\s*([\w-]+)\s*\}\}")
VAR_RE = re.compile(r"\{\{\s*(\w+)\s*\}\}")
SITE = {
    "site_name": "H&H Builders",
    "phone": "(303) 450-7006",
    "phone_href": "tel:+13034507006",
    "email": "contact@hhbldrs.com",
}


def include(text, depth=0):
    if depth > 8:
        raise RuntimeError("include nesting too deep")
    return INCLUDE_RE.sub(
        lambda m: include((SRC / "partials" / f"{m[1]}.html").read_text(), depth + 1), text
    )


def render(text, ctx):
    return VAR_RE.sub(lambda m: str(ctx.get(m[1], m[0])), text)


def nav_state(active):
    keys = ["services", "projects", "design-build", "about", "faq", "contact"]
    return {f"cur_{k.replace('-', '_')}": ('aria-current="page"' if k == active else "") for k in keys}


def build():
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(SRC / "assets", DIST / "assets")
    layout = (SRC / "layout.html").read_text()
    pages = sorted((SRC / "pages").rglob("*.html"))
    for page in pages:
        raw = page.read_text()
        m = META_RE.match(raw)
        meta = json.loads(m[1]) if m else {}
        body = raw[m.end():] if m else raw
        rel = page.relative_to(SRC / "pages")
        depth = len(rel.parts) - 1
        ctx = {
            **SITE,
            "root": meta.get("root") or ("../" * depth if depth else "./"),
            "title": meta.get("title", SITE["site_name"]),
            "description": meta.get("description", ""),
            "body_class": meta.get("body_class", ""),
            **nav_state(meta.get("nav", "")),
        }
        html = include(layout.replace("{{content}}", body))
        html = render(render(html, ctx), ctx)  # second pass for vars inside partial args
        leftovers = VAR_RE.findall(html)
        if leftovers:
            raise RuntimeError(f"{rel}: unresolved vars {sorted(set(leftovers))}")
        out = DIST / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html)
    (DIST / ".nojekyll").write_text("")
    print(f"built {len(pages)} pages -> {DIST.relative_to(ROOT)}/")


if __name__ == "__main__":
    build()
