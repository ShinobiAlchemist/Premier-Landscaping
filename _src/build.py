#!/usr/bin/env python3
"""Assemble the static pages from _src/pages/*.html plus the shared layout.

Run from the repo root:  python3 _src/build.py
Output files are written to the repo root, where GitHub Pages serves them.
"""
from pathlib import Path
import html as _html
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from logo_paths import TEXT, DARK, GREEN  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "_src" / "pages"

SITE = "Premier Landscape Management"

PAGE_LIST = [
    # file, nav key, title, description
    ("index.html", "home", f"{SITE} | Commercial and HOA landscaping in Phoenix",
     "Owner-run commercial and HOA landscape maintenance in Phoenix, Arizona. Monthly walkthroughs, written reports and crews who know your property. ROC 355147."),
    ("services.html", "services", f"Services | {SITE}",
     "Grounds maintenance, irrigation and water management, tree and palm care, enhancements and monsoon response for Phoenix commercial properties and HOAs."),
    ("who-we-serve.html", "serve", f"Who we serve | {SITE}",
     "Landscape management for HOA communities, office and business parks, retail centers and multifamily properties across the Phoenix metro."),
    ("how-we-work.html", "work", f"How we work | {SITE}",
     "How Premier Landscape Management starts and runs a contract: walkthrough, written proposal, property plan, monthly walkthroughs and the Phoenix seasonal calendar."),
    ("tools.html", "tools", f"Manager tools | {SITE}",
     "Free tools for Phoenix HOA boards and property managers: vendor documents, a landscape bid comparison sheet and a resident notice generator."),
    ("vendor-documents.html", "tools", f"Vendor documents | {SITE}",
     "Download Premier Landscape Management's W-9, certificate of insurance and Arizona ROC license, or request a certificate naming your association."),
    ("compare-bids.html", "tools", f"Landscape bid comparison sheet | {SITE}",
     "A printable checklist for comparing commercial and HOA landscape bids on the same terms."),
    ("resident-notices.html", "tools", f"Resident notice generator | {SITE}",
     "Create printable English and Spanish notices for overseeding, tree trimming, weed treatment and irrigation repairs."),
    ("about.html", "about", f"About | {SITE}",
     "Premier Landscape Management LLC is an owner-run Phoenix landscape contractor led by Jose Gonzalez. Arizona ROC 355147."),
    ("request-proposal.html", "proposal", f"Request a proposal | {SITE}",
     "Request a landscape maintenance proposal for your HOA or commercial property in Phoenix. We walk the grounds with you and send a written proposal."),
]

LOGO = (
    '<svg class="logo-svg" viewBox="18.7 10.5 984.6 262.8" aria-hidden="true" focusable="false">'
    + "".join(f'<path class="lt" d="{d}"/>' for d in TEXT)
    + f'<path class="ld" d="{DARK}"/><path class="lg" d="{GREEN}"/></svg>'
)

TERMS = {
    "overseed": ("Overseed", "Spreading ryegrass seed over dormant bermuda in fall, so the turf stays green through winter."),
    "scalp": ("Scalp", "Mowing bermuda very short in September, so new ryegrass seed can reach the soil."),
    "preemergent": ("Pre-emergent", "A weed treatment applied before weed seeds sprout. It keeps them from starting to grow."),
    "bermuda": ("Bermuda", "The warm-season grass on most Phoenix turf. It grows through summer and turns brown and dormant in winter."),
    "drip": ("Drip irrigation", "Small tubes and emitters that deliver water slowly to each plant's roots. Used for shrubs, trees and beds."),
    "natural": ("Natural-form pruning", "Pruning that keeps a plant's own shape by removing selected branches at their base."),
    "structural": ("Structural pruning", "Pruning that builds a strong trunk and well-spaced branches, so the tree holds up in wind."),
    "monsoon": ("Monsoon", "Arizona's summer storm season, June 15 to September 30, with high winds, dust storms and heavy rain."),
    "transition": ("Transition", "The late-spring period when winter ryegrass dies back in the heat and bermuda grows in again."),
}

GLOSSARY = "\n".join(
    f'<div class="def" id="def-{k}" popover><b>{t}</b>{d}</div>' for k, (t, d) in TERMS.items()
)

WEATHER = """    <div class="wx" id="wx" hidden aria-label="Current weather in Phoenix">
      <span id="wx-icon" aria-hidden="true"></span>
      <span><b id="wx-temp"></b> <span class="cond" id="wx-cond"></span><small>Phoenix, Sky Harbor</small></span>
    </div>"""

NAV = [
    ("services.html", "services", "Services"),
    ("who-we-serve.html", "serve", "Who we serve"),
    ("how-we-work.html", "work", "How we work"),
    ("tools.html", "tools", "Manager tools"),
    ("about.html", "about", "About"),
]

SCHEMA = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LandscapingBusiness",
  "name": "Premier Landscape Management LLC",
  "alternateName": "Premier Landscape Management Phoenix",
  "url": "https://www.premier-lm.com/",
  "founder": {"@type": "Person", "name": "Jose Gonzalez"},
  "areaServed": {"@type": "City", "name": "Phoenix", "containedInPlace": {"@type": "State", "name": "Arizona"}},
  "address": {"@type": "PostalAddress", "addressLocality": "Phoenix", "addressRegion": "AZ", "addressCountry": "US"},
  "hasCredential": {"@type": "EducationalOccupationalCredential", "credentialCategory": "license", "name": "Arizona Registrar of Contractors license ROC 355147"},
  "knowsAbout": ["Commercial landscape maintenance", "HOA landscaping", "Irrigation management", "Tree and palm care"]
}
</script>"""

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#1e2815">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/montserrat.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/site.css?v={ver}">
{schema}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<div class="review-bar" role="region" aria-label="Review notes">
  <div class="wrap">
    <p><b>Review draft.</b> Highlighted text is a placeholder or still needs Jose's confirmation before launch.</p>
    <button type="button" data-toggle-review>Hide highlights</button>
  </div>
</div>

<header class="site-header">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="Premier Landscape Management, home">{logo}</a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav class="nav" id="site-nav" aria-label="Main">
      <ul>
{nav}
      </ul>
      <a class="btn btn-ink" href="request-proposal.html"{wt_current}>Request a proposal</a>
    </nav>
{weather}
  </div>
</header>

<div class="alert-bar" id="alert-bar" role="status" hidden><div class="wrap"><p id="alert-text"></p></div></div>

<main id="main">
<div class="rail" aria-hidden="true"></div>
{body}
</main>

{glossary}

<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="logo" href="index.html" aria-label="Premier Landscape Management, home">{logo}</a>
        <p style="margin-top:1.25rem">Commercial and HOA landscape management across the Phoenix metro, run by owner Jose Gonzalez.</p>
      </div>
      <div>
        <h2>Services</h2>
        <ul>
          <li><a href="services.html#maintenance">Grounds maintenance</a></li>
          <li><a href="services.html#irrigation">Irrigation and water</a></li>
          <li><a href="services.html#trees">Tree and palm care</a></li>
          <li><a href="services.html#enhancements">Enhancements</a></li>
          <li><a href="services.html#monsoon">Monsoon response</a></li>
        </ul>
      </div>
      <div>
        <h2>Company</h2>
        <ul>
          <li><a href="who-we-serve.html">Who we serve</a></li>
          <li><a href="how-we-work.html">How we work</a></li>
          <li><a href="how-we-work.html#calendar">Seasonal calendar</a></li>
          <li><a href="about.html">About Jose and the crew</a></li>
          <li><a href="vendor-documents.html">Vendor documents</a></li>
          <li><a href="compare-bids.html">Bid comparison sheet</a></li>
          <li><a href="resident-notices.html">Resident notices</a></li>
        </ul>
      </div>
      <div>
        <h2>Contact</h2>
        <ul>
          <li><a href="tel:+16020000000"><span class="tbd">(602) 000-0000</span></a></li>
          <li><a href="mailto:info@premier-lm.com"><span class="tbd">info@premier-lm.com</span></a></li>
          <li><span class="tbd">Mon to Fri, 6 a.m. to 4 p.m.</span></li>
          <li>Serving the Phoenix metro</li>
        </ul>
      </div>
    </div>
    <div class="footer-base">
      <p>&copy; <span id="year">2026</span> Premier Landscape Management LLC</p>
      <p>Arizona ROC 355147. Licensed, <span class="tbd">bonded and insured</span>.</p>
    </div>
  </div>
</footer>

<script src="js/site.js?v={ver}"></script>
</body>
</html>
"""


PHOTO_RE = re.compile(r"\[\[photo (\S+) (std|tall|wide) \| ([^\]]+)\]\]")
TERM_RE = re.compile(r"\[\[term (\w+)\|([^\]]+)\]\]")


def photo(m):
    pid, size, alt = m.group(1), m.group(2), m.group(3).strip()
    cls = "photo" if size == "std" else f"photo {size}"
    w = 900 if size == "std" else 1400
    src = f"https://images.unsplash.com/photo-{pid}?w={w}&q=70&auto=format&fit=crop"
    alt = _html.escape(alt, quote=True)
    return (f'<figure class="{cls}"><img src="{src}" alt="{alt}" loading="lazy" decoding="async">'
            '<figcaption>Stand-in photo</figcaption></figure>')


def term(m):
    key, text = m.group(1), m.group(2)
    assert key in TERMS, key
    return f'<button type="button" class="term" popovertarget="def-{key}">{text}</button>'


def expand(body):
    return TERM_RE.sub(term, PHOTO_RE.sub(photo, body))


import time
VER = str(int(time.time()))


def build():
    for fname, key, title, desc in PAGE_LIST:
        body = (PAGES / fname).read_text(encoding="utf-8").strip("\n")
        body = expand(body)
        assert "[[" not in body, fname
        nav = "\n".join(
            f'        <li><a href="{href}"{" aria-current=\"page\"" if k == key else ""}>{label}</a></li>'
            for href, k, label in NAV
        )
        html = TEMPLATE.format(
            title=title,
            desc=desc,
            nav=nav,
            body=body,
            schema=SCHEMA if key == "home" else "",
            logo=LOGO,
            glossary=GLOSSARY,
            ver=VER,
            weather=WEATHER if key == "home" else "",
            wt_current=' aria-current="page"' if key == "proposal" else "",
        )
        (ROOT / fname).write_text(html, encoding="utf-8")
        print("built", fname)


if __name__ == "__main__":
    build()
