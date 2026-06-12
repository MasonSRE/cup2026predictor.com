# Cup 2026 Predictor Development

Domain: `cup2026predictor.com`

This project is a second-development fork of `vastxie/ai-worldcup-2026`, repositioned as an English SEO/tool site for:

- `2026 world cup predictions`
- `world cup predictor 2026`
- `world cup 2026 simulator`
- `world cup 2026 bracket predictor`
- `world cup 2026 winner prediction`

## Python

Use Python 3.11. The macOS system `python3` may be Python 3.9 and will fail on ISO timestamps ending in `Z`.

```bash
./scripts/python --version
./scripts/python -m src.predict match Spain Argentina --knockout
./scripts/python -m src.predict simulate --sims 1000 --seed 42
```

## Regenerate web data

```bash
./scripts/python -m src.predict simulate --sims 20000
```

Generated files such as `web/data.js`, `web/reports.js`, `web/blurbs.js`, and `out/` are ignored by git.

## Branding / SEO transform

```bash
./scripts/python scripts/brand_seo_transform.py
```

This maintains the Cup 2026 Predictor branding, static SEO landing pages, `robots.txt`, and `sitemap.xml`.

## Static preview

```bash
./scripts/python -m http.server 8642 --directory web
```

Open <http://localhost:8642>.

## Disclaimer

Predictions are for information and entertainment only. They are not betting advice.
