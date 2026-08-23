#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator für die Blogartikel von lieblingsplatz-groemitz.de
Erzeugt DE-Artikel im Root und EN-Artikel unter /en/,
plus blog.html, en/blog.html und sitemap.xml.
"""
import json
import os
import datetime

SITE = "https://www.lieblingsplatz-groemitz.de"
TODAY = "2026-08-23"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Projektwurzel

AUTHORS = {
    "PK": "Patricia Kreutzheide",
    "LK": "Leon Kreutzheide",
}

UI = {
    "de": {
        "back": "Zurück zum Blog",
        "blog_file": "blog.html",
        "home": "Startseite",
        "blog_crumb": "Blog",
        "updated": "Aktualisiert am 23. August 2026",
        "readtime": "Min. Lesezeit",
        "answer": "Kurz & knapp",
        "toc": "Inhalt",
        "faq": "Häufige Fragen",
        "sources": "Quellen und Stand der Angaben",
        "related": "Passend dazu",
        "lang_link": "Read this article in English",
        "nav": [
            ("index.html#startseite", "Startseite"),
            ("index.html#die-wohnung", "Die Wohnung"),
            ("index.html#ausstattung", "Ausstattung"),
            ("index.html#preise", "Preise"),
            ("index.html#kontakt", "Kontakt"),
        ],
        "cta_btn": "Jetzt reservieren",
        "footer_seo": [
            ("ferienwohnung-groemitz.html", "Ferienwohnung Grömitz"),
            ("ferienwohnung-groemitz-strandnah.html", "Ferienwohnung Grömitz Strandnah"),
            ("penthouse-ferienwohnung-groemitz.html", "Penthouse Ferienwohnung Grömitz"),
            ("barrierefreie-ferienwohnung-groemitz.html", "Barrierefreie Ferienwohnung Grömitz"),
            ("blog.html", "Grömitz-Ratgeber"),
        ],
        "footer_legal": [
            ("impressum.html", "Impressum"),
            ("datenschutz.html", "Datenschutz"),
            ("agb.html", "AGB"),
        ],
        "copyright": "© 2026 Lieblingsplatz Grömitz. Alle Rechte vorbehalten.",
    },
    "en": {
        "back": "Back to the blog",
        "blog_file": "blog.html",
        "home": "Home",
        "blog_crumb": "Blog",
        "updated": "Updated 23 August 2026",
        "readtime": "min read",
        "answer": "In short",
        "toc": "Contents",
        "faq": "Frequently asked questions",
        "sources": "Sources and last update",
        "related": "Related reading",
        "lang_link": "Diesen Artikel auf Deutsch lesen",
        "nav": [
            ("../index.html#startseite", "Home"),
            ("../index.html#die-wohnung", "The apartment"),
            ("../index.html#ausstattung", "Amenities"),
            ("../index.html#preise", "Rates"),
            ("../index.html#kontakt", "Contact"),
        ],
        "cta_btn": "Book now",
        "footer_seo": [
            ("../ferienwohnung-groemitz.html", "Ferienwohnung Grömitz"),
            ("../ferienwohnung-groemitz-strandnah.html", "Ferienwohnung Grömitz Strandnah"),
            ("../penthouse-ferienwohnung-groemitz.html", "Penthouse Ferienwohnung Grömitz"),
            ("../barrierefreie-ferienwohnung-groemitz.html", "Barrierefreie Ferienwohnung Grömitz"),
            ("../blog.html", "Grömitz-Ratgeber"),
        ],
        "footer_legal": [
            ("../impressum.html", "Impressum"),
            ("../datenschutz.html", "Privacy"),
            ("../agb.html", "Terms"),
        ],
        "copyright": "© 2026 Lieblingsplatz Grömitz. All rights reserved.",
    },
}


def nav_html(lang):
    u = UI[lang]
    p = "../" if lang == "en" else ""
    links = "\n".join(
        f'                <a href="{href}" class="nav-link">{label}</a>'
        for href, label in u["nav"]
    )
    cta = f"{p}index.html#kontakt"
    return f"""    <header class="navbar">
        <div class="navbar-container">
            <a href="{p}index.html" class="navbar-brand">
                <img src="{p}groemitz/cropped-Herz_Icon.png" alt="Lieblingsplatz Grömitz Logo" class="brand-logo">
                <span class="brand-name">Lieblingsplatz Grömitz</span>
            </a>
            <nav class="navbar-nav">
{links}
            </nav>
            <div class="navbar-cta">
                <a href="{cta}" class="btn btn-dark">{u['cta_btn']}</a>
            </div>
            <button class="mobile-menu-btn" aria-label="Menü öffnen">
                <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="3" y1="12" x2="21" y2="12"></line>
                    <line x1="3" y1="6" x2="21" y2="6"></line>
                    <line x1="3" y1="18" x2="21" y2="18"></line>
                </svg>
            </button>
        </div>
    </header>"""


def footer_html(lang):
    u = UI[lang]
    seo = '\n                <span class="fw-footer-divider">|</span>\n'.join(
        f'                <a href="{href}">{label}</a>' for href, label in u["footer_seo"]
    )
    legal = '\n                <span class="fw-footer-divider">|</span>\n'.join(
        f'                <a href="{href}">{label}</a>' for href, label in u["footer_legal"]
    )
    return f"""    <footer class="fw-footer-new">
        <div class="container">
            <div class="fw-footer-links-seo">
{seo}
            </div>
            <div class="fw-footer-links-legal">
{legal}
            </div>
            <div class="fw-footer-copyright">
                {u['copyright']}
            </div>
        </div>
    </footer>"""


def head_html(a, lang):
    """a: article dict, lang: 'de'|'en'"""
    p = "../" if lang == "en" else ""
    de_url = f"{SITE}/{a['slug_de']}"
    en_url = f"{SITE}/en/{a['slug_en']}"
    canonical = de_url if lang == "de" else en_url
    title = a["title_de"] if lang == "de" else a["title_en"]
    desc = a["desc_de"] if lang == "de" else a["desc_en"]
    h1 = a["h1_de"] if lang == "de" else a["h1_en"]
    answer = a["answer_de"] if lang == "de" else a["answer_en"]
    faqs = a["faq_de"] if lang == "de" else a["faq_en"]
    u = UI[lang]

    blogposting = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": h1,
        "description": desc,
        "inLanguage": "de-DE" if lang == "de" else "en-GB",
        "image": f"{SITE}/assets/images/blog/{a['img']}-1280.webp",
        "datePublished": a["published"],
        "dateModified": TODAY,
        "author": {
            "@type": "Person",
            "name": AUTHORS[a["author"]],
        },
        "publisher": {
            "@type": "Organization",
            "name": "Lieblingsplatz Grömitz",
            "logo": {
                "@type": "ImageObject",
                "url": f"{SITE}/groemitz/cropped-Herz_Icon.png",
            },
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
        "about": [{"@type": "Place", "name": n} for n in a["entities"]],
        "abstract": answer,
    }

    faqpage = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": ans},
            }
            for q, ans in faqs
        ],
    }

    crumb_blog = f"{SITE}/blog.html" if lang == "de" else f"{SITE}/en/blog.html"
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": u["home"], "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": u["blog_crumb"], "item": crumb_blog},
            {"@type": "ListItem", "position": 3, "name": h1, "item": canonical},
        ],
    }

    def ld(obj):
        return (
            '    <script type="application/ld+json">\n    '
            + json.dumps(obj, ensure_ascii=False, indent=2).replace("\n", "\n    ")
            + "\n    </script>"
        )

    return f"""<!DOCTYPE html>
<html lang="{'de' if lang == 'de' else 'en'}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <link rel="canonical" href="{canonical}">
    <link rel="alternate" hreflang="de" href="{de_url}">
    <link rel="alternate" hreflang="en" href="{en_url}">
    <link rel="alternate" hreflang="x-default" href="{de_url}">

    <meta property="og:type" content="article">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="{SITE}/assets/images/blog/{a['img']}-1280.webp">
    <meta property="og:locale" content="{'de_DE' if lang == 'de' else 'en_GB'}">
    <meta property="og:site_name" content="Lieblingsplatz Grömitz">
    <meta name="twitter:card" content="summary_large_image">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{p}styles.css">
    <link rel="icon" type="image/png" href="{p}groemitz/cropped-Herz_Icon.png">
    <link rel="apple-touch-icon" href="{p}groemitz/cropped-Herz_Icon.png">

{ld(blogposting)}

{ld(faqpage)}

{ld(breadcrumb)}
</head>"""


def article_html(a, lang):
    u = UI[lang]
    p = "../" if lang == "en" else ""
    h1 = a["h1_de"] if lang == "de" else a["h1_en"]
    badge = a["badge_de"] if lang == "de" else a["badge_en"]
    answer = a["answer_de"] if lang == "de" else a["answer_en"]
    body = a["body_de"] if lang == "de" else a["body_en"]
    faqs = a["faq_de"] if lang == "de" else a["faq_en"]
    toc = a["toc_de"] if lang == "de" else a["toc_en"]
    related = a["related_de"] if lang == "de" else a["related_en"]
    sources = a["sources"]
    cta = a["cta_de"] if lang == "de" else a["cta_en"]
    other = (f"en/{a['slug_en']}" if lang == "de" else f"{p}{a['slug_de']}")

    toc_items = "\n".join(
        f'                    <li><a href="#{anchor}">{label}</a></li>'
        for anchor, label in toc
    )
    faq_items = "\n".join(
        f"""                <div class="faq-item">
                    <h3>{q}</h3>
                    <p>{ans}</p>
                </div>"""
        for q, ans in faqs
    )
    related_items = "\n".join(
        f'                    <li><a href="{href}">{label}</a></li>' for href, label in related
    )
    source_items = " · ".join(
        f'<a href="{href}" target="_blank" rel="noopener nofollow">{label}</a>'
        for label, href in sources
    )

    return f"""{head_html(a, lang)}
<body>
{nav_html(lang)}

    <main>
        <div class="blog-article-hero">
            <img src="{p}assets/images/blog/{a['img']}-1280.webp" alt="{a['alt_de'] if lang == 'de' else a['alt_en']}" width="1280" height="720" fetchpriority="high">
        </div>

        <article class="blog-article-container">
            <a href="{p}{u['blog_file']}" class="blog-article-back">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
                {u['back']}
            </a>

            <nav class="article-breadcrumb" aria-label="Breadcrumb">
                <a href="{p}index.html">{u['home']}</a><span>›</span><a href="{p}{u['blog_file']}">{u['blog_crumb']}</a><span>›</span>{badge}
            </nav>

            <div class="blog-article-badge">{badge}</div>
            <h1 class="blog-article-title">{h1}</h1>
            <div class="blog-article-meta">{AUTHORS[a['author']]} · {u['updated']} · {a['readtime']} {u['readtime']}</div>
            <div class="article-lang"><a href="{other}">{u['lang_link']}</a></div>

            <div class="geo-answer">
                <h2 class="geo-answer-title">{u['answer']}</h2>
                <p>{answer}</p>
            </div>

            <nav class="article-toc" aria-label="{u['toc']}">
                <div class="article-toc-title">{u['toc']}</div>
                <ol>
{toc_items}
                </ol>
            </nav>

            <div class="blog-article-content">
{body}
            </div>

            <section class="article-faq">
                <h2>{u['faq']}</h2>
{faq_items}
            </section>

            <div class="article-sources">
                <strong>{u['sources']}</strong>
                {source_items}
            </div>

            <div class="blog-cta-box">
                <h3>{cta[0]}</h3>
                <p>{cta[1]}</p>
                <a href="{p}index.html#kontakt" class="btn btn-dark">{u['cta_btn']}</a>
            </div>

            <nav class="article-related">
                <h2>{u['related']}</h2>
                <ul>
{related_items}
                </ul>
            </nav>
        </article>
    </main>

{footer_html(lang)}

    <script src="{p}main.js"></script>
</body>
</html>
"""


def blog_index(articles, lang):
    u = UI[lang]
    p = "../" if lang == "en" else ""
    if lang == "de":
        title = "Grömitz-Ratgeber: Strand, Anreise, Ausflüge & Tipps | Blog"
        desc = ("Ehrliche Tipps von Gastgebern vor Ort: Strandabschnitte, Anreise, Kurtaxe, "
                "beste Reisezeit, Ausflugsziele und Restaurants in Grömitz an der Ostsee.")
        label = "BLOG & RATGEBER"
        h1 = "Der Grömitz-Ratgeber Ihrer Gastgeber"
        sub = ("Alles, was Sie vor und während Ihres Ostsee-Urlaubs wissen wollen – "
               "recherchiert und regelmäßig aktualisiert.")
        canonical = f"{SITE}/blog.html"
    else:
        title = "Grömitz Travel Guide: Beach, Getting There & Tips | Blog"
        desc = ("Local hosts' guide to Grömitz on the German Baltic coast: beaches, travel, "
                "tourist tax, best time to visit, day trips and where to eat.")
        label = "BLOG & GUIDES"
        h1 = "The Grömitz guide from your hosts"
        sub = "Everything worth knowing before and during your Baltic Sea holiday."
        canonical = f"{SITE}/en/blog.html"

    cards = []
    for a in articles:
        href = (a["slug_de"] if lang == "de" else a["slug_en"])
        t = a["card_title_de"] if lang == "de" else a["card_title_en"]
        txt = a["card_text_de"] if lang == "de" else a["card_text_en"]
        badge = a["badge_de"] if lang == "de" else a["badge_en"]
        more = "Weiterlesen" if lang == "de" else "Read more"
        cards.append(f"""                <article class="blog-page-card">
                    <div class="blog-page-img-wrapper">
                        <img src="{p}assets/images/blog/{a['img']}-800.webp" alt="{a['alt_de'] if lang == 'de' else a['alt_en']}" class="blog-page-img" loading="lazy" width="800" height="450">
                        <div class="blog-page-badge">{badge}</div>
                    </div>
                    <div class="blog-page-content">
                        <h2 class="blog-page-card-title">{t}</h2>
                        <p class="blog-page-card-text">{txt}</p>
                        <div class="blog-page-meta">
                            <div class="blog-page-author-info">
                                <div class="blog-page-avatar">{a['author']}</div>
                                <div class="blog-page-author-details">
                                    <span class="blog-page-author-name">{AUTHORS[a['author']]}</span>
                                    <span class="blog-page-date">{a['readtime']} {UI[lang]['readtime']}</span>
                                </div>
                            </div>
                            <a href="{href}" class="blog-page-readmore">{more} <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg></a>
                        </div>
                    </div>
                </article>""")

    itemlist = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": h1,
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "url": f"{SITE}/{a['slug_de']}" if lang == "de" else f"{SITE}/en/{a['slug_en']}",
                "name": a["card_title_de"] if lang == "de" else a["card_title_en"],
            }
            for i, a in enumerate(articles)
        ],
    }

    other = "en/blog.html" if lang == "de" else "../blog.html"
    lang_link = "Read these guides in English" if lang == "de" else "Diese Seite auf Deutsch lesen"

    legacy = [
        ("blog-fahrradtouren.html", "Aktivitäten",
         "Fahrradtouren an der Ostsee: die schönsten Routen",
         "Küstentouren und Strecken durchs Hinterland ab Grömitz, mit Länge, Schwierigkeit und Einkehrmöglichkeiten.",
         "Cycling on the Baltic coast: the best routes",
         "Coastal rides and inland routes from Grömitz, with distances, difficulty and places to stop.",
         "LK", "blog_promenade"),
        ("blog-wassersport.html", "Wassersport",
         "Wassersport in Grömitz: Surfen, Segeln und mehr",
         "Die besten Spots für Wind- und Wassersport rund um Grömitz und Dahme.",
         "Watersports in Grömitz: surfing, sailing and more",
         "The best spots for wind and water sports around Grömitz and Dahme.",
         "LK", "blog_beach"),
    ]
    legacy_cards = []
    for href, badge, t_de, x_de, t_en, x_en, author, img in legacy:
        t = t_de if lang == "de" else t_en
        x = x_de if lang == "de" else x_en
        more = "Weiterlesen" if lang == "de" else "Read more"
        link = href if lang == "de" else "../" + href
        note = "" if lang == "de" else ' <span style="font-size:12px;color:#888">(auf Deutsch)</span>'
        legacy_cards.append(f"""                <article class="blog-page-card">
                    <div class="blog-page-img-wrapper">
                        <img src="{p}assets/images/blog/{img}-800.webp" alt="{t}" class="blog-page-img" loading="lazy" width="800" height="450">
                        <div class="blog-page-badge">{badge}</div>
                    </div>
                    <div class="blog-page-content">
                        <h2 class="blog-page-card-title">{t}{note}</h2>
                        <p class="blog-page-card-text">{x}</p>
                        <div class="blog-page-meta">
                            <div class="blog-page-author-info">
                                <div class="blog-page-avatar">{author}</div>
                                <div class="blog-page-author-details">
                                    <span class="blog-page-author-name">{AUTHORS[author]}</span>
                                    <span class="blog-page-date">Archiv</span>
                                </div>
                            </div>
                            <a href="{link}" class="blog-page-readmore">{more} <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg></a>
                        </div>
                    </div>
                </article>""")
    cards.extend(legacy_cards)

    return f"""<!DOCTYPE html>
<html lang="{'de' if lang == 'de' else 'en'}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <link rel="canonical" href="{canonical}">
    <link rel="alternate" hreflang="de" href="{SITE}/blog.html">
    <link rel="alternate" hreflang="en" href="{SITE}/en/blog.html">
    <link rel="alternate" hreflang="x-default" href="{SITE}/blog.html">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="{canonical}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{p}styles.css">
    <link rel="icon" type="image/png" href="{p}groemitz/cropped-Herz_Icon.png">
    <link rel="apple-touch-icon" href="{p}groemitz/cropped-Herz_Icon.png">
    <script type="application/ld+json">
    {json.dumps(itemlist, ensure_ascii=False, indent=2).replace(chr(10), chr(10) + "    ")}
    </script>
</head>
<body>
{nav_html(lang)}

    <main>
        <section class="blog-page-header">
            <div class="container text-center">
                <div class="blog-page-label">{label}</div>
                <h1 class="blog-page-title font-thin">{h1}</h1>
                <p class="blog-page-subtitle">{sub}</p>
                <p class="article-lang" style="margin-top:20px"><a href="{other}">{lang_link}</a></p>
            </div>
        </section>

        <section class="blog-page-grid-section">
            <div class="container blog-page-grid">

{chr(10).join(cards)}

            </div>
        </section>
    </main>

{footer_html(lang)}

    <script src="{p}main.js"></script>
</body>
</html>
"""


def sitemap(articles):
    entries = [
        ("/", "weekly", "1.0"),
        ("/ferienwohnung-groemitz.html", "monthly", "0.9"),
        ("/ferienwohnung-groemitz-strandnah.html", "monthly", "0.9"),
        ("/penthouse-ferienwohnung-groemitz.html", "monthly", "0.9"),
        ("/barrierefreie-ferienwohnung-groemitz.html", "monthly", "0.9"),
        ("/blog.html", "weekly", "0.8"),
        ("/en/blog.html", "weekly", "0.6"),
        ("/blog-fahrradtouren.html", "monthly", "0.6"),
        ("/blog-wassersport.html", "monthly", "0.6"),
    ]
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
           'xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for loc, freq, prio in entries:
        out.append("  <url>")
        out.append(f"    <loc>{SITE}{loc}</loc>")
        out.append(f"    <lastmod>{TODAY}</lastmod>")
        out.append(f"    <changefreq>{freq}</changefreq>")
        out.append(f"    <priority>{prio}</priority>")
        out.append("  </url>")
    for a in articles:
        for lang in ("de", "en"):
            loc = f"/{a['slug_de']}" if lang == "de" else f"/en/{a['slug_en']}"
            out.append("  <url>")
            out.append(f"    <loc>{SITE}{loc}</loc>")
            out.append(f"    <lastmod>{TODAY}</lastmod>")
            out.append("    <changefreq>monthly</changefreq>")
            out.append(f"    <priority>{'0.7' if lang == 'de' else ' 0.5'.strip()}</priority>")
            out.append(f'    <xhtml:link rel="alternate" hreflang="de" href="{SITE}/{a["slug_de"]}"/>')
            out.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{SITE}/en/{a["slug_en"]}"/>')
            out.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}/{a["slug_de"]}"/>')
            out.append("  </url>")
    for loc in ("/impressum.html", "/datenschutz.html", "/agb.html"):
        out.append("  <url>")
        out.append(f"    <loc>{SITE}{loc}</loc>")
        out.append(f"    <lastmod>{TODAY}</lastmod>")
        out.append("    <changefreq>yearly</changefreq>")
        out.append("    <priority>0.3</priority>")
        out.append("  </url>")
    out.append("</urlset>")
    return "\n".join(out) + "\n"


def main():
    from articles import ARTICLES

    os.makedirs(os.path.join(ROOT, "en"), exist_ok=True)
    for a in ARTICLES:
        with open(os.path.join(ROOT, a["slug_de"]), "w", encoding="utf-8") as f:
            f.write(article_html(a, "de"))
        with open(os.path.join(ROOT, "en", a["slug_en"]), "w", encoding="utf-8") as f:
            f.write(article_html(a, "en"))

    with open(os.path.join(ROOT, "blog.html"), "w", encoding="utf-8") as f:
        f.write(blog_index(ARTICLES, "de"))
    with open(os.path.join(ROOT, "en", "blog.html"), "w", encoding="utf-8") as f:
        f.write(blog_index(ARTICLES, "en"))
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap(ARTICLES))

    print(f"{len(ARTICLES)} Artikel x 2 Sprachen + 2 Übersichten + sitemap.xml erzeugt.")


if __name__ == "__main__":
    main()
