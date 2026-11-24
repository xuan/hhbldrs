#!/usr/bin/env python3
"""Sanity checks for dist/: broken local links/images, duplicate ids, one <h1> per page, img alt present."""
import sys, re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote

DIST = Path(__file__).resolve().parent.parent / "dist"
problems = []

class P(HTMLParser):
    def __init__(s): super().__init__(); s.refs=[]; s.ids=[]; s.h1=0; s.noalt=0
    def handle_starttag(s, t, a):
        a = dict(a)
        if "id" in a: s.ids.append(a["id"])
        if t == "h1": s.h1 += 1
        if t == "img" and "alt" not in a: s.noalt += 1
        for k in ("href", "src"):
            if k in a and a[k]: s.refs.append(a[k])
        if "srcset" in a:
            s.refs += [x.strip().split()[0] for x in a["srcset"].split(",")]

for f in sorted(DIST.rglob("*.html")):
    p = P(); p.feed(f.read_text()); rel = f.relative_to(DIST)
    if p.h1 != 1: problems.append(f"{rel}: {p.h1} <h1>")
    if p.noalt: problems.append(f"{rel}: {p.noalt} img without alt")
    dup = {i for i in p.ids if p.ids.count(i) > 1}
    if dup: problems.append(f"{rel}: duplicate ids {dup}")
    ids = set(p.ids)
    for r in p.refs:
        u = urlparse(r)
        if u.scheme in ("http", "https", "mailto", "tel", "data"): continue
        if r.startswith("#"):
            if r[1:] and r[1:] not in ids: problems.append(f"{rel}: missing anchor {r}")
            continue
        path = unquote(u.path)
        if path.startswith("/hhbldrs/"): target = DIST / path[len("/hhbldrs/"):]
        else: target = (f.parent / path).resolve()
        if not target.exists(): problems.append(f"{rel}: broken {r}")
        elif u.fragment and target.suffix == ".html":
            tp = P(); tp.feed(target.read_text())
            if u.fragment not in tp.ids: problems.append(f"{rel}: missing anchor {r}")

print("\n".join(problems) or "all checks passed")
sys.exit(1 if problems else 0)
