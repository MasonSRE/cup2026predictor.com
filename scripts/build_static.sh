#!/usr/bin/env bash
set -euo pipefail
SIMS="${SIMS:-20000}"
SEED="${SEED:-20260612}"

echo "[build] generating Cup 2026 Predictor data with SIMS=$SIMS SEED=$SEED"
./scripts/python -m src.predict simulate --sims "$SIMS" --seed "$SEED"

echo "[build] generating English SEO pages"
./scripts/python scripts/brand_seo_transform.py

echo "[build] generating OG image and icons"
./scripts/python scripts/generate_assets.py

echo "[build] running SEO/static checks"
./scripts/python scripts/seo_check.py

echo "[build] complete. Publish directory: web"
