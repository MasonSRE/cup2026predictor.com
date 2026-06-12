#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
import json, re

WEB = Path(__file__).resolve().parents[1] / 'web'
DOMAIN = 'https://cup2026predictor.com'

class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.title=''; self.desc=''; self.canonical=''; self.h1=[]; self.h2=[]; self.links=[]; self.scripts=[]; self.schema=[]; self._tag=None
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs); self._tag=tag
        if tag=='meta' and attrs.get('name')=='description': self.desc=attrs.get('content') or ''
        if tag=='link' and attrs.get('rel')=='canonical': self.canonical=attrs.get('href') or ''
        if tag=='a' and attrs.get('href'): self.links.append(attrs.get('href'))
        if tag=='script':
            if attrs.get('src'): self.scripts.append(attrs.get('src'))
            if attrs.get('type')=='application/ld+json': self._schema=True
        if tag in ['title','h1','h2']: self._tag=tag
    def handle_endtag(self, tag):
        if tag == 'script': self._schema=False
        if tag == self._tag: self._tag=None
    def handle_data(self, data):
        d=data.strip()
        if not d: return
        if self._tag=='title': self.title += d
        elif self._tag=='h1': self.h1.append(d)
        elif self._tag=='h2': self.h2.append(d)
        elif getattr(self,'_schema',False): self.schema.append(d)

def audit():
    rows=[]; issues=[]
    pages=sorted(WEB.rglob('*.html'))
    titles=[]; descs=[]
    for p in pages:
        rel=str(p.relative_to(WEB))
        html=p.read_text(errors='ignore')
        pa=P(); pa.feed(html)
        titles.append(pa.title); descs.append(pa.desc)
        size=p.stat().st_size
        internal=[x for x in pa.links if x.startswith('/') or x.startswith(DOMAIN)]
        schema_types=[]
        for sc in pa.schema:
            try:
                obj=json.loads(sc)
                raw=json.dumps(obj)
                schema_types += re.findall(r'"@type"\s*:\s*"([^"]+)"', raw)
            except Exception: pass
        page_issues=[]
        if not (35 <= len(pa.title) <= 70): page_issues.append(f'title length {len(pa.title)}')
        if not (80 <= len(pa.desc) <= 170): page_issues.append(f'description length {len(pa.desc)}')
        if len(pa.h1)!=1: page_issues.append(f'H1 count {len(pa.h1)}')
        if len(internal)<3: page_issues.append(f'only {len(internal)} internal links')
        if not schema_types: page_issues.append('missing JSON-LD type')
        if 'pa-WK90PG-0AX8mkAS5xo1rK.js' not in html: page_issues.append('missing Plausible')
        if size>120000: page_issues.append(f'large HTML {size} bytes')
        if re.search(r'[\u4e00-\u9fff]', html): page_issues.append('CJK text remains')
        rows.append({'page':rel,'title':pa.title,'description_len':len(pa.desc),'h1':pa.h1,'internal_links':len(internal),'schema_types':schema_types,'size_bytes':size,'issues':page_issues})
        issues += [(rel,x) for x in page_issues]
    dup_titles=[k for k,v in Counter(titles).items() if k and v>1]
    dup_descs=[k for k,v in Counter(descs).items() if k and v>1]
    robots=(WEB/'robots.txt').read_text(errors='ignore')
    sitemap=(WEB/'sitemap.xml').read_text(errors='ignore')
    summary={
        'pages_checked':len(pages),
        'duplicate_titles':dup_titles,
        'duplicate_descriptions':len(dup_descs),
        'robots_has_sitemap': f'Sitemap: {DOMAIN}/sitemap.xml' in robots,
        'robots_disallows_public_js': any(x in robots for x in ['Disallow: /data.js','Disallow: /reports.js','Disallow: /blurbs.js']),
        'sitemap_url_count': sitemap.count('<url>'),
        'issues': issues,
        'top_recommendations': []
    }
    # Recommendations based on audit and site shape.
    if not (WEB/'llms.txt').exists(): summary['top_recommendations'].append('Add /llms.txt for AI/search-answer crawler context before launch.')
    if any('only ' in issue for _,issue in issues): summary['top_recommendations'].append('Increase contextual internal links on thin landing/team pages.')
    if any('description length' in issue for _,issue in issues): summary['top_recommendations'].append('Normalize meta descriptions to 80-170 chars.')
    summary['top_recommendations'].append('After Cloudflare deployment, verify live robots.txt because Cloudflare managed robots may override repository robots rules.')
    return {'summary':summary,'pages':rows}

out=audit()
Path('/tmp/cup2026_seo_audit.json').write_text(json.dumps(out,indent=2,ensure_ascii=False))
print(json.dumps(out['summary'], indent=2, ensure_ascii=False))
for r in out['pages']:
    if r['issues']:
        print('-', r['page'], '=>', '; '.join(r['issues']))
