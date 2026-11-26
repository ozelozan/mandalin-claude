# Yakacık Final Okulları - Dünya Çocuk Hakları Günü (20 Kasım) Instagram hikâye videosu, dikey 1080x1920, 30 fps
# Kullanım:  python3 hikaye.py still <kare> [<kare> ...]     -> cikti/_onizleme/ altına tek kare
#            python3 hikaye.py render <cikti.mp4>             -> sessiz video
#            python3 hikaye.py olaylar                        -> ses olaylarını (kare numaraları) JSON yazar
# Konsept: "Hak Ağacı". Okulun girişindeki boş ağaç çocukların çizim ve notlarıyla doldu; video da fotoğraflar
# ağacın beyaz tahtasını doldurana kadar akar. Her fotoğraf, ağaçtaki yapışkan notlar gibi bir "hak" notu taşır.
# Her kare yalnızca kare numarasının fonksiyonudur (render makineden bağımsız, rastgelelik seed'li).
import sys, os, math, json, subprocess, glob
import multiprocessing as mp
import numpy as np
from PIL import Image, ImageOps, ImageFilter, ImageDraw, ImageFont, ImageEnhance

W, H, FPS = 1080, 1920, 30
BANT_Y = 1540
BASE = os.path.dirname(os.path.abspath(__file__))
JOB = os.path.dirname(BASE)
YK = '/Volumes/Mini_MAN/mandalin-claude/marka/yakacik-final'
MEDYA = YK + '/Dünya Çocuk Hakları Günü - Yakacık Final/'
LOGO_ISARET = YK + '/logo/logo-isaret.png'
LOGO_YAZI = YK + '/logo/logo-yazi.png'
FFMPEG = os.path.expanduser('~/tools/bin/ffmpeg')
TMP = os.environ.get('HIKAYE_TMP', '/private/tmp/hikaye-cocuk-haklari')
MARKER = '/System/Library/Fonts/MarkerFelt.ttc'

# palet: logo (lacivert, kırmızı) + panodan (kâğıt, yaprak yeşili, kuru-ağaç kahvesi, yapışkan not renkleri)
KAGIT = (244, 239, 227)
LACIVERT = (19, 28, 81)
KIRMIZI = (203, 54, 49)
YESIL = (47, 143, 62)
YESIL_K = (30, 103, 45)
KAHVE = (122, 90, 60)
KAHVE_K = (92, 66, 44)
NOTLAR = [(255, 217, 59), (255, 143, 177), (168, 224, 99), (127, 214, 232), (255, 179, 71)]

AD = lambda s: 'WhatsApp Image 2026-11-25 at 17.53.' + s + '.jpeg'
FOTO = {1: '19 (1)', 2: '19', 3: '20 (1)', 4: '20 (2)', 5: '20 (3)', 6: '20 (4)', 7: '20 (5)', 8: '20',
        9: '21 (1)', 10: '21 (3)', 11: '21 (4)', 12: '21 (5)', 13: '21', 14: '22 (1)', 15: '22 (2)', 16: '22'}
VIDEO = {1: 'WhatsApp Video 2026-11-25 at 17.53.19.mp4', 2: 'WhatsApp Video 2026-11-25 at 17.53.20.mp4'}

# ---------------- zaman çizelgesi (kare) ----------------
A0, A1 = 0, 90          # boş ağaç + başlık
B0, B1 = 90, 174        # video 1: ağaç doluyor (8,3 sn kaynak ~2,96x hızlı)
C0, C1 = 174, 264       # video 2: "Haklarım varım" (ilk 3 sn, 1x)
GIR, CIK = 16, 9        # giriş / çıkış kare sayısı (giriş çıkıştan uzun)
FOTO_SURE = 42          # 1,4 sn
SAHNELER = []           # (tip, no, metin, süre)
for no, metin in [(6, 'Oynama hakkı'), (12, 'Sağlık hakkı'), (16, 'Bir adı olma hakkı'), (14, 'Korunma hakkı')]:
    SAHNELER.append(('foto', no, metin, FOTO_SURE))
SAHNELER.append(('agac3', 2, ['Çizdiler.', 'Yazdılar.', 'Astılar.'], 84))
for no, metin in [(3, 'Eğitim hakkı'), (4, 'Fikrini söyleme hakkı'), (7, 'Eşit olma hakkı'), (8, 'Yaşama hakkı')]:
    SAHNELER.append(('foto', no, metin, FOTO_SURE))
SAHNELER.append(('agac1', 5, ['Bu ağaç,', 'onların sesi.'], 66))
for no, metin in [(9, 'Dinlenme hakkı'), (10, 'Düşünme hakkı'), (11, 'Katılma hakkı'), (13, 'Beslenme hakkı'), (1, 'Ailesiyle yaşama hakkı')]:
    SAHNELER.append(('foto', no, metin, FOTO_SURE))
BASLA = []
_f = C1
for s in SAHNELER:
    BASLA.append(_f)
    _f += s[3]
E0 = _f                 # final: fotoğraflardan ağaç
E_SURE = 300
N = E0 + E_SURE

# ---------------- yardımcılar ----------------
klamp = lambda x, a=0.0, b=1.0: min(b, max(a, x))


def bezier(x1, y1, x2, y2):
    cx = 3 * x1; bx = 3 * (x2 - x1) - cx; ax = 1 - cx - bx
    cy = 3 * y1; by = 3 * (y2 - y1) - cy; ay = 1 - cy - by
    X = lambda t: ((ax * t + bx) * t + cx) * t
    Y = lambda t: ((ay * t + by) * t + cy) * t
    dX = lambda t: (3 * ax * t + 2 * bx) * t + cx

    def f(x):
        t = klamp(x)
        for _ in range(8):
            e = X(t) - x; d = dX(t)
            if abs(e) < 1e-5 or abs(d) < 1e-6:
                break
            t -= e / d
        return Y(klamp(t))
    return f


DOLLY = bezier(0.55, 0, 0.1, 1)      # ağır kalkış, uzun oturma
TERK = bezier(0.7, 0, 0.84, 0)       # hızlanarak terk
SINUS = bezier(0.37, 0, 0.63, 1)     # kalem çizgisi / tripod pan


def ip(f, f0, f1, a, b, ease=lambda x: x):
    return a + (b - a) * ease(klamp((f - f0) / float(f1 - f0)))


def trupper(s):
    return s.replace('i', 'İ').replace('ı', 'I').upper()


def font(size):
    return ImageFont.truetype(MARKER, size, index=1)   # Marker Felt Wide: tam Türkçe glif


def yazi(text, size, fill, bosluk=0):
    f = font(size)
    l, t, r, b = f.getbbox(text)
    im = Image.new('RGBA', (r - l + 24, b - t + 24), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((12 - l, 12 - t), text, font=f, fill=fill + (255,))
    return im


def sigdir(text, size, maxw, fill):
    while size > 20 and font(size).getlength(text) > maxw:
        size -= 2
    return yazi(text, size, fill)


def gol(im, yaricap, kayma=(0, 18), alfa=95):
    """Alfa kanalından yumuşak gölge: RGBA döndürür (pad dahil)."""
    pad = yaricap * 3
    w, h = im.size
    g = Image.new('RGBA', (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    a = Image.new('L', g.size, 0)
    a.paste(im.getchannel('A'), (pad + kayma[0], pad + kayma[1]))
    a = a.filter(ImageFilter.GaussianBlur(yaricap)).point(lambda v: int(v * alfa / 255))
    g.putalpha(a)
    g.alpha_composite(im, (pad, pad))
    return g


def paste_orta(base, im, cx, cy, mask=None):
    base.paste(im, (int(round(cx - im.width / 2)), int(round(cy - im.height / 2))), im if mask is None else mask)


def paste_alpha(base, im, cx, cy, opaklik=1.0):
    x, y = int(round(cx - im.width / 2)), int(round(cy - im.height / 2))
    if opaklik >= 0.999:
        base.paste(im, (x, y), im)
    else:
        a = im.getchannel('A').point(lambda v: int(v * opaklik))
        base.paste(im, (x, y), a)


def dondur(im, aci):
    return im.rotate(aci, resample=Image.BICUBIC, expand=True)


def olcekle(im, s):
    if abs(s - 1) < 1e-3:
        return im
    return im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BICUBIC)


def ac(yol, uzun):
    im = Image.open(yol)
    im.draft('RGB', (uzun * 2, uzun * 2))
    im = ImageOps.exif_transpose(im).convert('RGB')
    im.thumbnail((uzun, uzun), Image.LANCZOS)
    return ImageEnhance.Color(im).enhance(1.05)


def kes(im, w, h, fx=0.5, fy=0.5, zoom=1.0):
    """cover kırpma: fx/fy = pencerenin görüntü içindeki yatay/dikey konumu (0..1)."""
    s = max(w / im.width, h / im.height) * zoom
    cw, ch = w / s, h / s
    x0 = (im.width - cw) * fx
    y0 = (im.height - ch) * fy
    return im.resize((w, h), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch))


# ---------------- hazır varlıklar (fork ile işçilere miras kalır) ----------------
VAR = {}


def hazirla():
    rng = np.random.RandomState(7)
    # kâğıt zemin: renk + yumuşak leke + ince lif
    z = np.zeros((H, W, 3), np.float32) + np.array(KAGIT, np.float32)
    lk = rng.randn(H // 48 + 2, W // 48 + 2).astype(np.float32)
    lk = np.array(Image.fromarray(lk).resize((W, H), Image.BICUBIC))
    z += lk[..., None] * 3.2
    zim = Image.fromarray(np.clip(z, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(zim, 'RGBA')
    for _ in range(1400):
        x, y = rng.randint(0, W), rng.randint(0, H)
        l = rng.randint(14, 60); a = rng.uniform(0, math.pi)
        d.line([(x, y), (x + l * math.cos(a), y + l * math.sin(a))], fill=(150, 130, 100, rng.randint(10, 26)), width=1)
    VAR['kagit'] = zim
    VAR['gren'] = [rng.randint(-1, 2, (H, W)).astype(np.int16) * 5 for _ in range(4)]
    # fotoğraflar
    VAR['foto'] = {n: ac(MEDYA + AD(FOTO[n]), 1500) for n in FOTO}
    # fotoğraf kartları (beyaz baskı kenarlı + gölge)
    VAR['kart'] = {}
    for n in FOTO:
        if n in (2, 5, 15):
            continue
        VAR['kart'][n] = kart_yap(VAR['foto'][n], 960)
    # logo
    isaret = Image.open(LOGO_ISARET).convert('RGBA').crop((17, 17, 1041, 1041))
    yaz = Image.open(LOGO_YAZI).convert('RGBA')
    yaz = yaz.crop(yaz.getchannel('A').getbbox())
    beyaz = Image.new('RGBA', yaz.size, (255, 255, 255, 0)); beyaz.putalpha(yaz.getchannel('A'))   # koyu zeminde yazı beyaz
    isaret = isaret.resize((150, 150), Image.LANCZOS)
    beyaz = beyaz.resize((470, int(470 * yaz.height / yaz.width)), Image.LANCZOS)
    VAR['isaret'], VAR['yazi'] = isaret, beyaz
    # alt bant (lacivert, yırtık kâğıt kenarı)
    bant = Image.new('RGBA', (W, H - BANT_Y), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bant)
    pts = [(0, 14)]
    x = 0
    while x < W:
        x += rng.randint(18, 46)
        pts.append((min(x, W), rng.randint(0, 22)))
    pts += [(W, bant.height), (0, bant.height)]
    bd.polygon(pts, fill=LACIVERT + (255,))
    VAR['bant'] = bant
    # üst etiket (kâğıt şerit)
    VAR['ust'] = etiket(trupper('20 Kasım · Dünya Çocuk Hakları Günü'), 33, LACIVERT, 8)
    # final ağacı
    ağaç_hazirla()


def kart_yap(foto, genis):
    """foto (4:3) -> beyaz baskı kenarlı kart + gölge."""
    ic = foto.resize((genis - 44, int((genis - 44) * foto.height / foto.width)), Image.LANCZOS)
    k = Image.new('RGBA', (genis, ic.height + 44), (252, 250, 245, 255))
    k.paste(ic, (22, 22))
    return gol(k, 26, (0, 22), 105)


def etiket(text, size, renk, kenar, dolgu=(255, 255, 255), cerceve=KIRMIZI, bosluk=(26, 14)):
    t = yazi(text, size, renk)
    w, h = t.width + bosluk[0] * 2, t.height + bosluk[1] * 2
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 10, fill=dolgu + (255,))
    d.rounded_rectangle((0, 0, w - 1, h - 1), 10, outline=cerceve + (255,), width=kenar)
    im.alpha_composite(t, (bosluk[0], bosluk[1]))
    return gol(im, 10, (0, 8), 90)


def not_yap(text, renk):
    w, h = 600, 270
    im = Image.new('RGBA', (w, h), renk + (255,))
    # hafif kâğıt degradesi + alt kenar kıvrımı
    a = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
    arr = np.array(im).astype(np.float32)
    arr[..., :3] *= (1.0 - 0.07 * a)
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    # satırlara böl
    kel = text.split(' ')
    en_iyi = None
    for sz in range(78, 36, -2):
        f = font(sz)
        for k in range(1, len(kel) + 1):
            satirlar = [' '.join(kel[:k]), ' '.join(kel[k:])] if k < len(kel) else [text]
            if len(kel) == 1:
                satirlar = [text]
            gw = max(f.getlength(s) for s in satirlar if s)
            gh = sum(f.getbbox(s)[3] - f.getbbox(s)[1] + 12 for s in satirlar if s)
            if gw <= w - 80 and gh <= h - 60:
                if en_iyi is None or len(satirlar) <= len(en_iyi[1]):
                    en_iyi = (sz, [s for s in satirlar if s])
                break
        if en_iyi:
            break
    sz, satirlar = en_iyi
    f = font(sz)
    toplam = sum(f.getbbox(s)[3] - f.getbbox(s)[1] + 12 for s in satirlar) - 12
    y = (h - toplam) // 2
    d = ImageDraw.Draw(im)
    for s in satirlar:
        b = f.getbbox(s)
        d.text(((w - (b[2] - b[0])) // 2 - b[0], y - b[1]), s, font=f, fill=LACIVERT)
        y += b[3] - b[1] + 12
    im.putalpha(Image.new('L', (w, h), 255))
    return gol(im, 14, (0, 14), 110)


def bant_yaz(satirlar, boyut, w=None):
    """kâğıt şerit üzerinde 1-2 satır marker yazı (altyazı yerine, sahnenin başlığı)."""
    f = font(boyut)
    gen = max(f.getlength(s) for s in satirlar)
    hh = [f.getbbox(s)[3] - f.getbbox(s)[1] for s in satirlar]
    gw, gh = int(gen) + 90, sum(hh) + 14 * (len(satirlar) - 1) + 56
    im = Image.new('RGBA', (gw, gh), (252, 250, 245, 255))
    d = ImageDraw.Draw(im)
    y = 28
    for s, h_ in zip(satirlar, hh):
        b = f.getbbox(s)
        d.text((45 - b[0], y - b[1]), s, font=f, fill=LACIVERT)
        y += h_ + 14
    im.putalpha(Image.new('L', (gw, gh), 255))
    return gol(im, 14, (0, 12), 110)


def ağaç_hazirla():
    # kâğıttan kesilmiş koruluk + beyaz tahta
    daire = [(250, 640, 200), (400, 550, 215), (600, 520, 225), (790, 570, 215), (870, 680, 175),
             (700, 730, 215), (500, 740, 225), (330, 750, 190), (540, 640, 260)]
    S = 2
    dis = Image.new('L', (W * S, 1000 * S), 0)
    ic = Image.new('L', (W * S, 1000 * S), 0)
    dd, di = ImageDraw.Draw(dis), ImageDraw.Draw(ic)
    for cx, cy, r in daire:
        dd.ellipse(((cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S), fill=255)
        r2 = r - 30
        di.ellipse(((cx - r2) * S, (cy - r2) * S, (cx + r2) * S, (cy + r2) * S), fill=255)
    dis = dis.resize((W, 1000), Image.LANCZOS)
    ic = ic.resize((W, 1000), Image.LANCZOS)
    kat = Image.new('RGBA', (W, 1000), (0, 0, 0, 0))
    yes = Image.new('RGBA', (W, 1000), YESIL + (255,))
    kat.paste(yes, (0, 0), dis)
    # kenara yakın koyu yeşil şerit (kâğıt kalınlığı hissi)
    koyu = Image.new('RGBA', (W, 1000), YESIL_K + (255,))
    ince = ic.filter(ImageFilter.MaxFilter(9))
    kat.paste(koyu, (0, 0), Image.composite(Image.new('L', (W, 1000), 255), Image.new('L', (W, 1000), 0), dis).point(lambda v: v))
    kat.paste(yes, (0, 0), dis.filter(ImageFilter.MinFilter(7)))
    beyaz = Image.new('RGBA', (W, 1000), (250, 248, 242, 255))
    kat.paste(beyaz, (0, 0), ic)
    VAR['ag_kanopi'] = kat
    VAR['ag_ic'] = ic
    # gövde + çimen (kuru ağaç kahvesi)
    g = Image.new('RGBA', (W, 400), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    gd.polygon([(455, 0), (625, 0), (640, 110), (700, 250), (380, 250), (440, 110)], fill=KAHVE + (255,))
    for x0, x1 in [(480, 470), (520, 515), (565, 580), (600, 612)]:
        gd.line([(x0, 10), (x1, 230)], fill=KAHVE_K + (255,), width=5)
    rng = np.random.RandomState(3)
    x = 300
    while x < 790:
        h_ = rng.randint(28, 62)
        gd.polygon([(x, 250), (x + 12, 250 - h_), (x + 24, 250)], fill=YESIL + (255,))
        x += rng.randint(14, 24)
    VAR['ag_govde'] = gd and g
    # kart yerleşimi: 4x4 yarı kayık ızgara
    kon = []
    rng = np.random.RandomState(11)
    for r in range(4):
        for c in range(4):
            cx = 180 + c * 240 + (60 if r % 2 else 0) + rng.randint(-22, 22)
            cy = 400 + r * 140 + rng.randint(-18, 18)
            kon.append((cx, cy, rng.uniform(-8, 8)))
    sira = list(range(16))
    rng.shuffle(sira)
    VAR['ag_kon'] = [kon[i] for i in sira]


# ---------------- ortak çizimler ----------------
def alt_bant(im):
    im.paste(VAR['bant'], (0, BANT_Y), VAR['bant'])
    cy = 1652
    toplam = 150 + 34 + VAR['yazi'].width
    x0 = (W - toplam) // 2
    im.paste(VAR['isaret'], (x0, cy - 75), VAR['isaret'])
    im.paste(VAR['yazi'], (x0 + 150 + 34, cy - VAR['yazi'].height // 2), VAR['yazi'])


def gren_ekle(im, f, genlik):
    a = np.asarray(im, dtype=np.int16)
    g = VAR['gren'][(f // 2) % 4]      # ikili çekim: iki karede bir değişen gren
    a = a + (g * genlik // 5)[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def tam_ekran(kaynak, f, yerel, sure, fx0, fx1, zoom0, zoom1, fy=0.5, pan=lambda x: x):
    p = klamp(yerel / float(sure))
    fx = fx0 + (fx1 - fx0) * pan(p)
    z = zoom0 + (zoom1 - zoom0) * p
    return kes(kaynak, W, H, fx, fy, z)


def damga_olcek(f, f0):
    """damga: easing yok; 0 kare öncesi görünmez, 2 karede 1.35 -> 1."""
    if f < f0:
        return None
    k = f - f0
    return 1.35 if k == 0 else (1.12 if k == 1 else 1.0)


def yazi_sil(im, ilerleme):
    """soldan sağa açılan maske (kalemle yazılmış gibi)."""
    if ilerleme >= 1:
        return im
    w = int(im.width * ilerleme)
    a = im.getchannel('A')
    m = Image.new('L', im.size, 0)
    m.paste(255, (0, 0, w, im.height))
    out = im.copy()
    out.putalpha(Image.fromarray(np.minimum(np.array(a), np.array(m))))
    return out


# ---------------- sahne çizimleri ----------------
def sahne_bos_agac(im, f):
    foto = VAR['foto'][15]
    yer = f - A0
    ek = tam_ekran(foto, f, yer, A1 - A0, 0.5, 0.5, 1.0, 1.07, fy=0.5)
    im.paste(ek, (0, 0))
    # alt karartma (logo bandına geçiş)
    v = np.linspace(0, 1, 420, dtype=np.float32)[:, None, None]
    # başlık etiketleri
    y = 430
    k = damga_olcek(f, 14)
    if k:
        e1 = etiket(trupper('20 Kasım'), 118, LACIVERT, 9)
        paste_alpha(im, dondur(olcekle(e1, k), -2.5), 540, 345)
    if f >= 30:
        e2 = etiket(trupper('Dünya Çocuk Hakları Günü'), 70, LACIVERT, 8, bosluk=(32, 18))
        p = SINUS(klamp((f - 30) / 16.0))
        paste_alpha(im, dondur(yazi_sil(e2, p), 1.2), 540, 480)


def sahne_video(im, f, v, f0, f1, hiz):
    yol = '%s/v%d/%%04d.jpg' % (TMP, v)
    n = len(glob.glob('%s/v%d/*.jpg' % (TMP, v)))
    idx = min(n, max(1, int((f - f0) * hiz) + 1))
    fr = Image.open(yol % idx).convert('RGB')
    fr = fr.resize((W, H), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 55, 2))
    im.paste(fr, (0, 0))


def kart_ciz(im, n, f_yerel, sure, yon, aci0, cy=770):
    """foto kartı: giriş (dolly), tutuş (yavaş yaklaşma), çıkış (hızlanarak terk). Geri döndürür (dx, dy) kart ofseti."""
    kart = VAR['kart'][n]
    pg = DOLLY(klamp(f_yerel / float(GIR)))
    pc = TERK(klamp((f_yerel - sure) / float(CIK)))
    mesafe = 1500
    dx = yon[0] * mesafe * (1 - pg) - yon[0] * mesafe * pc
    dy = yon[1] * mesafe * (1 - pg) - yon[1] * mesafe * pc
    aci = aci0 + yon[0] * 9 * (1 - pg) - yon[0] * 13 * pc + (yon[1] * 4 * (1 - pg) if yon[0] == 0 else 0)
    zoom = 1.0 + 0.035 * klamp(f_yerel / float(sure))
    k2 = dondur(olcekle(kart, zoom), aci)
    paste_alpha(im, k2, 540 + dx, cy + dy)
    return dx, dy


YONLER = [(1, 0), (-1, 0), (0, 1), (1, 0), (-1, 0)]
ACILAR = [-2.4, 1.8, -1.2, 2.2, -1.8]


def sahne_foto(im, f, i, sahne):
    tip, no, metin, sure = sahne
    yerel = f - BASLA[i]
    k = sum(1 for s in SAHNELER[:i] if s[0] == 'foto')
    dx, dy = kart_ciz(im, no, yerel, sure, YONLER[k % 5], ACILAR[k % 5])
    # not: giriş bittikten sonra damga gibi çarpar (18. kare)
    sc = damga_olcek(yerel, 18)
    if sc:
        notkagidi = not_yap(trupper(metin) if False else metin, NOTLAR[k % 5])
        aci = (-3.5, 3.0, -2.0, 3.5, -3.0)[k % 5]
        paste_alpha(im, dondur(olcekle(notkagidi, sc), aci), 540 + (150 if k % 2 == 0 else -150) + dx, 1175 + dy)


def sahne_agac(im, f, i, sahne):
    tip, no, satirlar, sure = sahne
    yerel = f - BASLA[i]
    foto = VAR['foto'][no]
    pg = DOLLY(klamp(yerel / float(GIR)))
    pc = TERK(klamp((yerel - sure) / float(CIK)))
    dx = int(W * (1 - pg) - W * pc)
    if tip == 'agac3':
        ek = tam_ekran(foto, f, yerel, sure, 0.0, 1.0, 1.0, 1.0, pan=SINUS)   # üç ağaç boyunca tripod pan
    else:
        ek = tam_ekran(foto, f, yerel, sure, 0.5, 0.5, 1.0, 1.09)
    im.paste(ek, (dx, 0))
    # kısa yazı şeritleri (sahne başlığı): kalemle açılır
    if tip == 'agac3':
        for j, s in enumerate(satirlar):
            f0 = 22 + j * 20
            if yerel >= f0 and yerel < sure + CIK:
                b = bant_yaz([s], 84)
                p = SINUS(klamp((yerel - f0) / 12.0))
                paste_alpha(im, dondur(yazi_sil(b, p), (-2.0, 1.6, -1.2)[j]), 540 - 210 + (j % 2) * 420 + dx, 470 + j * 190)
    else:
        if yerel >= 20:
            b = bant_yaz(satirlar, 84)
            p = SINUS(klamp((yerel - 20) / 14.0))
            paste_alpha(im, dondur(yazi_sil(b, p), -1.8), 540 + dx, 1270)


def sahne_final(im, f):
    y = f - E0
    # üst etiket
    paste_alpha(im, VAR['ust'], 540, 268)
    # gövde
    im.paste(VAR['ag_govde'], (0, 940 - 20), VAR['ag_govde'])
    # koruluk (yeşil) + beyaz tahta, sonra kartlar
    kat = VAR['ag_kanopi'].copy()
    ic = VAR['ag_ic']
    kartlar = Image.new('RGBA', (W, 1000), (0, 0, 0, 0))
    for sira, (cx, cy, aci) in enumerate(VAR['ag_kon']):
        f0 = 6 + sira * 4
        if y < f0:
            continue
        p = DOLLY(klamp((y - f0) / 9.0))
        no = [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 2][sira]
        kk = VAR['mini'][no]
        s = 0.35 + 0.65 * p
        k2 = dondur(olcekle(kk, s), aci)
        kartlar.alpha_composite(k2, (int(cx - k2.width / 2), int(cy - k2.height / 2)))
    # kartları beyaz tahta dışına taşırma
    a = np.minimum(np.array(kartlar.getchannel('A')), np.array(ic))
    kartlar.putalpha(Image.fromarray(a))
    kat.alpha_composite(kartlar)
    g = gol(kat, 16, (0, 14), 90)
    pad = 16 * 3
    im.paste(g, (-pad, 30 - pad), g)
    # metin satırları
    satir = [('Her çocuk eşit.', 100, 84), ('Her çocuk değerli.', 150, 84), ('Her çocuğun hakları saklı.', 205, 92)]
    for j, (s, f0, sz) in enumerate(satir):
        if y < f0:
            continue
        t = sigdir(s, sz, 960, LACIVERT)
        p = SINUS(klamp((y - f0) / 18.0))
        if j == 2:
            t = sigdir(s, 92, 950, LACIVERT)
        paste_alpha(im, yazi_sil(t, p), 540, (1262, 1352, 1445)[j])
    # son satırın altına kırmızı çizgi (kalemle)
    if y >= 205 + 20:
        p = SINUS(klamp((y - 225) / 16.0))
        d = ImageDraw.Draw(im)
        x0, x1 = 90, 90 + int(900 * p)
        d.line([(x0, 1500), (x1, 1496)], fill=KIRMIZI, width=7)


def kare(f):
    im = VAR['kagit'].copy()
    paper = True
    if f < A1:
        sahne_bos_agac(im, f)
    elif f < B1:
        sahne_video(im, f, 1, B0, B1, 249 / 84.0)
        yerel = f - B0
        if yerel >= 22:
            b = bant_yaz(['Ağaç, çocukların', 'çizimleriyle doldu.'], 70)
            paste_alpha(im, dondur(yazi_sil(b, SINUS(klamp((yerel - 22) / 14.0))), -1.8), 540, 1250)
    elif f < C1:
        sahne_video(im, f, 2, C0, C1, 1.0)
    elif f < E0:
        if f > C1 + 0:
            pass
        # önceki sahnelerin çıkışı + mevcut sahne
        # önce video 2'yi (son) arka planda tut: ilk sahne girerken altta kalır
        i0 = 0
        for i, s in enumerate(SAHNELER):
            if BASLA[i] <= f < BASLA[i] + s[3] + CIK:
                pass
        # arka katman: video 2 son karesi, ilk sahnenin girişi bitene kadar
        if f < BASLA[0] + GIR:
            sahne_video(im, C1 - 1, 2, C0, C1, 1.0)
        # üst etiket (kâğıt zeminde)
        paste_alpha(im, VAR['ust'], 540, 268)
        for i, s in enumerate(SAHNELER):
            if BASLA[i] <= f < BASLA[i] + s[3] + CIK:
                if s[0] == 'foto':
                    sahne_foto(im, f, i, s)
                else:
                    sahne_agac(im, f, i, s)
    else:
        sahne_final(im, f)
    alt_bant(im)
    im = gren_ekle(im, f, 1 if f >= C1 else 2)
    return im


def kare_bayt(f):
    return kare(f).tobytes()


def init():
    hazirla()
    VAR['mini'] = {n: kart_yap_mini(VAR['foto'][n]) for n in FOTO}


def kart_yap_mini(foto):
    w = 270
    ic = foto.resize((w - 16, int((w - 16) * foto.height / foto.width)), Image.LANCZOS)
    k = Image.new('RGBA', (w, ic.height + 16), (252, 250, 245, 255))
    k.paste(ic, (8, 8))
    return k


def olaylar():
    o = {'fps': FPS, 'toplam': N, 'damga': [14], 'not': [], 'giris': [], 'cizgi': [], 'final': E0}
    k = 0
    for i, s in enumerate(SAHNELER):
        o['giris'].append(BASLA[i])
        if s[0] == 'foto':
            o['not'].append(BASLA[i] + 18)
    o['final_kart'] = [E0 + 6 + j * 4 for j in range(16)]
    o['final_satir'] = [E0 + 100, E0 + 150, E0 + 205]
    return o


def videolari_ac():
    for v in (1, 2):
        d = '%s/v%d' % (TMP, v)
        os.makedirs(d, exist_ok=True)
        if not glob.glob(d + '/*.jpg'):
            subprocess.run([FFMPEG, '-v', 'error', '-y', '-i', MEDYA + VIDEO[v], '-vf', 'fps=30', '-q:v', '2', d + '/%04d.jpg'], check=True)


if __name__ == '__main__':
    kom = sys.argv[1]
    videolari_ac()
    if kom == 'olaylar':
        print(json.dumps(olaylar(), indent=1))
        sys.exit()
    init()
    if kom == 'still':
        od = JOB + '/cikti/_onizleme'
        os.makedirs(od, exist_ok=True)
        for f in sys.argv[2:]:
            kare(int(f)).save('%s/k%04d.png' % (od, int(f)))
    elif kom == 'render':
        cikti = sys.argv[2]
        p = subprocess.Popen([FFMPEG, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (W, H), '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', cikti], stdin=subprocess.PIPE)
        with mp.get_context('fork').Pool(12) as pool:
            for k, b in enumerate(pool.imap(kare_bayt, range(N), chunksize=4)):
                p.stdin.write(b)
                if k % 100 == 0:
                    print('kare', k, '/', N, flush=True)
        p.stdin.close(); p.wait()
        print('bitti', cikti)
