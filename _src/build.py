#!/usr/bin/env python3
"""Assemble the static pages from _src/pages/*.html plus the shared layout.

Run from the repo root:  python3 _src/build.py
Output files are written to the repo root, where GitHub Pages serves them.
"""
from pathlib import Path
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
    ("about.html", "about", f"About | {SITE}",
     "Premier Landscape Management LLC is an owner-run Phoenix landscape contractor led by Jose Gonzalez. Arizona ROC 355147."),
    ("walkthrough.html", "walkthrough", f"Request a property walkthrough | {SITE}",
     "Request a walkthrough of your HOA or commercial property in Phoenix. We walk the grounds with you and send a written proposal."),
]

LOGO = (
    '<svg class="logo-svg" viewBox="18.7 10.5 984.6 262.8" aria-hidden="true" focusable="false">'
    + "".join(f'<path class="lt" d="{d}"/>' for d in TEXT)
    + f'<path class="ld" d="{DARK}"/><path class="lg" d="{GREEN}"/></svg>'
)

NAV = [
    ("services.html", "services", "Services"),
    ("who-we-serve.html", "serve", "Who we serve"),
    ("how-we-work.html", "work", "How we work"),
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
<link rel="stylesheet" href="css/site.css">
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
      <a class="btn btn-ink" href="walkthrough.html"{wt_current}>Request a walkthrough</a>
    </nav>
  </div>
</header>

<main id="main">
{body}
</main>

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

<script src="js/site.js"></script>
</body>
</html>
"""


def build():
    for fname, key, title, desc in PAGE_LIST:
        body = (PAGES / fname).read_text(encoding="utf-8").strip("\n")
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
            wt_current=' aria-current="page"' if key == "walkthrough" else "",
        )
        (ROOT / fname).write_text(html, encoding="utf-8")
        print("built", fname)


if __name__ == "__main__":
    build()
