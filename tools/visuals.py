"""Outils de dessin pour les visuels GoToDeco (Pillow).

Usage : sys.path.insert(0, "tools"); from visuals import *
Formats : STORY = (1080, 1920) ; POST = (1080, 1350) (4:5, s'affiche sans recadrage dans le fil).
"""
import base64, io, re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
BRAND = ROOT / "brand"
STORY, POST = (1080, 1920), (1080, 1350)

# Charte (voir brand/brief.md)
TURQ = (11, 174, 200); TURQ_DARK = (8, 120, 142); TURQ_DEEP = (6, 74, 92)
TURQ_LIGHT = (140, 230, 247); INK = (28, 32, 38); MUTE = (120, 128, 138)
BG_LIGHT = (247, 249, 250); WHITE = (255, 255, 255); AMBER = (238, 170, 84)


def font(weight, size):
    """weight : 300, 500, 600, 700 ou 800."""
    return ImageFont.truetype(str(BRAND / "fonts" / f"Montserrat-{weight}.ttf"), size)


def gradient(size, top, bottom, power=1.0):
    w, h = size
    img = Image.new("RGB", size); d = ImageDraw.Draw(img)
    for y in range(h):
        t = (y / (h - 1)) ** power
        d.line([(0, y), (w, y)], fill=tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))
    return img.convert("RGBA")


def soft_circles(img, color=(255, 255, 255), alpha=16):
    """Cercles décoratifs translucides en haut à droite et en bas à gauche."""
    w, h = img.size
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    d.ellipse([w - 380, -220, w + 200, 360], fill=(*color, alpha))
    d.ellipse([-260, h - 480, 220, h + 60], fill=(*color, int(alpha * 0.75)))
    return Image.alpha_composite(img, layer)


def text_w(draw, text, f):
    return draw.textlength(text, font=f)


def draw_text(draw, xy, text, f, fill, align="left", width=None, tracking=0):
    """Texte d'un bloc (crénage correct). align='center' centre dans `width` à partir de x.
    tracking > 0 : lettres espacées (réservé aux petites capitales)."""
    x, y = xy
    if tracking:
        total = sum(draw.textlength(c, font=f) for c in text) + tracking * (len(text) - 1)
        if align == "center": x = x + (width - total) / 2
        for c in text:
            draw.text((x, y), c, font=f, fill=fill); x += draw.textlength(c, font=f) + tracking
        return
    if align == "center":
        x = x + (width - text_w(draw, text, f)) / 2
    draw.text((x, y), text, font=f, fill=fill)


def wrap(draw, text, f, max_width):
    """Coupe un texte en lignes tenant dans max_width."""
    lines, cur = [], ""
    for word in text.split():
        test = f"{cur} {word}".strip()
        if text_w(draw, test, f) <= max_width: cur = test
        else:
            if cur: lines.append(cur)
            cur = word
    if cur: lines.append(cur)
    return lines


def fits(draw, text, f, max_width):
    return text_w(draw, text, f) <= max_width


def contrast(c1, c2):
    """Ratio de contraste WCAG ; viser > 4.5 pour le texte."""
    def lum(c):
        def ch(v):
            v /= 255
            return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
        return 0.2126 * ch(c[0]) + 0.7152 * ch(c[1]) + 0.0722 * ch(c[2])
    a, b = sorted((lum(c1), lum(c2)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def phone(screenshot_path, width=460):
    """Capture d'écran dans un cadre de téléphone (RGBA)."""
    shot = Image.open(screenshot_path).convert("RGB")
    sw = width; sh = int(sw * shot.height / shot.width)
    sh = min(sh, int(sw * 19.5 / 9))
    shot = shot.resize((sw, int(sw * shot.height / shot.width)), Image.LANCZOS).crop((0, 0, sw, sh))
    r = int(sw * 0.09); bz = max(10, int(sw * 0.028))
    mask = Image.new("L", (sw, sh), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, sw, sh], radius=r, fill=255)
    out = Image.new("RGBA", (sw + 2 * bz, sh + 2 * bz), (0, 0, 0, 0)); d = ImageDraw.Draw(out)
    d.rounded_rectangle([0, 0, sw + 2 * bz - 1, sh + 2 * bz - 1], radius=r + bz, fill=(22, 24, 28, 255))
    s = shot.convert("RGBA"); s.putalpha(mask); out.alpha_composite(s, (bz, bz))
    iw = int(sw * 0.2); d.rounded_rectangle([(out.width - iw) // 2, bz + 8, (out.width + iw) // 2, bz + 28], radius=10, fill=(22, 24, 28, 255))
    return out


def with_shadow(base, element, xy, blur=18, alpha=0.4, offset=(6, 12)):
    sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
    blk = Image.new("RGBA", element.size, (0, 0, 0, 0)); blk.putalpha(element.split()[3].point(lambda v: int(v * alpha)))
    sh.alpha_composite(blk, (xy[0] + offset[0], xy[1] + offset[1]))
    out = Image.alpha_composite(base, sh.filter(ImageFilter.GaussianBlur(blur)))
    out.alpha_composite(element, xy)
    return out


def parapente_icon(size, white=False):
    """Pictogramme du logo. Bitmap natif de 412 px : ne pas dépasser size=400."""
    svg = (BRAND / "logo.svg").read_text(encoding="utf-8", errors="ignore")
    raw = Image.open(io.BytesIO(base64.b64decode(re.search(r"data:image/png;base64,([A-Za-z0-9+/=]+)", svg).group(1)))).convert("RGBA")
    px = raw.load(); w, h = raw.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if r > 245 and g > 245 and b > 245: px[x, y] = (0, 0, 0, 0)
            elif white: px[x, y] = (255, 255, 255, a)
    raw = raw.crop(raw.getbbox())
    size = min(size, 400)
    return raw.resize((size, int(size * raw.height / raw.width)), Image.LANCZOS)


def save_jpeg(img, path):
    """Instagram n'accepte que le JPEG."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(path, "JPEG", quality=92, optimize=True)
    return path
