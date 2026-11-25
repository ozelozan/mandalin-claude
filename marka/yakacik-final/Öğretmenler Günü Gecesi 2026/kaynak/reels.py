# Yakacık Final Okulları - Öğretmenler Günü Gecesi 2026 fotoğraf Reels'i (dikey 1080x1920, 48 sn)
# Kullanım: python3 reels.py <çalışma-klasörü> <çıktı.mp4>
# Fotoğraflar Çengelköy Final etkinlik klasöründen (Ozan'ın seçimi); müzik: muzik/fon-muzigi-hareketli.mp3
# (Magnific / ElevenLabs Music v2, sözsüz, 120 BPM, vuruşlar 0.5 sn katlarında, son vuruş 47.0 sn).
# Yapı: 5 masa kolajı (iki yatay fotoğraf üst üste, 8 vuruş), 10 plaket (dikey tam ekran, 5 vuruş),
# b90'da (45 sn) beyaz flaşla yalnızca Yakacık Final logosu. Köşede sabit "9. Yılımız" sticker'ı.
import sys, os, math, subprocess
from multiprocessing import Pool
from PIL import Image, ImageOps, ImageFilter, ImageEnhance, ImageDraw, ImageFont, ImageChops

W, H, FPS = 1080, 1920, 25
B = 0.5                       # vuruş (sn)
SURE = 48.0
N = int(SURE * FPS)
EV = '/Volumes/Mini_MAN/mandalin-claude/marka/cengelkoy-final/ogretmenler-gunu-etkinlik-23-kasım/fotoğraflar/'
YK = '/Volumes/Mini_MAN/mandalin-claude/marka/yakacik-final'
MUZIK = YK + '/Öğretmenler Günü Gecesi 2026/muzik/fon-muzigi-hareketli.mp3'
LOGO = YK + '/logo/logo-tam.png'
FFMPEG = os.path.expanduser('~/tools/bin/ffmpeg')
NAVY, RED, WHITE = (19, 28, 81), (203, 54, 49), (255, 255, 255)
F_BI = '/System/Library/Fonts/Supplemental/Arial Bold Italic.ttf'
F_BL = '/System/Library/Fonts/Supplemental/Arial Black.ttf'
F_B = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
ma = lambda n: EV + 'masada fotoğraflar/DSC0' + str(n) + '.JPG'
pl = lambda n: EV + 'plaket/DSC0' + str(n) + '.JPG'

# ---- plan (vuruş cinsinden) ----
CEKIM = []
b = 0
for i, (a_, c_) in enumerate([(4731, 4737), (4730, 4738), (4749, 4751), (4752, 4764), (4767, 4769)]):
    CEKIM.append(dict(tip='cift', fotolar=[ma(a_), ma(c_)], b0=b, b1=b + 8, baslik=(i == 0)))
    b += 8
# plaketler Ozan'ın sırasıyla: 1. kurucu, 2. kurucu, 5, 6
for n in [4931, 4934, 4940, 4944, 4945, 4948, 4955, 4958, 4950, 4952]:
    CEKIM.append(dict(tip='tek', fotolar=[pl(n)], b0=b, b1=b + 5))   # 2.5 sn
    b += 5
CEKIM.append(dict(tip='logo', fotolar=[], b0=b, b1=SURE / B))
GECIS = ['whip', 'serit', 'zoom', 'iris', 'yukari', 'whip', 'flash', 'zoom', 'serit', 'iris', 'whip', 'yukari', 'zoom', 'serit', 'flash']
TD = 8   # geçiş kare sayısı


def ac(yol, uzun):
    im = Image.open(yol)
    im.draft('RGB', (uzun * 2, uzun * 2))
    im = ImageOps.exif_transpose(im).convert('RGB')
    im.thumbnail((uzun, uzun), Image.LANCZOS)
    ort = sum(ImageOps.grayscale(im).resize((64, 64)).getdata()) / 4096
    if ort < 80:
        im = ImageEnhance.Brightness(im).enhance(min(1.3, 88 / max(ort, 30)))
    im = ImageEnhance.Color(im).enhance(1.06)
    return im


def cover(im, w, h, fy=0.45):
    s = max(w / im.width, h / im.height)
    r = im.resize((math.ceil(im.width * s), math.ceil(im.height * s)), Image.LANCZOS)
    x, y = (r.width - w) // 2, round((r.height - h) * fy)
    return r.crop((x, y, x + w, y + h))


def kb(img, w, h, q, yon):
    """img (w*1.12, h*1.12) içinden yavaş yakınlaşma/uzaklaşma"""
    z = 1.0 + 0.10 * (q if yon else 1 - q)    # 1.00 -> 1.10 (kaynak 1.12 kat büyük)
    cw, ch = img.width / z, img.height / z
    x, y = (img.width - cw) / 2, (img.height - ch) / 2
    return img.resize((w, h), Image.BILINEAR, box=(x, y, x + cw, y + ch))


def ease(t): return 1 - (1 - t) ** 3
def ease_io(t): return t * t * (3 - 2 * t)


class Kaynak:
    def __init__(self):
        self.c = {}

    def get(self, yol, w, h, fy=0.45):
        k = (yol, w, h)
        if k not in self.c:
            self.c[k] = cover(ac(yol, max(w, h) * 2), round(w * 1.12), round(h * 1.12), fy)
        return self.c[k]


KY = Kaynak()
CT, CB_ = (260, 980), (1160, 1880)   # üst bant sticker için boş kalır   # çift düzende üst ve alt fotoğrafın y aralığı (1080x720)


def sticker():
    s = 180
    im = Image.new('RGBA', (s + 60, s + 60), (0, 0, 0, 0))
    gol = Image.new('L', im.size, 0)
    ImageDraw.Draw(gol).ellipse((34, 40, 34 + s, 40 + s), fill=130)
    im.putalpha(gol.filter(ImageFilter.GaussianBlur(10)))
    d = ImageDraw.Draw(im)
    o = 30
    d.ellipse((o, o, o + s, o + s), fill=WHITE)
    d.ellipse((o + 8, o + 8, o + s - 8, o + s - 8), fill=NAVY)
    d.ellipse((o + 16, o + 16, o + s - 16, o + s - 16), outline=RED, width=3)
    f1 = ImageFont.truetype(F_BL, 80)
    f2 = ImageFont.truetype(F_B, 21)
    cx = o + s / 2
    d.text((cx + 4, o + s * 0.43), '9.', font=f1, fill=WHITE, anchor='mm')
    d.text((cx, o + s * 0.74), 'YILIMIZ', font=f2, fill=WHITE, anchor='mm')
    return im.rotate(-8, resample=Image.BICUBIC, expand=True)


STK = None
LOGO_IM = None


def cekim_kare(i, t):
    """i. çekimin t (sn, mutlak) anındaki karesi (RGB)"""
    c = CEKIM[i]
    t0, t1 = c['b0'] * B, c['b1'] * B
    q = min(max((t - t0) / (t1 - t0), 0), 1)
    if c['tip'] == 'tek':
        src = KY.get(c['fotolar'][0], W, H, 0.42)
        return kb(src, W, H, q, i % 2 == 0)
    if c['tip'] == 'logo':
        tv = Image.new('RGB', (W, H), WHITE)
        lt = t - t0
        e = ease(min(max(lt / 0.6, 0), 1))
        pul = 1 + 0.035 * math.exp(-((t - 47.0) / 0.12) ** 2)   # son vuruşta hafif nabız
        s = (0.86 + 0.14 * e) * pul
        lw = round(LOGO_IM.width * s)
        lg = LOGO_IM.resize((lw, round(LOGO_IM.height * s)), Image.LANCZOS)
        if e < 1:
            lg.putalpha(lg.split()[3].point(lambda v: int(v * e)))
        tv.paste(lg, ((W - lg.width) // 2, (H - lg.height) // 2 - 40), lg)
        return tv
    # çift: lacivert zemin, üstte foto, ortada bant, altta foto 2 vuruş sonra sağdan kayarak
    tv = Image.new('RGB', (W, H), NAVY)
    lt = t - t0
    a, bb = KY.get(c['fotolar'][0], 1080, 720), KY.get(c['fotolar'][1], 1080, 720)
    tv.paste(kb(a, 1080, 720, q, True), (0, CT[0]))
    gir = min(max((lt - 2 * B + 0.36) / 0.36, 0), 1)       # alt foto: 2. vuruşa oturur
    if gir > 0:
        x = round((1 - ease(gir)) * 1080)
        tv.paste(kb(bb, 1080, 720, q, False), (x, CB_[0]))
    d = ImageDraw.Draw(tv)
    d.rectangle((0, CT[1], W, CB_[0]), fill=NAVY)
    d.rectangle((0, CT[1] + 6, round(W * ease(min(max(lt / 0.8, 0), 1))), CT[1] + 12), fill=RED)
    if c['baslik']:
        al = ease(min(max((lt - 0.3) / 0.6, 0), 1))
        f1 = ImageFont.truetype(F_BI, 58)
        f2 = ImageFont.truetype(F_B, 30)
        katman = Image.new('RGBA', (W, CB_[0] - CT[1]), (0, 0, 0, 0))
        dk = ImageDraw.Draw(katman)
        dk.text((W / 2, 78), 'Öğretmenler Günü Gecesi', font=f1, fill=WHITE + (int(255 * al),), anchor='mm')
        dk.text((W / 2, 138), '23 KASIM 2026', font=f2, fill=(230, 232, 240, int(255 * al)), anchor='mm')
        tv.paste(katman, (0, CT[1] + round((1 - al) * 14)), katman)
    return tv


def yatay_bulanik(im, g):
    if g < 2:
        return im
    k = max(1, int(g))
    return im.resize((max(1, W // k), H), Image.BILINEAR).resize((W, H), Image.BILINEAR)


def gecis(tip, A, Bm, p):
    if tip == 'whip':
        e = ease_io(p); off = round(e * W)
        tv = Image.new('RGB', (W, H)); tv.paste(A, (-off, 0)); tv.paste(Bm, (W - off, 0))
        return yatay_bulanik(tv, 1 + 14 * math.sin(math.pi * p))
    if tip == 'yukari':
        e = ease_io(p); off = round(e * H)
        tv = Image.new('RGB', (W, H)); tv.paste(A, (0, -off)); tv.paste(Bm, (0, H - off))
        g = 1 + 10 * math.sin(math.pi * p)
        return tv.resize((W, max(1, int(H / g))), Image.BILINEAR).resize((W, H), Image.BILINEAR) if g > 2 else tv
    if tip == 'zoom':
        if p < 0.5:
            z = 1 + 0.5 * ease_io(p * 2); im = A
        else:
            z = 1.35 - 0.35 * ease(p * 2 - 1); im = Bm
        cw, ch = W / z, H / z
        r = im.resize((W, H), Image.BILINEAR, box=((W - cw) / 2, (H - ch) / 2, (W + cw) / 2, (H + ch) / 2))
        g = 6 * math.sin(math.pi * p)
        return r.filter(ImageFilter.GaussianBlur(g)) if g > 0.5 else r
    if tip == 'flash':
        r = A if p < 0.5 else Bm
        w = 1 - abs(p - 0.5) * 2
        return Image.blend(r, Image.new('RGB', (W, H), WHITE), min(1, w * 1.2))
    if tip == 'iris':
        rad = ease(p) * math.hypot(W, H) / 2 * 1.05
        m = Image.new('L', (W, H), 0)
        ImageDraw.Draw(m).ellipse((W / 2 - rad, H / 2 - rad, W / 2 + rad, H / 2 + rad), fill=255)
        tv = Image.composite(Bm, A, m)
        ImageDraw.Draw(tv).ellipse((W / 2 - rad, H / 2 - rad, W / 2 + rad, H / 2 + rad), outline=WHITE, width=10)
        return tv
    if tip == 'serit':
        # lacivert ve kırmızı çapraz şeritler aşağıdan yukarı süpürür, ortada çekim değişir
        tv = (A if p < 0.5 else Bm).copy()
        d = ImageDraw.Draw(tv)
        for k, (renk, gec) in enumerate([(RED, 0.0), (NAVY, 0.12)]):
            pp = min(max((p - gec) / 0.88, 0), 1)
            ust = H + 600 - pp * (H + 1800)
            kal = 700
            d.polygon([(0, ust + 300), (W, ust), (W, ust + kal), (0, ust + kal + 300)], fill=renk)
        return tv
    return Bm


def kare(f):
    t = f / FPS
    i = max(k for k, c in enumerate(CEKIM) if c['b0'] * B <= t + 1e-6)
    tv = None
    for j in (i, i + 1):   # yakındaki kesim
        if 0 < j < len(CEKIM):
            kes = CEKIM[j]['b0'] * B
            p = (t - (kes - TD / 2 / FPS)) / (TD / FPS)
            if 0 <= p < 1:
                tip = 'flash' if CEKIM[j]['tip'] == 'logo' else GECIS[(j - 1) % len(GECIS)]
                tv = gecis(tip, cekim_kare(j - 1, t), cekim_kare(j, t), p)
    if tv is None:
        tv = cekim_kare(i, t)
    # sticker: logo kartına kadar sabit, ilk saniyede hafif büyüyerek gelir
    logo_t = CEKIM[-1]['b0'] * B
    a = min(max(t / 0.4, 0), 1) * (1 - min(max((t - (logo_t - 0.25)) / 0.25, 0), 1))
    if a > 0:
        s = STK if a >= 1 else STK.resize((max(1, round(STK.width * (0.7 + 0.3 * a))), max(1, round(STK.height * (0.7 + 0.3 * a)))), Image.BICUBIC)
        if a < 1:
            s = s.copy(); s.putalpha(s.split()[3].point(lambda v: int(v * a)))
        tv.paste(s, (round(930 - s.width / 2), round(178 - s.height / 2)), s)   # sağ üst, Reels başlığının altında
    return tv


def parca(arg):
    k, f0, f1, out = arg
    global STK, LOGO_IM
    STK = sticker()
    lg = Image.open(LOGO).convert('RGBA'); lg = lg.crop(lg.split()[3].getbbox())
    LOGO_IM = lg.resize((420, round(420 * lg.height / lg.width)), Image.LANCZOS)   # dengeli: ~1/2.5 genişlik
    pr = subprocess.Popen([FFMPEG, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-crf', '14', '-preset', 'fast', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for f in range(f0, f1):
        pr.stdin.write(kare(f).tobytes())
    pr.stdin.close(); pr.wait()
    return out


if __name__ == '__main__':
    Wd, OUT = sys.argv[1], sys.argv[2]
    os.makedirs(Wd, exist_ok=True)
    P = 8
    sinir = [round(N * k / P) for k in range(P + 1)]
    isler = [(k, sinir[k], sinir[k + 1], f'{Wd}/p{k}.mp4') for k in range(P)]
    with Pool(P) as po:
        parcalar = po.map(parca, isler)
    lf = Wd + '/liste.txt'
    open(lf, 'w').write('\n'.join(f"file '{p}'" for p in parcalar))
    subprocess.run([FFMPEG, '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lf, '-i', MUZIK,
                    '-filter_complex', f'[1:a]atrim=0:{SURE},asetpts=PTS-STARTPTS,afade=t=out:st={SURE - 0.5}:d=0.5,loudnorm=I=-14:TP=-1.5:LRA=11[a]',
                    '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-crf', '17', '-preset', 'slow', '-pix_fmt', 'yuv420p',
                    '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                    '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-t', str(SURE), '-movflags', '+faststart', OUT], check=True)
    print('tamam', OUT)
