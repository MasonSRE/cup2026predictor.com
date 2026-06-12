#!/usr/bin/env python3
"""Brand the upstream ai-worldcup-2026 static site for cup2026predictor.com."""
from __future__ import annotations

from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"
DOMAIN = "https://cup2026predictor.com"
SITE = "Cup 2026 Predictor"
DESC = (
    "Run AI-powered 2026 World Cup predictions with champion probabilities, "
    "match score forecasts, group-stage odds, bracket simulations, and winner chances."
)


def patch_index() -> None:
    p = WEB / "index.html"
    s = p.read_text(encoding="utf-8")
    head_start = s.index("<title>")
    head_end = s.index('<link rel="preconnect"', head_start)
    new_head = f'''<title>2026 World Cup Predictions & AI Predictor | Cup 2026 Predictor</title>
<meta name="description" content="{html.escape(DESC)}">
<meta name="keywords" content="2026 World Cup predictions, World Cup predictor 2026, World Cup 2026 simulator, World Cup bracket predictor, World Cup winner odds, World Cup score predictions">
<link rel="canonical" href="{DOMAIN}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE}">
<meta property="og:title" content="2026 World Cup Predictions & AI Predictor">
<meta property="og:description" content="{html.escape(DESC)}">
<meta property="og:url" content="{DOMAIN}/">
<meta property="og:image" content="{DOMAIN}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="2026 World Cup Predictions & AI Predictor">
<meta name="twitter:description" content="{html.escape(DESC)}">
<meta name="twitter:image" content="{DOMAIN}/og-image.png">
<link rel="icon" type="image/png" sizes="64x64" href="favicon.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<script type="application/ld+json">
{{"@context":"https://schema.org","@graph":[
 {{"@type":"WebSite","name":"{SITE}","alternateName":"cup2026predictor.com",
  "url":"{DOMAIN}/","inLanguage":"en-US",
  "description":"{DESC}",
  "potentialAction":{{"@type":"SearchAction","target":"{DOMAIN}/?team={{search_term_string}}","query-input":"required name=search_term_string"}}}},
 {{"@type":"SportsEvent","name":"2026 FIFA World Cup","alternateName":"World Cup 2026",
  "startDate":"2026-06-11","endDate":"2026-07-19","eventStatus":"https://schema.org/EventScheduled",
  "location":[{{"@type":"Country","name":"United States"}},{{"@type":"Country","name":"Canada"}},{{"@type":"Country","name":"Mexico"}}],
  "organizer":{{"@type":"Organization","name":"FIFA","url":"https://www.fifa.com"}}}}
]}}
</script>
'''
    s = s[:head_start] + new_head + s[head_end:]

    replacements = {
        "AI 世界杯预测 2026：本站用 AI 对美加墨世界杯进行数亿次模拟，提供 48 强实时夺冠概率、\n    104 场逐场比分预测与博彩盘口对照、小组出线形势、每日 AI 战报与预测战绩追踪，\n    每场比赛结束后自动更新。请启用 JavaScript 查看完整交互内容。":
        "Cup 2026 Predictor runs AI-powered World Cup 2026 simulations with champion probabilities, match score predictions, group-stage odds, bracket paths, and prediction tracking. Enable JavaScript to view the full interactive predictor.",
        "<span class=\"kicker\">Daily Update · Live</span>": "<span class=\"kicker\">World Cup 2026 · AI Predictor</span>",
        "<h1>AI 世界杯预测 <span class=\"accent\">2026</span></h1>": "<h1>Cup <span class=\"accent\">2026</span> Predictor</h1>",
        "<p class=\"sub\">谁能捧起大力神杯？我们让 AI 把这届世界杯提前\"踢\"了上亿遍。每天根据最新战况重新计算，整个赛事期间持续更新。</p>":
        "<p class=\"sub\">Explore 2026 World Cup predictions powered by Elo ratings, score models, odds signals, and Monte Carlo simulations. Track winner chances, match forecasts, group scenarios, and bracket paths throughout the tournament.</p>",
        "<div class=\"sec-head\"><span class=\"sec-no\">01</span><h2>夺冠概率榜</h2><div class=\"rule\"></div></div>":
        "<div class=\"sec-head\"><span class=\"sec-no\">01</span><h2>World Cup 2026 Winner Predictions</h2><div class=\"rule\"></div></div>",
        "<div class=\"sec-head\"><span class=\"sec-no\">02</span><h2>夺冠概率走势</h2><div class=\"rule\"></div><span class=\"sec-note\">每日更新累积</span></div>":
        "<div class=\"sec-head\"><span class=\"sec-no\">02</span><h2>Champion Probability Trend</h2><div class=\"rule\"></div><span class=\"sec-note\">updated after each match window</span></div>",
        "<div class=\"sec-head\"><span class=\"sec-no\">04</span><h2>赛程 · 比分 · 预测</h2><div class=\"rule\"></div></div>":
        "<div class=\"sec-head\"><span class=\"sec-no\">04</span><h2>Match Schedule · Score Predictions</h2><div class=\"rule\"></div></div>",
        "<div class=\"sec-head\"><span class=\"sec-no\">07</span><h2>AI 战报</h2><div class=\"rule\"></div><span class=\"sec-note\">随赛况更新 · 全部存档</span></div>":
        "<div class=\"sec-head\"><span class=\"sec-no\">07</span><h2>AI Match Reports</h2><div class=\"rule\"></div><span class=\"sec-note\">updated as results arrive</span></div>",
        "<div class=\"sec-head\"><span class=\"sec-no\">06</span><h2>预测战绩</h2><div class=\"rule\"></div><span class=\"sec-note\">所有预测都在比赛前生成</span></div>":
        "<div class=\"sec-head\"><span class=\"sec-no\">06</span><h2>Prediction Record</h2><div class=\"rule\"></div><span class=\"sec-note\">all picks are locked before kickoff</span></div>",
        "未找到 data.js — 请先运行: python3 -m src.update": "Missing data.js — run: ./scripts/python -m src.update",
        "博彩盘口 <b>已融合</b>": "Market odds <b>blended</b>",
        "胜负预测命中": "Outcome accuracy",
        "更新于": "Updated",
        "预测仅供娱乐，足球是圆的 ⚽": "For entertainment only — not betting advice ⚽",
        "const TABS = [[\"overview\",\"总览\"],[\"schedule\",\"赛程·预测\"],[\"groups\",\"小组形势\"],[\"reports\",\"AI 战报\"],[\"record\",\"预测战绩\"]];":
        "const TABS = [[\"overview\",\"Overview\"],[\"schedule\",\"Predictions\"],[\"groups\",\"Groups\"],[\"reports\",\"Reports\"],[\"record\",\"Record\"]];",
    }
    for old, new in replacements.items():
        s = s.replace(old, new)

    # Add SEO jump links after meta chips if not already present.
    marker = '<div class="meta-chips" id="meta-chips"></div>'
    links = f'''<div class="meta-chips seo-links" aria-label="Key predictor pages">
      <a class="chip" href="/predictor/">World Cup Predictor 2026</a>
      <a class="chip" href="/simulator/">World Cup 2026 Simulator</a>
      <a class="chip" href="/bracket-predictor/">Bracket Predictor</a>
      <a class="chip" href="/winner-predictions/">Winner Predictions</a>
      <a class="chip" href="/groups/">Group Predictions</a>
      <a class="chip" href="/teams/argentina/">Argentina Prediction</a>
    </div>'''
    if 'class="meta-chips seo-links"' not in s:
        s = s.replace(marker, marker + "\n    " + links)

    # Make .chip links look like chips.
    css_marker = "  .chip { font-family: var(--mono); font-size: 12px; color: var(--dim);\n    border: 1px solid var(--line); background: rgba(12,24,17,.6); padding: 7px 13px; border-radius: 2px; }"
    css_add = css_marker + "\n  a.chip { text-decoration: none; display: inline-flex; }\n  a.chip:hover { color: var(--lime); border-color: var(--lime); }"
    s = s.replace(css_marker, css_add)

    p.write_text(s, encoding="utf-8")


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang=\"en\">
<head>
<meta charset=\"UTF-8\">
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
<title>{title}</title>
<meta name=\"description\" content=\"{description}\">
<link rel=\"canonical\" href=\"{canonical}\">
<meta property=\"og:type\" content=\"website\">
<meta property=\"og:site_name\" content=\"Cup 2026 Predictor\">
<meta property=\"og:title\" content=\"{title}\">
<meta property=\"og:description\" content=\"{description}\">
<meta property=\"og:url\" content=\"{canonical}\">
<meta property=\"og:image\" content=\"https://cup2026predictor.com/og-image.png\">
<link rel=\"icon\" type=\"image/png\" href=\"/favicon.png\">
<link rel=\"stylesheet\" href=\"/landing.css\">
<script type=\"application/ld+json\">{schema}</script>
</head>
<body>
<main class=\"wrap\">
  <a class=\"brand\" href=\"/\">Cup 2026 Predictor</a>
  <section class=\"hero\">
    <p class=\"eyebrow\">World Cup 2026 prediction tool</p>
    <h1>{h1}</h1>
    <p class=\"lede\">{lede}</p>
    <div class=\"actions\">
      <a class=\"button primary\" href=\"/\">Open the live predictor</a>
      <a class=\"button\" href=\"/simulator/\">Run tournament simulator</a>
    </div>
  </section>
  <section class=\"grid\">{cards}</section>
  <section class=\"content\">{body}</section>
  <nav class=\"links\">
    <a href=\"/predictor/\">Predictor</a>
    <a href=\"/simulator/\">Simulator</a>
    <a href=\"/bracket-predictor/\">Bracket predictor</a>
    <a href=\"/winner-predictions/\">Winner predictions</a>
    <a href=\"/groups/\">Groups</a>
    <a href=\"/teams/argentina/\">Teams</a>
  </nav>
  <p class=\"fine\">Predictions are for information and entertainment only. They are not betting advice.</p>
</main>
</body>
</html>
"""

LANDING_CSS = """
:root{--bg:#07100b;--panel:#0c1811;--line:rgba(214,255,222,.15);--ink:#eaf6ec;--dim:#91aa98;--lime:#b8f53d;--gold:#ffd75e;--hot:#ff7a52}*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 80% 0,rgba(184,245,61,.13),transparent 34%),var(--bg);color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;line-height:1.65}.wrap{max-width:1040px;margin:0 auto;padding:36px 22px 80px}.brand{color:var(--lime);text-decoration:none;font-weight:800;letter-spacing:.08em;text-transform:uppercase;font-size:13px}.hero{padding:70px 0 44px}.eyebrow{color:var(--lime);font-size:13px;letter-spacing:.22em;text-transform:uppercase}h1{font-size:clamp(42px,8vw,78px);line-height:1.02;margin:12px 0 18px;max-width:900px}.lede{font-size:19px;color:var(--dim);max-width:760px}.actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:28px}.button{border:1px solid var(--line);color:var(--ink);text-decoration:none;padding:12px 18px;border-radius:8px}.button.primary{background:var(--lime);color:#07100b;border-color:var(--lime);font-weight:800}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:20px 0 42px}.card,.content{border:1px solid var(--line);background:rgba(12,24,17,.76);border-radius:14px;padding:20px}.card b{display:block;color:var(--gold);font-size:22px;margin-bottom:6px}.card span{color:var(--dim);font-size:14px}.content h2{font-size:28px;margin:8px 0 12px}.content h3{margin-top:28px}.content p,.content li{color:var(--dim)}.links{display:flex;gap:10px;flex-wrap:wrap;margin-top:28px}.links a{color:var(--lime);border:1px solid var(--line);padding:8px 12px;border-radius:999px;text-decoration:none;font-size:14px}.fine{color:#6f8274;font-size:13px;margin-top:28px}@media(max-width:760px){.grid{grid-template-columns:1fr}h1{font-size:42px}}
"""


def make_page(slug: str, title: str, description: str, h1: str, lede: str, cards: list[tuple[str, str]], body: str) -> None:
    d = WEB / slug
    d.mkdir(parents=True, exist_ok=True)
    canonical = f"{DOMAIN}/{slug}/"
    schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "url": canonical,
        "description": description,
        "isPartOf": {"@type": "WebSite", "name": SITE, "url": DOMAIN + "/"},
    }, ensure_ascii=False)
    html_text = PAGE_TEMPLATE.format(
        title=html.escape(title), description=html.escape(description), canonical=canonical,
        h1=html.escape(h1), lede=html.escape(lede),
        cards="\n".join(f'<article class="card"><b>{html.escape(k)}</b><span>{html.escape(v)}</span></article>' for k, v in cards),
        body=body, schema=html.escape(schema, quote=False)
    )
    (d / "index.html").write_text(html_text, encoding="utf-8")


def generate_pages() -> None:
    (WEB / "landing.css").write_text(LANDING_CSS.strip() + "\n", encoding="utf-8")
    pages = [
        ("predictor", "World Cup Predictor 2026 | Cup 2026 Predictor", "Use a 2026 World Cup predictor with AI-powered winner chances, match forecasts, group-stage probabilities, and bracket paths.", "World Cup Predictor 2026", "Pick a team, compare match probabilities, and follow AI-updated predictions for the 2026 World Cup.", [("48 teams", "Group and knockout paths"), ("104 matches", "Score and outcome forecasts"), ("Live record", "Pre-kickoff picks tracked")], "<h2>What the predictor does</h2><p>The predictor combines Elo ratings, score distributions, market signals where available, and Monte Carlo tournament simulations. It is built for searchers looking for 2026 World Cup predictions, winner chances, and match score forecasts.</p>"),
        ("simulator", "World Cup 2026 Simulator | Monte Carlo Tournament Predictions", "Simulate the 2026 World Cup bracket and group stage with AI-powered Monte Carlo projections and champion probabilities.", "World Cup 2026 Simulator", "Run tournament simulations to estimate every team's path from the group stage to the final.", [("Monte Carlo", "Tournament-level simulations"), ("Bracket paths", "Round-of-32 to final"), ("Winner odds", "Champion probability table")], "<h2>Built for tournament scenarios</h2><p>The simulator locks completed results, updates Elo after matches, and replays the remaining tournament to estimate qualification, knockout, finalist, and champion probabilities.</p>"),
        ("bracket-predictor", "World Cup 2026 Bracket Predictor | Projected Knockout Bracket", "Explore a World Cup 2026 bracket predictor with projected knockout paths, round probabilities, and likely finals.", "World Cup 2026 Bracket Predictor", "Project the Round of 32, knockout paths, likely finals, and champion chances from current simulation data.", [("Round of 32", "Official 48-team format"), ("Likely finals", "Most common simulated pairings"), ("Knockout mode", "Extra time and penalties modeled")], "<h2>Bracket prediction approach</h2><p>The bracket predictor follows the official 2026 structure: 12 groups, best third-place teams, Round of 32 slots, then the fixed knockout tree through the final.</p>"),
        ("winner-predictions", "World Cup 2026 Winner Predictions | Champion Chances", "See World Cup 2026 winner predictions, champion probabilities, favorites, dark horses, and AI-updated title chances.", "World Cup 2026 Winner Predictions", "Compare the favorites, dark horses, and daily champion probability movement for the 2026 World Cup.", [("Favorites", "Spain, Argentina, France and more"), ("Dark horses", "Probability jumps after results"), ("Daily updates", "Fresh simulations after match windows")], "<h2>Champion probability, not hype</h2><p>Winner predictions are generated from tournament simulations rather than editorial picks. Use them to compare contenders and track how each result changes the title race.</p>"),
        ("groups", "World Cup 2026 Group Predictions | Group Stage Odds", "Check World Cup 2026 group predictions, qualification odds, group winner chances, and best third-place scenarios.", "World Cup 2026 Group Predictions", "Follow group-stage projections for all 12 groups, including qualification and group winner scenarios.", [("12 groups", "48-team expanded format"), ("Top two", "Automatic qualification paths"), ("Best thirds", "Third-place race modeled")], "<h2>Group-stage prediction coverage</h2><p>Each group page can be expanded into qualification probability, match schedule, points scenarios, and likely knockout opponents.</p>"),
    ]
    for args in pages:
        make_page(*args)

    teams = {
        "argentina": ("Argentina World Cup 2026 Prediction", "Argentina World Cup 2026 prediction with champion chances, group outlook, match forecasts, and projected bracket path.", "Argentina World Cup 2026 Prediction", "Track Argentina's 2026 World Cup winner chances, match projections, and likely path through the bracket."),
        "spain": ("Spain World Cup 2026 Prediction", "Spain World Cup 2026 prediction with champion probability, score forecasts, and projected knockout path.", "Spain World Cup 2026 Prediction", "Follow Spain's title probability, expected matchups, and simulated path to the 2026 World Cup final."),
        "brazil": ("Brazil World Cup 2026 Prediction", "Brazil World Cup 2026 prediction with winner chances, group outlook, and knockout path projections.", "Brazil World Cup 2026 Prediction", "See Brazil's current champion chances and tournament path from the AI simulation model."),
        "england": ("England World Cup 2026 Prediction", "England World Cup 2026 prediction with winner odds, score forecasts, and bracket projections.", "England World Cup 2026 Prediction", "Compare England's World Cup 2026 chances across group, knockout, finalist, and champion probabilities."),
        "usa": ("USA World Cup 2026 Prediction", "United States World Cup 2026 prediction with host boost, match forecasts, and group-stage odds.", "USA World Cup 2026 Prediction", "Track the United States as a 2026 host with group-stage odds, match predictions, and knockout chances."),
        "mexico": ("Mexico World Cup 2026 Prediction", "Mexico World Cup 2026 prediction with host boost, winner chances, and group-stage projections.", "Mexico World Cup 2026 Prediction", "Follow Mexico's host-nation path, group predictions, and simulated knockout chances."),
    }
    for slug, (title, desc, h1, lede) in teams.items():
        make_page(f"teams/{slug}", title + " | Cup 2026 Predictor", desc, h1, lede, [("Team chances", "Qualification to champion"), ("Match forecasts", "Score probabilities"), ("Bracket path", "Projected opponents")], "<h2>Team prediction page</h2><p>This page is designed to rank for team-specific World Cup 2026 prediction searches while sending users into the live predictor for updated probabilities.</p>")


def update_sitemap_and_robots() -> None:
    urls = ["/"] + [
        "/predictor/", "/simulator/", "/bracket-predictor/", "/winner-predictions/", "/groups/",
        "/teams/argentina/", "/teams/spain/", "/teams/brazil/", "/teams/england/", "/teams/usa/", "/teams/mexico/",
    ]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        pr = "1.0" if u == "/" else "0.8"
        xml.append(f"  <url><loc>{DOMAIN}{u}</loc><lastmod>2026-06-12</lastmod><changefreq>daily</changefreq><priority>{pr}</priority></url>")
    xml.append("</urlset>")
    (WEB / "sitemap.xml").write_text("\n".join(xml) + "\n", encoding="utf-8")
    (WEB / "robots.txt").write_text(f"""User-agent: *
Allow: /
Disallow: /data.js
Disallow: /reports.js
Disallow: /blurbs.js

Sitemap: {DOMAIN}/sitemap.xml
""", encoding="utf-8")


def main() -> None:
    patch_index()
    generate_pages()
    update_sitemap_and_robots()


if __name__ == "__main__":
    main()
