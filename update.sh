#!/usr/bin/env bash
# 更新：同步比分 → 更新 Elo → 重算预测 → 刷新网站数据（macOS / Linux 通用）
cd "$(dirname "$0")"
python3 -m src.update "$@"
