# Cup 2026 Predictor

AI-powered 2026 World Cup prediction, simulator, bracket, and winner-chance site for:

- <https://cup2026predictor.com>

This project is a second-development fork of [`vastxie/ai-worldcup-2026`](https://github.com/vastxie/ai-worldcup-2026), repositioned as an English SEO/tool site around:

- `2026 world cup predictions`
- `world cup predictor 2026`
- `world cup 2026 simulator`
- `world cup 2026 bracket predictor`
- `world cup 2026 winner prediction`

## What it does

The prediction engine models the 2026 FIFA World Cup with:

1. Dynamic Elo ratings.
2. Expected goals and score distributions.
3. Dixon-Coles low-score correction.
4. Host-country Elo boost for United States, Canada, and Mexico.
5. Optional market-odds blending.
6. Conditional Monte Carlo simulations for group and knockout paths.
7. Pre-kickoff prediction record tracking.

The static website provides:

- Champion probability table.
- Match schedule and score predictions.
- Group-stage qualification outlook.
- AI match reports.
- Prediction performance record.
- SEO landing pages for predictor/simulator/bracket/winner/team searches.

## Quick start

Use Python 3.11. On this Mac, system `python3` may be Python 3.9, so use the included wrapper:

```bash
./scripts/python --version
./scripts/python -m src.predict match Spain Argentina --knockout
./scripts/python -m src.predict simulate --sims 1000 --seed 42
```

Preview the static site:

```bash
./scripts/python -m http.server 8642 --directory web
```

Open <http://localhost:8642>.

## Regenerate SEO pages

```bash
./scripts/python scripts/brand_seo_transform.py
./scripts/python scripts/seo_check.py
```

## Data sources

The upstream project credits:

- Elo baseline: eloratings.net
- Schedule and scores: fixturedownload.com
- Historical results: martj42/international_results
- Optional market odds: the-odds-api.com

## Disclaimer

Predictions are for information and entertainment only. They are not betting advice.

## License

MIT, following the upstream project license.
