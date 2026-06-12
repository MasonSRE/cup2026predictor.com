#!/usr/bin/env python3
"""Generate the English Cup 2026 Predictor static frontend and SEO pages."""
from __future__ import annotations

from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"
DOMAIN = "https://cup2026predictor.com"
SITE = "Cup 2026 Predictor"
DESC = "AI-powered 2026 World Cup predictions, match forecasts, bracket simulations, group odds, and winner chances."
TEAM_SLUGS = ["argentina", "spain", "brazil", "england", "usa", "mexico", "france", "germany", "portugal", "netherlands"]

COUNTRY_SLUG = {
    "Argentina": "argentina", "Spain": "spain", "Brazil": "brazil", "England": "england", "United States": "usa",
    "Mexico": "mexico", "France": "france", "Germany": "germany", "Portugal": "portugal", "Netherlands": "netherlands",
    "Canada": "canada", "Japan": "japan", "Colombia": "colombia", "Uruguay": "uruguay", "Croatia": "croatia",
}

INDEX_HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="theme-color" content="#07100b">
<title>2026 World Cup Predictions & AI Predictor | Cup 2026 Predictor</title>
<meta name="description" content="AI-powered 2026 World Cup predictions with champion probabilities, match score forecasts, group-stage odds, bracket simulations, and winner chances.">
<meta name="keywords" content="2026 World Cup predictions, World Cup predictor 2026, World Cup 2026 simulator, World Cup bracket predictor, World Cup winner predictions, World Cup score predictions">
<link rel="canonical" href="https://cup2026predictor.com/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Cup 2026 Predictor">
<meta property="og:title" content="2026 World Cup Predictions & AI Predictor">
<meta property="og:description" content="AI-powered 2026 World Cup predictions, match forecasts, bracket simulations, group odds, and winner chances.">
<meta property="og:url" content="https://cup2026predictor.com/">
<meta property="og:image" content="https://cup2026predictor.com/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="2026 World Cup Predictions & AI Predictor">
<meta name="twitter:description" content="AI-powered 2026 World Cup predictions, match forecasts, bracket simulations, group odds, and winner chances.">
<meta name="twitter:image" content="https://cup2026predictor.com/og-image.png">
<link rel="icon" type="image/png" sizes="64x64" href="/favicon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<script type="application/ld+json">{"@context":"https://schema.org","@graph":[{"@type":"WebSite","name":"Cup 2026 Predictor","url":"https://cup2026predictor.com/","inLanguage":"en-US","description":"AI-powered 2026 World Cup predictions, match forecasts, bracket simulations, group odds, and winner chances."},{"@type":"SportsEvent","name":"2026 FIFA World Cup","alternateName":"World Cup 2026","startDate":"2026-06-11","endDate":"2026-07-19","eventStatus":"https://schema.org/EventScheduled","location":[{"@type":"Country","name":"United States"},{"@type":"Country","name":"Canada"},{"@type":"Country","name":"Mexico"}],"organizer":{"@type":"Organization","name":"FIFA","url":"https://www.fifa.com"}}]}</script>
<!-- Privacy-friendly analytics by Plausible -->
<script async src="https://plausible.xiaoyuan.fun/js/pa-WK90PG-0AX8mkAS5xo1rK.js"></script>
<script>
window.plausible=window.plausible||function(){(plausible.q=plausible.q||[]).push(arguments)},plausible.init=plausible.init||function(i){plausible.o=i||{}};
plausible.init()
</script>
<style>
:root{--bg:#07100b;--panel:#0c1811;--panel2:#101f16;--line:rgba(214,255,222,.14);--line2:rgba(214,255,222,.28);--ink:#eaf6ec;--dim:#8ca893;--faint:#5d7564;--lime:#b8f53d;--gold:#ffd75e;--hot:#ff7a52;--blue:#70d6ff;--mono:"IBM Plex Mono",ui-monospace,Menlo,monospace;--body:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}*{box-sizing:border-box}html{background:var(--bg);scroll-behavior:smooth}body{margin:0;background:radial-gradient(900px 420px at 82% -10%,rgba(184,245,61,.16),transparent 62%),radial-gradient(700px 360px at 0 20%,rgba(112,214,255,.09),transparent 60%),var(--bg);color:var(--ink);font-family:var(--body);line-height:1.55}.wrap{max-width:1180px;margin:0 auto;padding:0 24px 100px}.topbar{position:sticky;top:0;z-index:20;background:rgba(7,16,11,.84);backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}.topbar-inner{max-width:1180px;margin:0 auto;padding:14px 24px;display:flex;gap:16px;align-items:center;justify-content:space-between}.brand{color:var(--lime);font-weight:900;letter-spacing:.08em;text-transform:uppercase;text-decoration:none;font-size:13px}.nav{display:flex;gap:6px;overflow:auto}.nav a{color:var(--dim);text-decoration:none;font-family:var(--mono);font-size:12px;padding:8px 10px;border:1px solid transparent;border-radius:999px;white-space:nowrap}.nav a:hover{color:var(--lime);border-color:var(--line2)}header{padding:74px 0 48px;position:relative}.year{position:absolute;right:0;top:10px;font-weight:950;font-size:clamp(92px,18vw,220px);line-height:.8;color:transparent;-webkit-text-stroke:1px rgba(184,245,61,.14);z-index:-1}.eyebrow{color:var(--lime);font-family:var(--mono);font-size:12px;letter-spacing:.28em;text-transform:uppercase}h1{font-size:clamp(44px,7vw,86px);line-height:1;margin:18px 0 18px;max-width:920px;letter-spacing:-.045em}.accent{color:var(--lime)}.lede{max-width:760px;color:var(--dim);font-size:18px}.chips{display:flex;gap:10px;flex-wrap:wrap;margin-top:24px}.chip{font-family:var(--mono);font-size:12px;color:var(--dim);border:1px solid var(--line);background:rgba(12,24,17,.66);padding:8px 12px;border-radius:999px;text-decoration:none}.chip b{color:var(--ink)}a.chip:hover{color:var(--lime);border-color:var(--lime)}.hero-grid{display:grid;grid-template-columns:1.2fr .8fr;gap:16px;margin-top:34px}.panel{border:1px solid var(--line);background:linear-gradient(180deg,rgba(16,31,22,.86),rgba(12,24,17,.72));border-radius:18px;padding:22px;box-shadow:0 24px 80px rgba(0,0,0,.25)}.quick-stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}.stat{border:1px solid var(--line);border-radius:14px;padding:16px;background:rgba(7,16,11,.45)}.stat span{display:block;color:var(--faint);font-family:var(--mono);font-size:10px;text-transform:uppercase;letter-spacing:.06em;white-space:nowrap}.stat b{display:block;color:var(--lime);font-size:26px;margin-top:5px}section{margin-top:64px}.section-head{display:flex;align-items:flex-end;justify-content:space-between;gap:16px;margin-bottom:18px}.section-head h2{font-size:32px;margin:0;letter-spacing:-.02em}.section-head p{margin:0;color:var(--faint);font-size:13px}.board{border:1px solid var(--line);border-radius:18px;overflow:hidden;background:rgba(12,24,17,.56)}.row{display:grid;grid-template-columns:48px 230px 1fr 86px;gap:16px;align-items:center;padding:13px 16px;border-bottom:1px solid var(--line)}.row:last-child{border-bottom:0}.rank{font-family:var(--mono);color:var(--faint);font-size:12px}.team{display:flex;align-items:center;gap:10px;min-width:0}.flag{font-size:22px}.team a,.team-name{color:var(--ink);font-weight:750;text-decoration:none;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.team small{display:block;color:var(--faint);font-family:var(--mono);font-size:11px}.bar{height:16px;background:rgba(214,255,222,.07);border-radius:999px;overflow:hidden}.bar i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--lime),var(--gold));border-radius:inherit}.pct{font-family:var(--mono);font-weight:800;text-align:right}.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.card{border:1px solid var(--line);border-radius:16px;background:rgba(12,24,17,.62);padding:18px}.card h3{margin:0 0 8px;font-size:18px}.card p{margin:0;color:var(--dim)}.match-list{display:grid;gap:10px}.match{display:grid;grid-template-columns:110px 1fr 160px;gap:12px;align-items:center;border:1px solid var(--line);border-radius:14px;padding:14px;background:rgba(12,24,17,.62)}.match .time{font-family:var(--mono);color:var(--faint);font-size:12px}.teams-line{font-weight:800}.pred{font-family:var(--mono);color:var(--dim);font-size:12px;text-align:right}.group-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.group-card h3{margin:0 0 12px;color:var(--lime)}.mini-row{display:flex;justify-content:space-between;gap:8px;padding:6px 0;border-bottom:1px solid rgba(214,255,222,.08);font-size:14px}.mini-row:last-child{border-bottom:0}.fine{color:var(--faint);font-size:13px;margin-top:26px}.footer{margin-top:70px;border-top:1px solid var(--line);padding-top:24px;color:var(--faint);font-size:13px}.footer a{color:var(--lime)}@media(max-width:900px){.hero-grid,.quick-stats,.cards,.group-grid{grid-template-columns:1fr}.row{grid-template-columns:36px 1fr 70px}.row .bar{display:none}.match{grid-template-columns:1fr}.pred{text-align:left}.nav{max-width:70vw}.section-head{display:block}.topbar-inner{align-items:flex-start;flex-direction:column}}
</style>
</head>
<body>
<div class="topbar"><div class="topbar-inner"><a class="brand" href="/">Cup 2026 Predictor</a><nav class="nav"><a href="#predictions">Predictions</a><a href="#matches">Matches</a><a href="#groups">Groups</a><a href="/simulator/">Simulator</a><a href="/bracket-predictor/">Bracket</a><a href="/winner-predictions/">Winner</a></nav></div></div>
<div class="wrap">
<header>
  <div class="year">2026</div>
  <p class="eyebrow">AI World Cup predictor · live simulation model</p>
  <h1>2026 World Cup <span class="accent">Predictions</span> & AI Simulator</h1>
  <p class="lede">Explore champion probabilities, match score forecasts, group-stage odds, and projected bracket paths for the expanded 48-team World Cup in the United States, Canada, and Mexico.</p>
  <div class="chips" id="meta-chips"></div>
  <div class="chips">
    <a class="chip" href="/predictor/">World Cup Predictor 2026</a>
    <a class="chip" href="/simulator/">World Cup 2026 Simulator</a>
    <a class="chip" href="/bracket-predictor/">Bracket Predictor</a>
    <a class="chip" href="/winner-predictions/">Winner Predictions</a>
    <a class="chip" href="/groups/">Group Predictions</a>
  </div>
  <div class="hero-grid">
    <div class="panel"><div class="quick-stats" id="quick-stats"></div></div>
    <div class="panel"><h2 style="margin:0 0 10px">Model approach</h2><p class="fine" style="margin:0">Dynamic Elo ratings feed expected-goal distributions, score probabilities, host boosts, optional market-odds blending, and conditional Monte Carlo simulations. Picks are locked before kickoff for performance tracking.</p></div>
  </div>
</header>
<main>
<section id="predictions"><div class="section-head"><div><h2>World Cup 2026 winner predictions</h2><p>Champion probabilities from the latest tournament simulation.</p></div><p id="updated"></p></div><div class="board" id="winner-board"></div></section>
<section id="finals"><div class="section-head"><div><h2>Most likely final matchups</h2><p>The final pairings appearing most often across simulations.</p></div></div><div class="cards" id="final-cards"></div></section>
<section id="matches"><div class="section-head"><div><h2>Upcoming match predictions</h2><p>Score and outcome forecasts for the next scheduled fixtures.</p></div><a class="chip" href="/predictor/">Open predictor page</a></div><div class="match-list" id="match-list"></div></section>
<section id="groups"><div class="section-head"><div><h2>Group-stage outlook</h2><p>Projected group winners and qualification probabilities.</p></div><a class="chip" href="/groups/">View group page</a></div><div class="group-grid" id="group-grid"></div></section>
<section id="teams"><div class="section-head"><div><h2>Team prediction pages</h2><p>SEO-ready team pages backed by the same probability data.</p></div></div><div class="cards" id="team-cards"></div></section>
<section id="record"><div class="section-head"><div><h2>Prediction record</h2><p>All scoring is based on predictions locked before kickoff.</p></div></div><div class="cards" id="record-cards"></div></section>
</main>
<footer class="footer"><p>Predictions are for information and entertainment only. They are not betting advice. Data updates are generated from the local model and source snapshots in this repository.</p></footer>
</div>
<script src="/data.js"></script>
<script src="/reports.js"></script>
<script src="/blurbs.js"></script>
<script>
(() => {
  const D = window.WC_DATA;
  if (!D) { document.body.innerHTML = '<main class="wrap"><h1>Missing prediction data</h1><p>Run <code>./scripts/python -m src.predict simulate --sims 20000</code> to generate <code>web/data.js</code>.</p></main>'; return; }
  const FLAGS = {ARG:'🇦🇷',ESP:'🇪🇸',FRA:'🇫🇷',ENG:'🏴',BRA:'🇧🇷',POR:'🇵🇹',COL:'🇨🇴',MEX:'🇲🇽',NED:'🇳🇱',GER:'🇩🇪',ECU:'🇪🇨',TUR:'🇹🇷',URU:'🇺🇾',JPN:'🇯🇵',SUI:'🇨🇭',USA:'🇺🇸',CAN:'🇨🇦',KOR:'🇰🇷',CZE:'🇨🇿',RSA:'🇿🇦',MAR:'🇲🇦'};
  const slug = name => ({'United States':'usa'}[name] || name.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,''));
  const team = code => D.teams.find(t => t.code === code) || {code, name_en: code};
  const name = code => team(code).name_en || code;
  const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const pct = (v, d=1) => v == null ? '—' : (v > 0 && v * 100 < 0.05 ? '<0.1%' : (v * 100).toFixed(d) + '%');
  const stage = {group:'Group',r32:'Round of 32',r16:'Round of 16',qf:'Quarter-final',sf:'Semi-final',third_place:'Third-place match',final:'Final'};
  const fmtDate = iso => { try { return new Date(iso).toLocaleString('en-US',{month:'short',day:'numeric',hour:'2-digit',minute:'2-digit'}); } catch { return iso || 'TBD'; } };
  document.getElementById('updated').textContent = `Updated ${D.meta.updated_at}`;
  document.getElementById('meta-chips').innerHTML = [`${D.meta.sims.toLocaleString()} simulations`, `${D.meta.played}/${D.meta.total} matches played`, D.meta.market ? 'Market odds blended' : 'Model-only probabilities', `Seed ${D.meta.seed ?? 'auto'}`].map(x=>`<span class="chip"><b>${x}</b></span>`).join('');
  const top = [...D.teams].sort((a,b)=>b.p_champion-a.p_champion);
  document.getElementById('quick-stats').innerHTML = [
    ['Favorite', `${FLAGS[top[0].code]||''} ${top[0].name_en}`], ['Champion chance', pct(top[0].p_champion)], ['Teams', D.teams.length], ['Matches', D.meta.total]
  ].map(([a,b])=>`<div class="stat"><span>${a}</span><b>${b}</b></div>`).join('');
  document.getElementById('winner-board').innerHTML = top.slice(0,18).map((t,i)=>`<div class="row"><div class="rank">#${i+1}</div><div class="team"><span class="flag">${FLAGS[t.code]||'⚽'}</span><div><a href="/teams/${slug(t.name_en)}/">${esc(t.name_en)}</a><small>Group ${t.group} · Elo ${Math.round(t.elo)}</small></div></div><div class="bar"><i style="width:${Math.max(2,t.p_champion*100*3.2)}%"></i></div><div class="pct">${pct(t.p_champion)}</div></div>`).join('');
  document.getElementById('final-cards').innerHTML = (D.top_finals||[]).slice(0,6).map(f=>{ const [a,b]=f.pair; return `<article class="card"><h3>${FLAGS[a]||''} ${esc(name(a))} vs ${FLAGS[b]||''} ${esc(name(b))}</h3><p>${pct(f.p)} simulated final probability</p></article>`; }).join('');
  const upcoming = D.schedule.filter(m => !m.score).slice(0,10);
  document.getElementById('match-list').innerHTML = upcoming.map(m=>{ const h=m.home?name(m.home):(m.slot_home||'TBD'); const a=m.away?name(m.away):(m.slot_away||'TBD'); const pr=m.pred||{}; return `<div class="match"><div class="time">${fmtDate(m.date_utc)}<br>${stage[m.stage]||m.stage}</div><div class="teams-line">${m.home?(FLAGS[m.home]||'⚽'):''} ${esc(h)} <span style="color:var(--faint)">vs</span> ${esc(a)} ${m.away?(FLAGS[m.away]||'⚽'):''}<br><small style="color:var(--faint);font-weight:500">${esc(m.venue||'Venue TBD')}</small></div><div class="pred">${pr.outcome_score ? `Pick ${pr.outcome_score[0]}-${pr.outcome_score[1]}` : 'Prediction pending'}<br>${pr.p_home!=null ? `${pct(pr.p_home,0)} · ${pct(pr.p_draw,0)} · ${pct(pr.p_away,0)}` : ''}</div></div>`}).join('');
  const groups = [...new Set(D.teams.map(t=>t.group))].sort();
  document.getElementById('group-grid').innerHTML = groups.map(g=>{ const rows=D.teams.filter(t=>t.group===g).sort((a,b)=>b.p_group_win-a.p_group_win); return `<article class="card group-card"><h3>Group ${g}</h3>${rows.map(t=>`<div class="mini-row"><span>${FLAGS[t.code]||''} ${esc(t.name_en)}</span><b>${pct(t.p_r32,0)}</b></div>`).join('')}</article>`; }).join('');
  document.getElementById('team-cards').innerHTML = top.slice(0,9).map(t=>`<article class="card"><h3>${FLAGS[t.code]||''} ${esc(t.name_en)}</h3><p>Champion ${pct(t.p_champion)} · Final ${pct(t.p_final)} · Round of 32 ${pct(t.p_r32)}</p><p style="margin-top:10px"><a class="chip" href="/teams/${slug(t.name_en)}/">${esc(t.name_en)} prediction</a></p></article>`).join('');
  const st = D.record?.stats || {};
  document.getElementById('record-cards').innerHTML = [
    ['Locked matches', st.n ?? 0], ['Outcome accuracy', st.outcome_acc == null ? '—' : pct(st.outcome_acc,0)], ['Exact score accuracy', st.score_acc == null ? '—' : pct(st.score_acc,0)], ['Brier score', st.brier == null ? '—' : Number(st.brier).toFixed(3)]
  ].map(([a,b])=>`<article class="card"><h3>${a}</h3><p style="font-size:28px;color:var(--lime);font-weight:900">${b}</p></article>`).join('');
})();
</script>
</body>
</html>
'''

LANDING_CSS = """
:root{--bg:#07100b;--panel:#0c1811;--line:rgba(214,255,222,.15);--ink:#eaf6ec;--dim:#91aa98;--lime:#b8f53d;--gold:#ffd75e;--hot:#ff7a52}*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 80% 0,rgba(184,245,61,.13),transparent 34%),var(--bg);color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;line-height:1.65}.wrap{max-width:1040px;margin:0 auto;padding:36px 22px 80px}.brand{color:var(--lime);text-decoration:none;font-weight:800;letter-spacing:.08em;text-transform:uppercase;font-size:13px}.hero{padding:70px 0 44px}.eyebrow{color:var(--lime);font-size:13px;letter-spacing:.22em;text-transform:uppercase}h1{font-size:clamp(42px,8vw,78px);line-height:1.02;margin:12px 0 18px;max-width:900px}.lede{font-size:19px;color:var(--dim);max-width:760px}.actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:28px}.button{border:1px solid var(--line);color:var(--ink);text-decoration:none;padding:12px 18px;border-radius:8px}.button.primary{background:var(--lime);color:#07100b;border-color:var(--lime);font-weight:800}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:20px 0 42px}.card,.content{border:1px solid var(--line);background:rgba(12,24,17,.76);border-radius:14px;padding:20px}.card b{display:block;color:var(--gold);font-size:22px;margin-bottom:6px}.card span{color:var(--dim);font-size:14px}.content h2{font-size:28px;margin:8px 0 12px}.content h3{margin-top:28px}.content p,.content li{color:var(--dim)}.links{display:flex;gap:10px;flex-wrap:wrap;margin-top:28px}.links a{color:var(--lime);border:1px solid var(--line);padding:8px 12px;border-radius:999px;text-decoration:none;font-size:14px}.fine{color:#6f8274;font-size:13px;margin-top:28px}@media(max-width:760px){.grid{grid-template-columns:1fr}h1{font-size:42px}}
""".strip()+"\n"

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang=\"en\"><head><meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><title>{title}</title><meta name=\"description\" content=\"{description}\"><link rel=\"canonical\" href=\"{canonical}\"><meta property=\"og:type\" content=\"website\"><meta property=\"og:site_name\" content=\"Cup 2026 Predictor\"><meta property=\"og:title\" content=\"{title}\"><meta property=\"og:description\" content=\"{description}\"><meta property=\"og:url\" content=\"{canonical}\"><meta property=\"og:image\" content=\"https://cup2026predictor.com/og-image.png\"><link rel=\"icon\" type=\"image/png\" href=\"/favicon.png\"><link rel=\"stylesheet\" href=\"/landing.css\"><script type=\"application/ld+json\">{schema}</script><!-- Privacy-friendly analytics by Plausible --><script async src=\"https://plausible.xiaoyuan.fun/js/pa-WK90PG-0AX8mkAS5xo1rK.js\"></script><script>window.plausible=window.plausible||function(){{(plausible.q=plausible.q||[]).push(arguments)}},plausible.init=plausible.init||function(i){{plausible.o=i||{{}}}};plausible.init()</script></head>
<body><main class=\"wrap\"><a class=\"brand\" href=\"/\">Cup 2026 Predictor</a><section class=\"hero\"><p class=\"eyebrow\">World Cup 2026 prediction tool</p><h1>{h1}</h1><p class=\"lede\">{lede}</p><div class=\"actions\"><a class=\"button primary\" href=\"/\">Open the live predictor</a><a class=\"button\" href=\"/simulator/\">Run tournament simulator</a></div></section><section class=\"grid\">{cards}</section><section class=\"content\">{body}</section><nav class=\"links\"><a href=\"/predictor/\">Predictor</a><a href=\"/simulator/\">Simulator</a><a href=\"/bracket-predictor/\">Bracket predictor</a><a href=\"/winner-predictions/\">Winner predictions</a><a href=\"/groups/\">Groups</a><a href=\"/teams/argentina/\">Teams</a></nav><p class=\"fine\">Predictions are for information and entertainment only. They are not betting advice.</p></main></body></html>
"""

def load_data():
    p = WEB / "data.js"
    if not p.exists():
        return None
    s = p.read_text(encoding="utf-8")
    return json.loads(s.removeprefix("window.WC_DATA = ").rstrip(";\n"))

def slugify(s: str) -> str:
    return COUNTRY_SLUG.get(s) or re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def pct(v):
    return "—" if v is None else f"{v*100:.1f}%"

def make_page(slug, title, description, h1, lede, cards, body):
    d = WEB / slug
    d.mkdir(parents=True, exist_ok=True)
    canonical = f"{DOMAIN}/{slug}/"
    schema = json.dumps({"@context":"https://schema.org","@type":"WebPage","name":title,"url":canonical,"description":description,"isPartOf":{"@type":"WebSite","name":SITE,"url":DOMAIN+"/"}}, ensure_ascii=False)
    html_text = PAGE_TEMPLATE.format(title=html.escape(title), description=html.escape(description), canonical=canonical, h1=html.escape(h1), lede=html.escape(lede), cards="\n".join(f'<article class="card"><b>{html.escape(k)}</b><span>{html.escape(v)}</span></article>' for k,v in cards), body=body, schema=html.escape(schema, quote=False))
    (d / "index.html").write_text(html_text, encoding="utf-8")

def generate_pages():
    data = load_data()
    teams = data["teams"] if data else []
    by_name = {t["name_en"]: t for t in teams}
    top = sorted(teams, key=lambda t: t.get("p_champion") or 0, reverse=True)
    WEB.joinpath("index.html").write_text(INDEX_HTML, encoding="utf-8")
    WEB.joinpath("landing.css").write_text(LANDING_CSS, encoding="utf-8")
    generic = [
        ("predictor", "World Cup Predictor 2026 | Cup 2026 Predictor", "Use a 2026 World Cup predictor with AI-powered winner chances, match forecasts, group-stage probabilities, and bracket paths.", "World Cup Predictor 2026", "Pick a team, compare match probabilities, and follow AI-updated predictions for the 2026 World Cup.", [("48 teams", "Group and knockout paths"), ("104 matches", "Score and outcome forecasts"), ("Live record", "Pre-kickoff picks tracked")], "<h2>What the predictor does</h2><p>The predictor combines Elo ratings, score distributions, host boost adjustments, optional market signals, and Monte Carlo tournament simulations. It is designed for users searching for World Cup 2026 predictions, winner chances, and match score forecasts.</p>"),
        ("simulator", "World Cup 2026 Simulator | Monte Carlo Tournament Predictions", "Simulate the 2026 World Cup bracket and group stage with AI-powered Monte Carlo projections and champion probabilities.", "World Cup 2026 Simulator", "Run tournament simulations to estimate every team's path from the group stage to the final.", [("Monte Carlo", "Tournament-level simulations"), ("Bracket paths", "Round of 32 to final"), ("Winner chances", "Champion probability table")], "<h2>Built for tournament scenarios</h2><p>The simulator locks completed results, updates Elo after matches, and replays the remaining tournament to estimate qualification, knockout, finalist, and champion probabilities.</p>"),
        ("bracket-predictor", "World Cup 2026 Bracket Predictor | Projected Knockout Bracket", "Explore a World Cup 2026 bracket predictor with projected knockout paths, round probabilities, and likely finals.", "World Cup 2026 Bracket Predictor", "Project the Round of 32, knockout paths, likely finals, and champion chances from current simulation data.", [("Round of 32", "Official 48-team format"), ("Likely finals", "Most common simulated pairings"), ("Knockout mode", "Extra time and penalties modeled")], "<h2>Bracket prediction approach</h2><p>The bracket predictor follows the official expanded 2026 structure: 12 groups, best third-place teams, Round of 32 slots, then the fixed knockout tree through the final.</p>"),
        ("winner-predictions", "World Cup 2026 Winner Predictions | Champion Chances", "See World Cup 2026 winner predictions, champion probabilities, favorites, dark horses, and AI-updated title chances.", "World Cup 2026 Winner Predictions", "Compare favorites, dark horses, and daily champion probability movement for the 2026 World Cup.", [("Current favorite", top[0]["name_en"] if top else "TBD"), ("Favorite chance", pct(top[0].get("p_champion")) if top else "—"), ("Update cadence", "After match windows")], "<h2>Champion probability, not hype</h2><p>Winner predictions are generated from tournament simulations rather than editorial picks. Use them to compare contenders and track how each result changes the title race.</p>"),
        ("groups", "World Cup 2026 Group Predictions | Group Stage Odds", "Check World Cup 2026 group predictions, qualification odds, group winner chances, and best third-place scenarios.", "World Cup 2026 Group Predictions", "Follow group-stage projections for all 12 groups, including qualification and group winner scenarios.", [("12 groups", "48-team expanded format"), ("Top two", "Automatic qualification paths"), ("Best thirds", "Third-place race modeled")], "<h2>Group-stage prediction coverage</h2><p>Each group is modeled with expected points, group winner probability, Round of 32 probability, and later-stage tournament chances.</p>"),
    ]
    for args in generic: make_page(*args)
    selected = [t for t in top if slugify(t["name_en"]) in TEAM_SLUGS]
    for t in selected:
        nm, sl = t["name_en"], slugify(t["name_en"])
        title = f"{nm} World Cup 2026 Prediction | Cup 2026 Predictor"
        desc = f"{nm} World Cup 2026 prediction with champion chances, group outlook, match forecasts, and projected bracket path."
        body = f"<h2>{html.escape(nm)} prediction data</h2><p>{html.escape(nm)} is in Group {t['group']} with Elo {round(t['elo'])}. Current model probabilities: Round of 32 {pct(t.get('p_r32'))}, Round of 16 {pct(t.get('p_r16'))}, quarter-final {pct(t.get('p_qf'))}, semi-final {pct(t.get('p_sf'))}, final {pct(t.get('p_final'))}, champion {pct(t.get('p_champion'))}.</p><h3>How to use this page</h3><p>Use this team page as a fast summary, then open the live predictor for updated match forecasts and group-stage movement.</p>"
        make_page(f"teams/{sl}", title, desc, f"{nm} World Cup 2026 Prediction", f"Track {nm}'s 2026 World Cup winner chances, group outlook, match projections, and likely bracket path.", [("Group", str(t['group'])), ("Elo", str(round(t['elo']))), ("Champion chance", pct(t.get('p_champion')))], body)

def update_sitemap_robots():
    urls = ["/"] + ["/predictor/","/simulator/","/bracket-predictor/","/winner-predictions/","/groups/"] + [f"/teams/{x}/" for x in TEAM_SLUGS]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        xml.append(f"  <url><loc>{DOMAIN}{u}</loc><lastmod>2026-06-12</lastmod><changefreq>daily</changefreq><priority>{'1.0' if u=='/' else '0.8'}</priority></url>")
    xml.append('</urlset>')
    (WEB/'sitemap.xml').write_text('\n'.join(xml)+'\n', encoding='utf-8')
    (WEB/'robots.txt').write_text(f"User-agent: *\nAllow: /\n\nUser-agent: Googlebot\nAllow: /\n\nUser-agent: Bingbot\nAllow: /\n\nUser-agent: Applebot\nAllow: /\n\nUser-agent: DuckDuckBot\nAllow: /\n\nUser-agent: GPTBot\nAllow: /\n\nUser-agent: ChatGPT-User\nAllow: /\n\nUser-agent: OAI-SearchBot\nAllow: /\n\nUser-agent: PerplexityBot\nAllow: /\n\nUser-agent: ClaudeBot\nAllow: /\n\nUser-agent: anthropic-ai\nAllow: /\n\nUser-agent: CCBot\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n", encoding='utf-8')
    (WEB/'llms.txt').write_text(f"""# Cup 2026 Predictor

Cup 2026 Predictor is an English World Cup 2026 prediction and simulator site.

Canonical URL: {DOMAIN}/
Sitemap: {DOMAIN}/sitemap.xml
Robots: {DOMAIN}/robots.txt

## Key pages

- {DOMAIN}/ — 2026 World Cup predictions and live AI simulator overview.
- {DOMAIN}/predictor/ — World Cup Predictor 2026 landing page.
- {DOMAIN}/simulator/ — World Cup 2026 tournament simulator page.
- {DOMAIN}/bracket-predictor/ — projected World Cup 2026 bracket predictor.
- {DOMAIN}/winner-predictions/ — World Cup 2026 winner predictions and champion chances.
- {DOMAIN}/groups/ — World Cup 2026 group-stage prediction page.
- {DOMAIN}/teams/spain/ — Spain World Cup 2026 prediction.
- {DOMAIN}/teams/argentina/ — Argentina World Cup 2026 prediction.
- {DOMAIN}/teams/brazil/ — Brazil World Cup 2026 prediction.
- {DOMAIN}/teams/england/ — England World Cup 2026 prediction.
- {DOMAIN}/teams/usa/ — United States World Cup 2026 prediction.
- {DOMAIN}/teams/mexico/ — Mexico World Cup 2026 prediction.

## Data and model notes

The site uses a local Python prediction engine based on dynamic Elo ratings, score distributions, host boosts, optional market signals, and Monte Carlo tournament simulations. Predictions are for information and entertainment only and are not betting advice.

## Source attribution

This project is a second-development fork of the open-source ai-worldcup-2026 project, with custom English SEO pages, branding, analytics, and deployment workflow for cup2026predictor.com.
""", encoding='utf-8')

def main():
    generate_pages()
    update_sitemap_robots()

if __name__ == '__main__':
    main()
