# Blog-Generator

Erzeugt die Blogartikel (DE + EN), die Übersichtsseiten `blog.html` / `en/blog.html`
und die `sitemap.xml` aus den Inhaltsdateien in `tools/art/`.

## Verwendung

```bash
python3 tools/build_blog.py
```

Das Skript schreibt in die Projektwurzel. `tools/` selbst wird über `.vercelignore`
nicht deployt.

## Neuen Artikel anlegen

1. `tools/art/a11.py` nach dem Muster einer bestehenden Datei anlegen.
2. In `tools/articles.py` importieren und der Liste `ARTICLES` hinzufügen.
3. Hero-/Kartenbild als WebP in `assets/images/blog/<name>-1280.webp`
   und `<name>-800.webp` ablegen, `"img": "<name>"` im Artikel setzen.
4. `python3 tools/build_blog.py` ausführen.

## Felder pro Artikel

| Feld | Bedeutung |
|---|---|
| `slug_de` / `slug_en` | Dateinamen (EN landet unter `en/`) |
| `title_*` | Title-Tag, max. 60 Zeichen |
| `desc_*` | Meta-Description, 120–165 Zeichen |
| `answer_*` | Antwortblock „Kurz & knapp“ – 40–60 Wörter, GEO-relevant |
| `toc_*` | Liste `(anker, label)`, muss zu den `id`s im Body passen |
| `body_*` | HTML des Fließtexts |
| `faq_*` | Liste `(frage, antwort)` – wird zusätzlich als FAQPage-Schema ausgegeben |
| `sources` | Liste `(label, url)` für den Quellenblock |
| `related_*` | Liste `(href, label)` für die Verlinkung am Ende |
| `cta_*` | Tupel `(überschrift, text)` für die CTA-Box |
