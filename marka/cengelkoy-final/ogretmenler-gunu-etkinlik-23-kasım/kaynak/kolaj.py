# Fotoğraf kolajı üretir: python3 kolaj.py <düzen.json> <çıktı.png>
# düzen.json: {"tip": "full|pblur|p2|p3|p4|big2|big2R|L2", "fotolar": [[yol, fy], ...]}
# 3840x2160, koyu zemin, ince boşluk; her hücre "cover" kırpılır, fy dikey odak (0 üst, 1 alt).
import sys, json
from PIL import Image, ImageOps, ImageFilter, ImageEnhance

W, H, G = 3840, 2160, 24
ZEMIN = (14, 15, 20)
d = json.load(open(sys.argv[1]))
tip, fotolar = d['tip'], d['fotolar']


def ac(yol):
    im = Image.open(yol)
    im.draft('RGB', (W, H))
    im = ImageOps.exif_transpose(im).convert('RGB')
    # çok karanlık fotoğrafları hafifçe aç (gece salonu)
    ort = sum(ImageOps.grayscale(im).resize((64, 64)).getdata()) / 4096
    if ort < 70:
        im = ImageEnhance.Brightness(im).enhance(min(1.35, 80 / max(ort, 30)))
    return im


def cover(im, w, h, fy):
    s = max(w / im.width, h / im.height)
    r = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (r.width - w) // 2
    y = round((r.height - h) * fy)
    return r.crop((x, y, x + w, y + h))


def kutular(tip):
    if tip in ('full', 'pblur'):
        return [(0, 0, W, H)]
    if tip in ('p2', 'p3', 'p4', 'L2'):
        n = {'p2': 2, 'p3': 3, 'p4': 4, 'L2': 2}[tip]
        cw = (W - G * (n + 1)) // n
        return [(G + i * (cw + G), G, cw, H - 2 * G) for i in range(n)]
    if tip in ('big2', 'big2R'):
        bw = round(W * 0.62)
        sw = W - bw - 3 * G
        sh = (H - 3 * G) // 2
        if tip == 'big2':
            return [(G, G, bw, H - 2 * G), (2 * G + bw, G, sw, sh), (2 * G + bw, 2 * G + sh, sw, sh)]
        return [(2 * G + sw, G, bw, H - 2 * G), (G, G, sw, sh), (G, 2 * G + sh, sw, sh)]
    raise ValueError(tip)


tuval = Image.new('RGB', (W, H), ZEMIN)
if tip == 'pblur':
    yol, fy = fotolar[0]
    im = ac(yol)
    arka = cover(im, W, H, 0.5).filter(ImageFilter.GaussianBlur(60))
    tuval = ImageEnhance.Brightness(arka).enhance(0.55)
    h = H - 2 * G
    w = round(im.width * h / im.height)
    tuval.paste(im.resize((w, h), Image.LANCZOS), ((W - w) // 2, G))
else:
    for (x, y, w, h), (yol, fy) in zip(kutular(tip), fotolar):
        tuval.paste(cover(ac(yol), w, h, fy), (x, y))
tuval.save(sys.argv[2])
