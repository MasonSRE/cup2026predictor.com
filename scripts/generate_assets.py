#!/usr/bin/env python3
"""Generate Cup 2026 Predictor social and icon assets."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / 'web'
BG = (7, 16, 11)
PANEL = (12, 24, 17)
LIME = (184, 245, 61)
GOLD = (255, 215, 94)
INK = (234, 246, 236)
DIM = (135, 166, 144)

def font(size, bold=False):
    candidates = [
        '/System/Library/Fonts/Supplemental/Arial Bold.ttf' if bold else '/System/Library/Fonts/Supplemental/Arial.ttf',
        '/System/Library/Fonts/Helvetica.ttc',
        '/Library/Fonts/Arial.ttf',
    ]
    for p in candidates:
        try: return ImageFont.truetype(p, size=size)
        except Exception: pass
    return ImageFont.load_default()

def fit_text(draw, text, max_width, start_size, bold=False):
    size = start_size
    while size > 16:
        f = font(size, bold)
        if draw.textbbox((0,0), text, font=f)[2] <= max_width:
            return f
        size -= 2
    return font(size, bold)

def draw_pitch(draw, w, h):
    for x in range(-200, w+200, 140):
        draw.line([(x,0),(x+260,h)], fill=(18,40,25), width=2)
    draw.rectangle([70,70,w-70,h-70], outline=(52,83,58), width=3)
    draw.line([(w//2,70),(w//2,h-70)], fill=(52,83,58), width=3)
    draw.ellipse([w//2-92,h//2-92,w//2+92,h//2+92], outline=(52,83,58), width=3)

def og():
    w,h=1200,630
    img=Image.new('RGB',(w,h),BG)
    overlay=Image.new('RGBA',(w,h),(0,0,0,0))
    od=ImageDraw.Draw(overlay)
    for r in range(0,700,6):
        alpha=max(0,90-r//8)
        od.ellipse([820-r,-180-r,820+r,-180+r], fill=(*LIME,alpha))
    img=Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    d=ImageDraw.Draw(img)
    draw_pitch(d,w,h)
    d.rounded_rectangle([70,70,1130,560], radius=34, fill=(7,16,11), outline=(52,83,58), width=2)
    d.text((105,105),'WORLD CUP 2026 · AI PREDICTOR', font=font(26, True), fill=LIME)
    title='Cup 2026 Predictor'
    d.text((105,165), title, font=fit_text(d,title,840,78,True), fill=INK)
    sub='Predictions · Simulator · Bracket · Winner Chances'
    d.text((108,258), sub, font=font(34, False), fill=DIM)
    # trophy-ish mark
    cx,cy=965,255
    d.ellipse([cx-88,cy-88,cx+88,cy+88], outline=LIME, width=8)
    d.arc([cx-130,cy-35,cx-55,cy+55], 90, 270, fill=GOLD, width=9)
    d.arc([cx+55,cy-35,cx+130,cy+55], 270, 90, fill=GOLD, width=9)
    d.rectangle([cx-28,cy+86,cx+28,cy+150], fill=GOLD)
    d.rounded_rectangle([cx-82,cy+150,cx+82,cy+176], radius=8, fill=LIME)
    stats=[('48','TEAMS'),('104','MATCHES'),('MONTE CARLO','SIMS')]
    x=105
    for big,label in stats:
        d.rounded_rectangle([x,395,x+250,500], radius=18, fill=PANEL, outline=(52,83,58), width=2)
        d.text((x+22,414), big, font=font(34, True), fill=GOLD if big=='MONTE CARLO' else LIME)
        d.text((x+22,458), label, font=font(18, True), fill=DIM)
        x += 275
    d.text((880,490),'cup2026predictor.com', font=font(26, True), fill=LIME)
    img.save(WEB/'og-image.png', quality=95)

def icon(size, path):
    img=Image.new('RGB',(size,size),BG)
    d=ImageDraw.Draw(img)
    d.rounded_rectangle([size*.08,size*.08,size*.92,size*.92], radius=int(size*.18), fill=PANEL, outline=LIME, width=max(3,size//24))
    d.text((size*.18,size*.20),'CUP', font=fit_text(d,'CUP',size*.64,int(size*.23),True), fill=INK)
    d.text((size*.20,size*.47),'2026', font=fit_text(d,'2026',size*.60,int(size*.22),True), fill=LIME)
    d.ellipse([size*.36,size*.70,size*.64,size*.98], fill=GOLD)
    img.save(path)

def main():
    og()
    icon(64, WEB/'favicon.png')
    icon(180, WEB/'apple-touch-icon.png')

if __name__ == '__main__': main()
