# Premier Landscape Management website (review build)

Static site for Premier Landscape Management LLC, a commercial and HOA landscaping company in Phoenix, Arizona (ROC 355147). Hosted on GitHub Pages for owner review.

## Editing

Page content lives in `_src/pages/`. The shared header, footer and page titles live in `_src/build.py`. After editing, rebuild the root HTML files:

```
python3 _src/build.py
```

Styles are in `css/site.css`, scripts in `js/site.js`, and self-hosted fonts (Archivo, Newsreader) in `assets/fonts/`.

## Review markers

Text wrapped in `<span class="tbd">` is highlighted on the site as a placeholder or an item that needs confirmation. Dark striped boxes marked "Photo needed" are image slots with a shot description. Search for `tbd` and `photo` to find them all before launch.

## Before launch

- Replace phone, email, hours, years in business and insurance details
- Replace photo slots with real photos of Premier crews and properties
- Have Jose review and edit his letter and bio
- Connect the walkthrough form (for example Formspree or the hosting platform's form handler)
- Remove `<meta name="robots" content="noindex">` and the review banner from `_src/build.py`
