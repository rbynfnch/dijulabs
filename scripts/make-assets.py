"""One-time asset generator: logo wordmark, favicons, OG images, placeholder app art.
Run: python3 scripts/make-assets.py  (needs Pillow). Not part of the site build."""
import json, os
from PIL import Image, ImageDraw, ImageFont, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)
IMG3 = os.environ.get("LOGO_HORIZ", "/tmp/claude-0/-home-user/cfe517b2-04d1-5a12-a3df-e02452988de1/images/3.webp")
GRID = json.load(open(os.environ.get("GRID", "/tmp/grid.json")))
INK = (11, 15, 20)
BG = (251, 250, 248)
F = lambda w, s: ImageFont.truetype(f"/usr/share/fonts/opentype/inter/Inter-{w}.otf", s)

# --- wordmark: dark ink with alpha, cropped from the provided horizontal logo
im = Image.open(IMG3).convert("L")
mask = im.point(lambda v: 255 - v if v < 200 else 0)
x0 = 520  # right of the pixel mark
crop = mask.crop((x0, 0, im.width, im.height))
crop = crop.crop(crop.point(lambda v: 255 if v > 40 else 0).getbbox())
w = 640
crop = crop.resize((w, round(crop.height * w / crop.width)), Image.LANCZOS)
wm = Image.new("RGBA", crop.size, INK + (0,))
wm.putalpha(crop)
wm.save(P("src/assets/wordmark.png"), optimize=True)
print("wordmark", wm.size)

# --- pixel mark renderer
def mark(size, bg=None, pad=0.0):
    R, C = len(GRID), len(GRID[0])
    s = size * (1 - 2 * pad)
    cell = s / R
    ox = (size - cell * C) / 2
    oy = size * pad
    img = Image.new("RGBA", (size, size), bg or (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for r, row in enumerate(GRID):
        for c, v in enumerate(row):
            if v:
                col = tuple(int(v[i:i + 2], 16) for i in (0, 2, 4))
                d.rectangle([ox + c * cell, oy + r * cell, ox + (c + 1) * cell - 0.6, oy + (r + 1) * cell - 0.6], fill=col)
    return img

mark(180, BG + (255,), 0.14).convert("RGB").save(P("public/apple-touch-icon.png"))
mark(512, BG + (255,), 0.12).convert("RGB").save(P("public/icon-512.png"))
mark(192, BG + (255,), 0.12).convert("RGB").save(P("public/icon-192.png"))
mark(64, None, 0.02).save(P("public/favicon-64.png"))
mark(32, None, 0.0).save(P("public/favicon-32.png"))

# --- apps (mirror of src/data/apps.ts accents; placeholder art only)
APPS = [
    ("giftly", "Giftly", "Give better. Remember more.", (36, 82, 116), [("People", (91, 110, 225)), ("Gift ideas", (233, 84, 99)), ("Occasions", (59, 130, 246)), ("Budgets", (34, 170, 120))]),
    ("momntm", "MOMNTM", "Build momentum.", (17, 24, 33), [("Today's #1", (255, 138, 61)), ("Deep work", (99, 102, 241)), ("Follow up", (20, 184, 166)), ("Someday", (148, 163, 184))]),
    ("ranch-manager", "Ranch Manager", "Everything in one place.", (74, 92, 62), [("Livestock", (194, 120, 58)), ("Pastures", (84, 140, 80)), ("Supplies", (70, 120, 180)), ("Tasks", (160, 90, 160))]),
]

def rr(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, r, fill=fill, outline=outline, width=width)

def screen(name, accent, rows, variant, dark):
    S = 2
    W, H = 390 * S, 844 * S
    bg = (16, 20, 26) if dark else (248, 248, 247)
    fg = (240, 241, 243) if dark else INK
    sub = (130, 138, 148)
    card = (30, 36, 44) if dark else (255, 255, 255)
    im = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(im)
    d.text((34 * S, 18 * S), "9:41", font=F("SemiBold", 15 * S), fill=fg)
    d.text((W // 2, 72 * S), [name, "Details", "Overview"][variant], font=F("Bold", 24 * S), fill=fg, anchor="mm")
    y = 120 * S
    if variant == 1:
        rr(d, (24 * S, y, W - 24 * S, y + 190 * S), 20 * S, fill=tuple(int(c * .85 + 30) for c in accent))
        d.text((W // 2, y + 95 * S), name[:1], font=F("Bold", 80 * S), fill=(255, 255, 255), anchor="mm")
        y += 214 * S
        for t, w in (("Placeholder screenshot", 0.62), ("Replace with a real capture", 0.8), ("", 0.45)):
            if t:
                d.text((28 * S, y), t, font=F("SemiBold", 16 * S), fill=fg)
                y += 28 * S
            rr(d, (28 * S, y, 28 * S + int((W - 56 * S) * w), y + 10 * S), 5 * S, fill=(*sub,) if dark else (226, 228, 231))
            y += 28 * S
    else:
        for i, (label, col) in enumerate(rows * 2 if variant == 2 else rows):
            rr(d, (24 * S, y, W - 24 * S, y + 64 * S), 16 * S, fill=card, outline=None if dark else (232, 232, 230))
            rr(d, (40 * S, y + 16 * S, 72 * S, y + 48 * S), 9 * S, fill=col)
            d.text((90 * S, y + 32 * S), label if i < 4 else ["Notes", "Archive", "Settings", "Help"][i - 4], font=F("Medium", 17 * S), fill=fg, anchor="lm")
            d.text((W - 44 * S, y + 32 * S), "›", font=F("Medium", 22 * S), fill=sub, anchor="rm")
            y += 78 * S
    rr(d, (W // 2 - 70 * S, H - 22 * S, W // 2 + 70 * S, H - 16 * S), 3 * S, fill=fg)
    return im

for slug, name, tag, accent, rows in APPS:
    dark = slug == "momntm"
    os.makedirs(P("public/apps", slug), exist_ok=True)
    for i in range(3):
        screen(name, accent, rows, i, dark).save(P("public/apps", slug, f"screen-{i + 1}.webp"), quality=84)
    ic = Image.new("RGB", (512, 512), accent)
    ImageDraw.Draw(ic).text((256, 262), name[:1], font=F("Bold", 280), fill=(255, 255, 255), anchor="mm")
    ic.save(P("public/apps", slug, "icon.png"))

    # OG image 1200x630
    og = Image.new("RGB", (1200, 630), BG)
    d = ImageDraw.Draw(og)
    m = mark(380, None, 0.0)
    og.paste(m, (770, 125), m)
    d.text((80, 90), "DIJULABS / APP", font=F("Medium", 22), fill=(120, 126, 134))
    d.text((80, 250), name, font=F("Bold", 96), fill=INK)
    d.text((80, 372), tag, font=F("Regular", 38), fill=(90, 96, 104))
    wm2 = wm.resize((220, round(wm.height * 220 / wm.width)), Image.LANCZOS)
    og.paste(wm2, (80, 520), wm2)
    og.save(P("public/og", f"{slug}.png"), optimize=True)

og = Image.new("RGB", (1200, 630), BG)
d = ImageDraw.Draw(og)
m = mark(420, None, 0.0)
og.paste(m, (720, 105), m)
d.text((80, 190), "Small apps.", font=F("Bold", 92), fill=INK)
d.text((80, 300), "Useful ideas.", font=F("Bold", 92), fill=INK)
d.text((80, 430), "A small digital lab creating useful apps,\ntools, and experiments.", font=F("Regular", 32), fill=(90, 96, 104), spacing=10)
wm2 = wm.resize((260, round(wm.height * 260 / wm.width)), Image.LANCZOS)
og.paste(wm2, (80, 80), wm2)
og.save(P("public/og/default.png"), optimize=True)
print("ok")
