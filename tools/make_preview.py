#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Baut eine einzelne, in sich geschlossene Vorschau-HTML aus den generierten Seiten."""
import base64
import io
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "tools", "vorschau.html")

DE = [
    ("blog.html", "Blog-Übersicht"),
    ("blog-strand-groemitz.html", "1 · Strand Grömitz"),
    ("blog-seebruecke-tauchgondel.html", "2 · Seebrücke & Tauchgondel"),
    ("blog-beste-reisezeit-groemitz.html", "3 · Beste Reisezeit"),
    ("blog-anreise-parken-groemitz.html", "4 · Anreise & Parken"),
    ("blog-kurtaxe-ostseecard-groemitz.html", "5 · Kurtaxe & ostseecard"),
    ("blog-groemitz-bei-regen.html", "6 · Grömitz bei Regen"),
    ("blog-tagesausfluege-groemitz.html", "7 · Tagesausflüge"),
    ("blog-groemitz-im-winter.html", "8 · Winter & Nebensaison"),
    ("blog-essen-restaurants-groemitz.html", "9 · Essen & Restaurants"),
    ("blog-barrierefrei-groemitz.html", "10 · Barrierefreier Urlaub"),
]
EN = [
    ("en/blog.html", "Blog index"),
    ("en/groemitz-beach-guide.html", "1 · Beach guide"),
    ("en/groemitz-pier-diving-gondola.html", "2 · Pier & diving gondola"),
    ("en/groemitz-best-time-to-visit.html", "3 · Best time to visit"),
    ("en/how-to-get-to-groemitz.html", "4 · Getting there"),
    ("en/groemitz-tourist-tax.html", "5 · Tourist tax"),
    ("en/groemitz-rainy-day.html", "6 · Rainy days"),
    ("en/day-trips-from-groemitz.html", "7 · Day trips"),
    ("en/groemitz-in-winter.html", "8 · Winter"),
    ("en/groemitz-restaurants-guide.html", "9 · Restaurants"),
    ("en/accessible-holiday-groemitz.html", "10 · Accessibility"),
]

css = io.open(os.path.join(ROOT, "styles.css"), encoding="utf-8").read()
img_cache = {}


def data_uri(path):
    if path in img_cache:
        return img_cache[path]
    full = os.path.join(ROOT, path)
    ext = os.path.splitext(path)[1].lower()
    mime = {".webp": "image/webp", ".png": "image/png", ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg", ".svg": "image/svg+xml"}.get(ext, "application/octet-stream")
    with open(full, "rb") as fh:
        uri = f"data:{mime};base64," + base64.b64encode(fh.read()).decode()
    img_cache[path] = uri
    return uri


img_order = []


def img_token(path):
    if path not in img_order:
        img_order.append(path)
    return img_order.index(path)


def build_page(rel):
    src = io.open(os.path.join(ROOT, rel), encoding="utf-8").read()
    base = os.path.dirname(rel)

    def resolve(p):
        return os.path.normpath(os.path.join(base, p)) if base else os.path.normpath(p)

    # Stylesheet als Platzhalter (wird zur Laufzeit einmalig eingesetzt)
    src = re.sub(r'<link rel="stylesheet" href="[^"]*styles\.css">',
                 "<style>@@CSS@@</style>", src)
    # Skript entfernen (Mobile-Menü wird in der Vorschau nicht gebraucht)
    src = re.sub(r'<script src="[^"]*main\.js"></script>', "", src)

    # Bilder als Data-URI
    def img_sub(m):
        p = m.group(2)
        if p.startswith(("http", "data:")):
            return m.group(0)
        f = resolve(p)
        if not os.path.exists(os.path.join(ROOT, f)):
            return m.group(0)
        return f'{m.group(1)}="@@IMG:{img_token(f)}@@"'

    src = re.sub(r'(src|href)="([^"]+\.(?:webp|png|jpe?g|svg))"', img_sub, src)

    # Interne Links auf Vorschau-Routing umbiegen
    def link_sub(m):
        href = m.group(1)
        if href.startswith(("http", "mailto:", "tel:", "#", "data:", "@@IMG:")):
            return m.group(0)
        target, _, frag = href.partition("#")
        if not target:
            return m.group(0)
        f = resolve(target)
        if f in PAGE_SET:
            return f'href="#/{f}{("#" + frag) if frag else ""}" data-route="{f}"'
        return 'href="#" data-external="1"'

    src = re.sub(r'href="([^"]+)"', link_sub, src)
    return src


PAGES = DE + EN
PAGE_SET = {p for p, _ in PAGES}
docs = {rel: build_page(rel) for rel, _ in PAGES}


def safe_json(obj):
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


def nav(items):
    return "\n".join(
        f'<li><button class="nav-item" data-page="{rel}">{label}</button></li>'
        for rel, label in items
    )


html = f"""<title>Grömitz-Ratgeber Vorschau</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {{
  --ground: #efece6;
  --panel: #ffffff;
  --ink: #16150f;
  --muted: #6f6a5f;
  --hair: #dcd6ca;
  --accent: #1d3f4a;
  --accent-soft: #e3ebec;
}}
:root:not([data-theme="light"]) {{}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --ground: #16150f;
    --panel: #1e1d17;
    --ink: #f2efe7;
    --muted: #a09a8d;
    --hair: #34322a;
    --accent: #8fc0cd;
    --accent-soft: #24312f;
  }}
}}
:root[data-theme="dark"] {{
  --ground: #16150f;
  --panel: #1e1d17;
  --ink: #f2efe7;
  --muted: #a09a8d;
  --hair: #34322a;
  --accent: #8fc0cd;
  --accent-soft: #24312f;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  background: var(--ground);
  color: var(--ink);
  font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: 15px;
  line-height: 1.5;
}}
.shell {{ display: grid; grid-template-columns: 268px 1fr; min-height: 100vh; }}
.rail {{
  background: var(--panel);
  border-right: 1px solid var(--hair);
  padding: 24px 18px 40px;
  display: flex; flex-direction: column; gap: 22px;
  position: sticky; top: 0; height: 100vh; overflow-y: auto;
}}
.brand {{ display: flex; flex-direction: column; gap: 4px; }}
.brand strong {{ font-size: 15px; font-weight: 600; letter-spacing: -0.01em; }}
.brand span {{ font-size: 12px; color: var(--muted); }}
.meta {{
  font-size: 12px; color: var(--muted); line-height: 1.6;
  border: 1px solid var(--hair); border-radius: 10px; padding: 12px 14px;
}}
.meta b {{ color: var(--ink); font-weight: 600; }}
.group-label {{
  font-size: 11px; font-weight: 600; letter-spacing: 0.09em; text-transform: uppercase;
  color: var(--muted); margin: 0 0 8px 2px;
}}
ul {{ list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 2px; }}
.nav-item {{
  width: 100%; text-align: left; border: 0; background: transparent; cursor: pointer;
  font: inherit; font-size: 13.5px; color: var(--ink);
  padding: 7px 10px; border-radius: 7px; line-height: 1.35;
}}
.nav-item:hover {{ background: var(--accent-soft); }}
.nav-item[aria-current="true"] {{ background: var(--accent); color: var(--panel); font-weight: 500; }}
.nav-item:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
.stage {{ display: flex; flex-direction: column; min-width: 0; }}
.toolbar {{
  display: flex; align-items: center; gap: 14px; flex-wrap: wrap;
  padding: 12px 20px; border-bottom: 1px solid var(--hair); background: var(--panel);
}}
.path {{ font-size: 12.5px; color: var(--muted); font-variant-numeric: tabular-nums; }}
.path b {{ color: var(--ink); font-weight: 600; }}
.spacer {{ flex: 1; }}
.seg {{ display: inline-flex; border: 1px solid var(--hair); border-radius: 8px; overflow: hidden; }}
.seg button {{
  border: 0; background: transparent; font: inherit; font-size: 12.5px; cursor: pointer;
  padding: 6px 12px; color: var(--muted);
}}
.seg button[aria-pressed="true"] {{ background: var(--accent); color: var(--panel); }}
.viewport {{ flex: 1; display: flex; justify-content: center; padding: 20px; overflow: auto; }}
iframe {{
  border: 1px solid var(--hair); border-radius: 12px; background: #fff;
  width: 100%; height: 100%; min-height: 78vh; display: block;
}}
.frame-wrap {{ width: 100%; max-width: 100%; display: flex; justify-content: center; }}
.frame-wrap[data-w="mobile"] iframe {{ width: 402px; max-width: 100%; }}
.hint {{ font-size: 12px; color: var(--muted); padding: 0 20px 16px; }}
@media (max-width: 900px) {{
  .shell {{ grid-template-columns: 1fr; }}
  .rail {{ position: static; height: auto; }}
}}
</style>

<div class="shell">
  <aside class="rail">
    <div class="brand">
      <strong>Grömitz-Ratgeber</strong>
      <span>Vorschau vor dem Push · 23. August 2026</span>
    </div>
    <div class="meta">
      <b>22 Seiten</b> · 10 Artikel auf Deutsch, 10 auf Englisch, 2 Übersichten.<br>
      Rendering mit dem echten <b>styles.css</b> der Website. Interne Links funktionieren.
    </div>
    <nav>
      <p class="group-label">Deutsch</p>
      <ul>
{nav(DE)}
      </ul>
    </nav>
    <nav>
      <p class="group-label">English</p>
      <ul>
{nav(EN)}
      </ul>
    </nav>
  </aside>

  <main class="stage">
    <div class="toolbar">
      <span class="path">lieblingsplatz-groemitz.de/<b id="cur">blog.html</b></span>
      <span class="spacer"></span>
      <span class="seg" role="group" aria-label="Ansicht">
        <button type="button" data-w="desktop" aria-pressed="true">Desktop</button>
        <button type="button" data-w="mobile" aria-pressed="false">Mobil</button>
      </span>
    </div>
    <div class="viewport">
      <div class="frame-wrap" data-w="desktop">
        <iframe id="frame" title="Seitenvorschau"></iframe>
      </div>
    </div>
    <p class="hint">Externe Links und Links auf Seiten außerhalb des Blogs sind in der Vorschau deaktiviert.</p>
  </main>
</div>

<script id="docs" type="application/json">{safe_json(docs)}</script>
<script id="assets" type="application/json">{safe_json({"css": css, "img": [data_uri(p) for p in img_order]})}</script>
<script>
(function () {{
  const DOCS = JSON.parse(document.getElementById('docs').textContent);
  const ASSETS = JSON.parse(document.getElementById('assets').textContent);
  const hydrate = html => html
    .replace('@@CSS@@', () => ASSETS.css)
    .replace(/@@IMG:(\d+)@@/g, (_, i) => ASSETS.img[+i]);
  const frame = document.getElementById('frame');
  const cur = document.getElementById('cur');
  const buttons = Array.from(document.querySelectorAll('.nav-item'));

  function show(page, frag) {{
    if (!DOCS[page]) return;
    frame.srcdoc = hydrate(DOCS[page]);
    cur.textContent = page;
    buttons.forEach(b => b.setAttribute('aria-current', String(b.dataset.page === page)));
    frame.addEventListener('load', function once() {{
      frame.removeEventListener('load', once);
      const d = frame.contentDocument;
      if (!d) return;
      d.addEventListener('click', function (e) {{
        const a = e.target.closest('a');
        if (!a) return;
        const route = a.getAttribute('data-route');
        if (route) {{ e.preventDefault(); show(route); return; }}
        if (a.getAttribute('data-external')) {{ e.preventDefault(); return; }}
        const href = a.getAttribute('href') || '';
        if (href.startsWith('#')) return;
        if (!href.startsWith('http')) e.preventDefault();
      }});
      if (frag) {{
        const t = d.getElementById(frag);
        if (t) t.scrollIntoView();
      }}
    }});
  }}

  buttons.forEach(b => b.addEventListener('click', () => show(b.dataset.page)));

  document.querySelectorAll('.seg button').forEach(b => {{
    b.addEventListener('click', () => {{
      document.querySelectorAll('.seg button').forEach(x => x.setAttribute('aria-pressed', String(x === b)));
      document.querySelector('.frame-wrap').dataset.w = b.dataset.w;
    }});
  }});

  show('blog.html');
}})();
</script>
"""

io.open(OUT, "w", encoding="utf-8").write(html)
print(f"{OUT} geschrieben, {os.path.getsize(OUT)/1024/1024:.1f} MB, {len(docs)} Seiten")
