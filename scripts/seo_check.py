#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from html.parser import HTMLParser
import sys

WEB = Path(__file__).resolve().parents[1] / 'web'
required_pages = [
    'index.html','predictor/index.html','simulator/index.html','bracket-predictor/index.html',
    'winner-predictions/index.html','groups/index.html','teams/argentina/index.html',
    'teams/spain/index.html','teams/brazil/index.html','teams/england/index.html','teams/usa/index.html','teams/mexico/index.html'
]
class MetaParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.title=''; self._in_title=False; self.h1=[]; self.canonical=None; self.description=None
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag=='title': self._in_title=True
        if tag=='h1': self._in_h1=True
        if tag=='link' and attrs.get('rel')=='canonical': self.canonical=attrs.get('href')
        if tag=='meta' and attrs.get('name')=='description': self.description=attrs.get('content')
    def handle_endtag(self, tag):
        if tag=='title': self._in_title=False
        if tag=='h1': self._in_h1=False
    def handle_data(self, data):
        if getattr(self,'_in_title',False): self.title += data.strip()
        if getattr(self,'_in_h1',False): self.h1.append(data.strip())

errors=[]
for rel in required_pages:
    p=WEB/rel
    if not p.exists(): errors.append(f'missing {rel}'); continue
    s=p.read_text(errors='ignore')
    parser=MetaParser(); parser.feed(s)
    if not parser.title: errors.append(f'{rel}: missing title')
    if not parser.description or len(parser.description)<50: errors.append(f'{rel}: weak/missing description')
    if not parser.canonical or not parser.canonical.startswith('https://cup2026predictor.com/'): errors.append(f'{rel}: bad canonical {parser.canonical}')
    if not parser.h1: errors.append(f'{rel}: missing h1')
    if 'worldcup.lightai.io' in s: errors.append(f'{rel}: old domain still present')

site=(WEB/'sitemap.xml').read_text()
for rel in required_pages:
    url='https://cup2026predictor.com/' + ('' if rel=='index.html' else rel.replace('index.html',''))
    if url not in site: errors.append(f'sitemap missing {url}')
robots=(WEB/'robots.txt').read_text()
if 'https://cup2026predictor.com/sitemap.xml' not in robots: errors.append('robots sitemap wrong')

if errors:
    print('FAIL')
    for e in errors: print('-', e)
    sys.exit(1)
print('OK: checked', len(required_pages), 'pages')
