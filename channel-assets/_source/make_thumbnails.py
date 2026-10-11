# Thumbnails, 1280x720, one fixed layout per channel so every episode looks like a set.
# Run from the repo root: python3 channel-assets/_source/make_thumbnails.py <fonts-dir>
import math, random, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F = sys.argv[1].rstrip('/') + '/'
OUT = "channel-assets/thumbnails/"
W, H = 1280, 720
def font(name, size, wght=None):
    f = ImageFont.truetype(F + name, size)
    if wght is not None:
        try: f.set_variation_by_axes([wght])
        except Exception: pass
    return f
def hexc(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def vgrad(top, bot):
    img = Image.new("RGB", (W, H), top); px = img.load()
    for y in range(H):
        t = y / (H - 1); c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
        for x in range(W): px[x, y] = c
    return img
def fit(d, lines, name, maxw, start, wght=None, minsize=48):
    size = start
    while size > minsize:
        f = font(name, size, wght)
        if all(d.textlength(l, font=f) <= maxw for l in lines): return f
        size -= 4
    return font(name, minsize, wght)
def shadow_text(d, xy, text, f, fill, shadow=(0, 0, 0), off=4):
    d.text((xy[0] + off, xy[1] + off), text, font=f, fill=shadow)
    d.text(xy, text, font=f, fill=fill)

# ---------- Gold and Ruin: dark ink, gold serif, cracked coin on the right ----------
INK = hexc("120E0B"); INK2 = hexc("2A1E14"); GOLD = hexc("C9A44C"); GOLD_D = hexc("8C6E2A"); GOLD_L = hexc("E8CD7E"); CREAM = hexc("EFE6D2"); RED = hexc("B8392E")
def coin(d, cx, cy, R):
    d.ellipse([cx-R, cy-R, cx+R, cy+R], fill=GOLD_D)
    d.ellipse([cx-R+10, cy-R+10, cx+R-10, cy+R-10], fill=GOLD)
    d.ellipse([cx-R+32, cy-R+32, cx+R-32, cy+R-32], outline=GOLD_D, width=6)
    for i in range(40):
        a = 2*math.pi*i/40; r1 = R-18; r2 = R-26
        d.line([cx+r1*math.cos(a), cy+r1*math.sin(a), cx+r2*math.cos(a), cy+r2*math.sin(a)], fill=GOLD_D, width=3)
    g = font("Cinzel[wght].ttf", int(R*0.95), 800)
    w = d.textlength("G", font=g); bb = d.textbbox((0, 0), "G", font=g)
    d.text((cx-w/2+3, cy-(bb[1]+bb[3])/2+3), "G", font=g, fill=GOLD_D)
    d.text((cx-w/2, cy-(bb[1]+bb[3])/2), "G", font=g, fill=GOLD_L)
    pts = [(cx+R*0.15, cy-R-4), (cx-R*0.05, cy-R*0.45), (cx+R*0.18, cy-R*0.15), (cx-R*0.12, cy+R*0.2), (cx+R*0.1, cy+R*0.5), (cx-R*0.08, cy+R+4)]
    left = [(x-7, y) for x, y in pts]; right = [(x+7, y) for x, y in reversed(pts)]
    d.polygon(left+right, fill=INK)
def gold_and_ruin(slug, top, big, bottom):
    im = vgrad(INK2, INK)
    glow = Image.new("L", (W, H), 0); gd = ImageDraw.Draw(glow); gd.ellipse([W-560, H//2-300, W+40, H//2+300], fill=90)
    glow = glow.filter(ImageFilter.GaussianBlur(90)); im = Image.composite(Image.new("RGB", (W, H), hexc("5A4220")), im, glow)
    d = ImageDraw.Draw(im)
    coin(d, 1010, 360, 220)
    d.rectangle([0, 0, 760, H], fill=None)
    maxw = 700
    f1 = fit(d, [top], "Cinzel[wght].ttf", maxw, 54, 700, 36)
    f2 = fit(d, big, "Cinzel[wght].ttf", maxw, 118, 800, 64)
    f3 = fit(d, [bottom], "CormorantGaramond-Italic[wght].ttf", maxw, 54, 600, 36)
    y = 120
    shadow_text(d, (60, y), top, f1, GOLD); y += f1.size + 28
    for line in big:
        shadow_text(d, (60, y), line, f2, CREAM, off=6); y += f2.size + 10
    y += 24
    d.line([60, y, 60+maxw, y], fill=GOLD_D, width=3); y += 24
    shadow_text(d, (60, y), bottom, f3, GOLD_L)
    im.save(OUT + slug + ".png", optimize=True)

# ---------- Twist of Myth: indigo sky, stars, amber spiral on the right, parchment serif ----------
INDIGO = hexc("1B1638"); TEAL = hexc("0F3B44"); AMBER = hexc("F2B35E"); PARCH = hexc("F3E9D2")
def stars(d, n, seed):
    rnd = random.Random(seed)
    for _ in range(n):
        x = rnd.randrange(W); y = rnd.randrange(H); r = rnd.choice([1, 1, 2, 2, 3])
        d.ellipse([x-r, y-r, x+r, y+r], fill=(235, 225, 200))
def spiral(d, cx, cy, turns, maxr, width, col):
    pts = []; N = 500
    for i in range(N+1):
        t = i/N; a = t*turns*2*math.pi; r = maxr*t
        pts.append((cx+r*math.cos(a), cy+r*math.sin(a)))
    d.line(pts, fill=col, width=width, joint="curve")
def twist_of_myth(slug, big, bottom, seed):
    im = vgrad(INDIGO, TEAL); d = ImageDraw.Draw(im); stars(d, 160, seed)
    glow = Image.new("L", (W, H), 0); gd = ImageDraw.Draw(glow); gd.ellipse([W-520, H//2-260, W+20, H//2+260], fill=110)
    glow = glow.filter(ImageFilter.GaussianBlur(80)); im = Image.composite(Image.new("RGB", (W, H), hexc("5A3C12")), im, glow)
    d = ImageDraw.Draw(im); stars(d, 60, seed+1)
    spiral(d, 1020, 360, 3.0, 230, 22, AMBER); d.ellipse([1008, 348, 1032, 372], fill=PARCH)
    maxw = 720
    f2 = fit(d, big, "IMFeENrm28P.ttf", maxw, 128, None, 64)
    f3 = fit(d, [bottom], "IMFeENit28P.ttf", maxw, 56, None, 36)
    total = len(big)*(f2.size+6) + 30 + f3.size
    y = (H - total)//2 - 10
    for line in big:
        shadow_text(d, (60, y), line, f2, PARCH, off=6); y += f2.size + 6
    y += 30
    shadow_text(d, (60, y), bottom, f3, AMBER)
    im.save(OUT + slug + ".png", optimize=True)

gold_and_ruin("gold-and-ruin-01-east-india-company", "EAST INDIA COMPANY", ["IT RULED", "20 MILLION.", "THEN WENT BROKE."], "A company with an army, a famine, and a bailout")
gold_and_ruin("gold-and-ruin-02-mansa-musa", "MANSA MUSA", ["HE GAVE AWAY", "SO MUCH GOLD,", "GOLD LOST VALUE."], "The richest man who ever lived, and what came after")
twist_of_myth("twist-of-myth-01-trishanku", ["STUCK BETWEEN", "HEAVEN", "AND EARTH"], "The king still hanging upside down", 11)
twist_of_myth("twist-of-myth-02-shibi", ["A KING,", "A DOVE,", "AND A SCALE"], "What he put on the other side", 23)
twist_of_myth("twist-of-myth-03-bhasmasura", ["ONE TOUCH.", "ASH."], "The demon who tested his gift on its giver", 37)
print("thumbnails written")
