#!/usr/bin/env python3
"""Generate food-photography-style placeholder images for every recipe.

No network/real photos available, so these are stylized 'plated food' scenes:
a warm wooden-style surface, a round plate, and category-appropriate food
shapes with soft shading. Reads each recipe's category to pick palette/shapes.
"""
import os, glob, math, random, yaml
from PIL import Image, ImageDraw, ImageFilter

IMG_DIR = "public/images/recipes"
REC_DIR = "src/content/recipes"
os.makedirs(IMG_DIR, exist_ok=True)
W, H = 1280, 800

# Warm surface palettes (table/board) per category for variety
SURFACE = {
    "Beef":        [(58, 40, 32), (74, 52, 40)],
    "Chicken":     [(62, 50, 34), (82, 66, 44)],
    "Pork":        [(64, 44, 42), (84, 58, 54)],
    "Fish":        [(40, 50, 56), (54, 66, 72)],
    "Budget Meals":[(50, 52, 40), (66, 70, 52)],
    "Meal Prep":   [(48, 44, 56), (64, 58, 74)],
    "Low Carb":    [(42, 54, 50), (56, 70, 64)],
}
FOOD = {  # main food tone, accent tone
    "Beef":        [(120, 64, 40), (78, 38, 24)],
    "Chicken":     [(196, 150, 86), (150, 104, 52)],
    "Pork":        [(180, 110, 96), (132, 72, 62)],
    "Fish":        [(214, 140, 110), (170, 96, 74)],
    "Budget Meals":[(196, 168, 96), (150, 120, 60)],
    "Meal Prep":   [(150, 120, 80), (108, 84, 54)],
    "Low Carb":    [(140, 96, 70), (100, 64, 46)],
}
GREEN = [(86, 120, 60), (104, 142, 70)]   # garnish/veg
PLATE = (232, 226, 214)
PLATE_RIM = (208, 200, 186)

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def jitter(c, d=14):
    return tuple(max(0, min(255, x + random.randint(-d, d))) for x in c)

def make(slug, category, seed):
    random.seed(seed)
    s1, s2 = SURFACE.get(category, [(60, 50, 44), (80, 66, 56)])
    img = Image.new("RGB", (W, H), s1)
    d = ImageDraw.Draw(img)

    # --- wooden-plank surface with diagonal light ---
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=lerp(s2, s1, t))
    plank = 96
    for x in range(-H, W, plank):
        d.line([(x, 0), (x + H, H)], fill=lerp(s1, (0, 0, 0), 0.18), width=2)
    # soft warm light pool top-left
    glow = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(glow)
    gd.ellipse([-200, -260, 900, 760], fill=70)
    glow = glow.filter(ImageFilter.GaussianBlur(180))
    warm = Image.new("RGB", (W, H), (255, 226, 170))
    img = Image.composite(warm, img, glow.point(lambda p: int(p * 0.5)))
    d = ImageDraw.Draw(img)

    # --- plate (round, centered, with shadow + rim) ---
    cx, cy, r = W // 2, H // 2 + 10, 300
    sh = Image.new("L", (W, H), 0)
    ImageDraw.Draw(sh).ellipse([cx - r - 18, cy - r + 26, cx + r + 30, cy + r + 46], fill=120)
    sh = sh.filter(ImageFilter.GaussianBlur(40))
    img = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), img, sh)
    d = ImageDraw.Draw(img)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PLATE_RIM)
    d.ellipse([cx - r + 26, cy - r + 26, cx + r - 26, cy + r - 26], fill=PLATE)
    d.ellipse([cx - r + 26, cy - r + 26, cx + r - 26, cy + r - 26], outline=lerp(PLATE, (0, 0, 0), 0.06), width=3)

    food, faccent = FOOD.get(category, [(150, 100, 70), (110, 70, 48)])
    inner = r - 70

    def blob(bx, by, br, col, n=22):
        pts = []
        for i in range(n):
            a = 2 * math.pi * i / n
            rad = br * (0.78 + random.random() * 0.34)
            pts.append((bx + math.cos(a) * rad, by + math.sin(a) * rad))
        d.polygon(pts, fill=col)

    cat = category
    if cat == "Beef":  # burger-ish stack / mound of seasoned meat
        for k in range(14):
            a = random.random() * 2 * math.pi
            rad = random.random() * inner * 0.8
            bx, by = cx + math.cos(a) * rad, cy + math.sin(a) * rad
            blob(bx, by, random.randint(46, 78), jitter(food, 20))
        for k in range(7):  # sesame/char specks
            a = random.random() * 2 * math.pi; rad = random.random() * inner * 0.7
            d.ellipse([cx + math.cos(a)*rad-5, cy+math.sin(a)*rad-5, cx+math.cos(a)*rad+5, cy+math.sin(a)*rad+5], fill=jitter(faccent, 10))
    elif cat in ("Chicken", "Pork"):  # 2-3 seared pieces + sauce sheen
        for (ox, oy) in [(-90, -40), (70, 10), (-10, 90)]:
            blob(cx + ox, cy + oy, random.randint(88, 110), jitter(food, 14))
            blob(cx + ox - 10, cy + oy - 14, 40, jitter(lerp(food, (255,235,180), 0.4), 10))
    elif cat == "Fish":  # fillet + lemon wedges
        d.polygon([(cx-150, cy-70),(cx+150, cy-120),(cx+170, cy+70),(cx-130, cy+110)], fill=jitter(food,10))
        for k in range(6):
            a = random.random()*2*math.pi; rad=random.random()*70
            d.line([(cx-150+math.cos(a)*rad, cy), (cx+150, cy+math.sin(a)*rad)], fill=jitter(faccent,12), width=4)
        for (lx, ly) in [(cx+150, cy-130),(cx-160, cy+120)]:  # lemon wedges
            d.pieslice([lx-44, ly-44, lx+44, ly+44], 200, 320, fill=(226, 198, 70))
    elif cat == "Budget Meals":  # rice/grain bed + topping
        blob(cx, cy, inner*0.92, (224, 214, 188), n=30)
        for k in range(16):
            a=random.random()*2*math.pi; rad=random.random()*inner*0.7
            blob(cx+math.cos(a)*rad, cy+math.sin(a)*rad, random.randint(26,44), jitter(food,22))
    elif cat == "Meal Prep":  # three sections (protein / grain / veg)
        d.pieslice([cx-inner, cy-inner, cx+inner, cy+inner], 90, 210, fill=jitter(food,10))
        d.pieslice([cx-inner, cy-inner, cx+inner, cy+inner], 210, 330, fill=(220,210,184))
        d.pieslice([cx-inner, cy-inner, cx+inner, cy+inner], 330, 450, fill=jitter(GREEN[0],14))
    else:  # Low Carb: protein + greens
        blob(cx-40, cy, 130, jitter(food,12))
        for k in range(10):
            a=random.random()*2*math.pi; rad=inner*0.55+random.random()*inner*0.3
            blob(cx+90+math.cos(a)*rad*0.4, cy+math.sin(a)*rad*0.4, random.randint(30,50), jitter(GREEN[1],18))

    # garnish flecks (herbs) for most plates
    if cat not in ("Fish",):
        for k in range(18):
            a = random.random()*2*math.pi; rad = random.random()*inner*0.85
            gx, gy = cx+math.cos(a)*rad, cy+math.sin(a)*rad
            d.ellipse([gx-4, gy-4, gx+5, gy+5], fill=jitter(random.choice(GREEN), 16))

    # subtle vignette
    vig = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vig).ellipse([-260, -200, W+260, H+200], fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(220))
    dark = Image.new("RGB", (W, H), (0, 0, 0))
    img = Image.composite(img, dark, vig)

    img.save(os.path.join(IMG_DIR, f"{slug}.jpg"), "JPEG", quality=86)

count = 0
for f in sorted(glob.glob(os.path.join(REC_DIR, "*.md"))):
    raw = open(f).read()
    fm = yaml.safe_load(raw.split("---", 2)[1])
    slug = os.path.basename(f)[:-3]
    make(slug, fm["category"], seed=sum(ord(c) for c in slug))
    count += 1
print(f"Generated {count} food-style placeholder images.")
