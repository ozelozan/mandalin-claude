# Çengelköy Final Okulları - Öğretmenler Günü Gecesi 2026 fotoğraf Reels'i (dikey 1080x1920, 48 sn), 26 Kasım 2026
# Yakacık Reels (marka/yakacik-final/.../kaynak/reels.py v3) uyarlaması. Kullanım: python3 reels-cengelkoy.py <çalışma> <çıktı.mp4>
# Fotoğraflar Ozan'ın sırasıyla; 04792 açılış. Müzik Yakacık Reels'iyle aynı (Magnific / ElevenLabs Music v2, 120 BPM, 48 sn).
# Yapı: tam ekran dikey sahneler (5-8 vuruş) + çerçeveli yatay baskılar (çift ya da tek); b90'da (45 sn) yalnızca Çengelköy Final logosu.
# Sağ üstte hareketli 3B "10. Yılımız" rozeti (GPT 2.6). Açılışta tarih yok.
import sys, os, math, subprocess
from multiprocessing import Pool
from PIL import Image, ImageOps, ImageFilter, ImageEnhance, ImageDraw, ImageFont, ImageChops

W, H, FPS = 1080, 1920, 25
B = 0.5                       # vuruş (sn)
SURE = 48.0
N = int(SURE * FPS)
EV = '/Volumes/Mini_MAN/mandalin-claude/marka/cengelkoy-final/ogretmenler-gunu-etkinlik-23-kasım/fotoğraflar/'
YK = '/Volumes/Mini_MAN/mandalin-claude/marka/yakacik-final'
CG = '/Volumes/Mini_MAN/mandalin-claude/marka/cengelkoy-final'
MUZIK = YK + '/Öğretmenler Günü Gecesi 2026/muzik/fon-muzigi-hareketli.mp3'
LOGO = CG + '/logo/logo-tam.png'
FFMPEG = os.path.expanduser('~/tools/bin/ffmpeg')
NAVY, RED, WHITE = (19, 28, 81), (203, 54, 49), (255, 255, 255)
F_BI = '/System/Library/Fonts/Supplemental/Arial Bold Italic.ttf'
F_BL = '/System/Library/Fonts/Supplemental/Arial Black.ttf'
F_B = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
ma = lambda n: EV + 'masada fotoğraflar/DSC0' + str(n) + '.JPG'
dn = lambda on, n: EV + 'denemeler kullanma/' + on + 'DSC0' + str(n) + '.JPG'
pl = lambda n: EV + 'plaket/DSC0' + str(n) + '.JPG'

# ---- plan (vuruş cinsinden) ----
bul = lambda kl, n: EV + kl + '/DSC0' + str(n) + '.JPG'
PLAN = [('tek', [bul('konusma', 4792)], 8, True),                                   # açılış
        ('cift', [bul('masada fotoğraflar', 4722), bul('masada fotoğraflar', 4724)], 7, False),
        ('cift', [bul('masada fotoğraflar', 4728), bul('masada fotoğraflar', 4737)], 7, False),
        ('cift', [bul('masada fotoğraflar', 4742), bul('masada fotoğraflar', 4759)], 7, False),
        ('cift', [bul('masada fotoğraflar', 4772), bul('masada fotoğraflar', 4774)], 7, False),
        ('tek', [bul('karsilama', 4690)], 5, False)] + \
       [('tek', [bul('plaket', n)], 5, False) for n in (4936, 4959, 4962, 4965, 4966, 4970)] + \
       [('tek', [EV + 'plaket/zeynep-veysel hoca.jpg'], 5, False),
        ('cift', [bul('eglence', 4802), bul('eglence', 4883)], 7, False),
        ('cift', [bul('eglence', 4912)], 7, False)]                                  # tek yatay baskı
CEKIM = []
b = 0
for tip, fl, u, bas in PLAN:
    CEKIM.append(dict(tip=tip, fotolar=fl, b0=b, b1=b + u, baslik=bas))
    b += u
assert b == 90, b
CEKIM.append(dict(tip='logo', fotolar=[], b0=b, b1=SURE / B))
GECIS = ['whip', 'serit', 'zoom', 'iris', 'yukari', 'whip', 'flash', 'zoom', 'serit', 'iris', 'whip', 'yukari', 'zoom', 'serit', 'flash', 'iris', 'whip', 'yukari']
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
ALT_GRAD = Image.linear_gradient('L').resize((W, H)).point(lambda v: max(0, (v - 175) * 160 // 80))
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
    d.text((cx + 4, o + s * 0.43), '7.', font=f1, fill=WHITE, anchor='mm')
    d.text((cx, o + s * 0.74), 'YILIMIZ', font=f2, fill=WHITE, anchor='mm')
    return im.rotate(-8, resample=Image.BICUBIC, expand=True)


STK = None
LOGO_IM = None
ALT_LOGO = None
ZEMIN = None
ROZET = CG + '/ogretmenler-gunu-etkinlik-23-kasım/sticker/rozet-10.png'   # GPT 2.6 ile üretilen 3B rozet


def zemin():
    z = Image.new('RGB', (W, H), NAVY)
    v = Image.new('L', (W, H), 0)
    ImageDraw.Draw(v).ellipse((-500, 200, W + 500, H - 100), fill=255)
    acik = Image.new('RGB', (W, H), (34, 46, 112))
    return Image.composite(acik, z, v.filter(ImageFilter.GaussianBlur(260)))


def alt_logo():
    """amblem kendi renginde + yazı beyaz, yan yana (plakasız, Ozan'ın kuralı). Kaynak: logo-beyaz-yazi.png, 557. satırdan bölünür"""
    lg = Image.open(CG + '/logo/logo-beyaz-yazi.png').convert('RGBA')
    em = lg.crop((0, 0, lg.width, 557)); em = em.crop(em.split()[3].getbbox())
    yz = lg.crop((0, 557, lg.width, lg.height)); yz = yz.crop(yz.split()[3].getbbox())
    h = 96
    em = em.resize((round(em.width * h / em.height), h), Image.LANCZOS)
    th = 72
    yz = yz.resize((round(yz.width * th / yz.height), th), Image.LANCZOS)
    tv = Image.new('RGBA', (em.width + 20 + yz.width, h), (0, 0, 0, 0))
    tv.paste(em, (0, 0), em); tv.paste(yz, (em.width + 20, (h - th) // 2 + 2), yz)
    return tv


def hazirla():
    global STK, LOGO_IM, ALT_LOGO, ZEMIN
    r = Image.open(ROZET).convert('RGBA'); r = r.crop(r.split()[3].getbbox())
    STK = r.resize((250, round(250 * r.height / r.width)), Image.LANCZOS)
    lg = Image.open(LOGO).convert('RGBA'); lg = lg.crop(lg.split()[3].getbbox())
    LOGO_IM = lg.resize((420, round(420 * lg.height / lg.width)), Image.LANCZOS)
    ALT_LOGO = alt_logo()
    ZEMIN = zemin()


def rozet_kare(t):
    """hareketli rozet: dönerek gelir, süzülür, her 4 vuruşta nabız, 8 vuruşta bir parlama, hafif 3B salınım"""
    gir = min(max(t / 0.7, 0), 1)
    sx = abs(math.cos((1 - ease(gir)) * math.pi * 1.5)) if gir < 1 else 1.0      # Y ekseninde dönerek açılır
    sx = sx * (0.92 + 0.08 * math.cos(t * 1.6))                                   # sürekli hafif 3B salınım
    vur = (t % (4 * B)) / (4 * B)
    nab = 1 + 0.07 * math.exp(-vur * 9)
    s = (0.4 + 0.6 * ease(gir)) * nab
    w, h = max(2, round(STK.width * s * sx)), max(2, round(STK.height * s))
    im = STK.resize((w, h), Image.BICUBIC)
    pp = (t % (8 * B)) / (8 * B)
    if 0.05 < pp < 0.35 and gir >= 1:                                              # parlama şeridi
        u = (pp - 0.05) / 0.3
        bant = Image.new('L', (w, h), 0)
        cx = -0.4 * w + u * 1.8 * w
        ImageDraw.Draw(bant).polygon([(cx, 0), (cx + w * 0.18, 0), (cx - w * 0.12, h), (cx - w * 0.30, h)], fill=150)
        bant = ImageChops.multiply(bant.filter(ImageFilter.GaussianBlur(w * 0.03)), im.split()[3])
        im = Image.composite(Image.new('RGBA', (w, h), (255, 255, 255, 255)), im, bant)
    a = 6 * math.sin(t * 1.3)
    im = im.rotate(a, resample=Image.BICUBIC, expand=True)
    return im, 8 * math.sin(t * 2.2)


UST_GRAD = Image.linear_gradient('L').transpose(Image.FLIP_TOP_BOTTOM).resize((W, H)).point(lambda v: max(0, (v - 185) * 150 // 70))


def baslik_ciz(tv, lt):
    """açılış başlığı (tarih yok, Ozan'ın isteği)"""
    al = ease(min(max((lt - 0.2) / 0.5, 0), 1))
    katman = Image.new('RGBA', (W, 200), (0, 0, 0, 0))
    dk = ImageDraw.Draw(katman)
    dk.text((70, 80), 'Öğretmenler Günü Gecesi', font=ImageFont.truetype(F_BI, 54), fill=WHITE + (int(255 * al),), anchor='lm')
    dk.rectangle((70, 124, 70 + round(120 * al), 129), fill=RED + (int(255 * al),))
    tv.paste(katman, (0, 110), katman)


def cekim_kare(i, t):
    """i. çekimin t (sn, mutlak) anındaki karesi (RGB)"""
    c = CEKIM[i]
    t0, t1 = c['b0'] * B, c['b1'] * B
    q = min(max((t - t0) / (t1 - t0), 0), 1)
    if c['tip'] == 'tek':
        src = KY.get(c['fotolar'][0], W, H, 0.42)
        tv = kb(src, W, H, q, i % 2 == 0)
        if c['baslik']:
            tv.paste((8, 10, 30), (0, 0), UST_GRAD)   # başlık okunsun diye üstten yumuşak koyulaşma
            baslik_ciz(tv, t - t0)
        return tv
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
    # çift (v2): lacivert zemin, iki beyaz çerçeveli baskı; üstteki çekimle gelir, alttaki 1 vuruş sonra
    # sağdan hızlı kayar; ikisi de sahnede hafifçe süzülür (yüzme + çok küçük dönme)
    tv = ZEMIN.copy()
    lt = t - t0
    yerler = [(c['fotolar'][0], 540, 640, -2.0, 0.0, -1), (c['fotolar'][1], 540, 1325, 2.0, B, 1)] if len(c['fotolar']) == 2 \
        else [(c['fotolar'][0], 540, 960, -1.5, 0.0, -1)]   # tek masa fotoğrafı: ortada büyük baskı
    olc = 1.0 if len(c['fotolar']) == 2 else 1.08
    for k, (yol, cx, cy, aci, gecik, yon) in enumerate(yerler):
        g = min(max((lt - gecik + 0.12) / 0.26, 0), 1) if (k == 1 or i > 0) else 1.0
        if k == 0 and i > 0:
            g = 1.0          # üst baskı geçişle birlikte gelir
        if g <= 0:
            continue
        e = 1 + 2.4 * (g - 1) ** 3 + 1.4 * (g - 1) ** 2 if g < 1 else 1.0   # geri sekmeli
        fw, fh = round(920 * olc), round(613 * olc)
        foto = kb(KY.get(yol, fw, fh), fw, fh, q, k == 0)
        bask = Image.new('RGB', (fw + 40, fh + 40), (250, 249, 246)); bask.paste(foto, (20, 20))
        faz = i * 1.7 + k * 2.1
        a = aci + 0.6 * math.sin(lt * 2.4 + faz) + (1 - e) * 10 * yon
        x = cx + (1 - e) * 1150 * yon + 5 * math.sin(lt * 1.9 + faz)
        y = cy + 7 * math.sin(lt * 2.6 + faz)
        r = bask.convert('RGBA').rotate(a, resample=Image.BICUBIC, expand=True)
        golge = Image.new('RGBA', r.size, (0, 0, 0, 0))
        golge.putalpha(r.split()[3].point(lambda v: v * 110 // 255).filter(ImageFilter.GaussianBlur(14)))
        tv.paste(golge, (round(x - r.width / 2 + 10), round(y - r.height / 2 + 16)), golge)
        tv.paste(r, (round(x - r.width / 2), round(y - r.height / 2)), r)
    if c['baslik']:
        baslik_ciz(tv, lt)
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
    logo_t = CEKIM[-1]['b0'] * B
    cik = 1 - min(max((t - (logo_t - 0.2)) / 0.2, 0), 1)
    if cik > 0:
        # tam ekran plaketlerde logonun okunması için alttan yumuşak koyulaşma (plaka değil)
        if CEKIM[i]['tip'] == 'tek':
            tv.paste((8, 10, 30), (0, 0), ALT_GRAD)
        al = ALT_LOGO if cik >= 1 else ALT_LOGO.copy()
        if cik < 1:
            al.putalpha(al.split()[3].point(lambda v: int(v * cik)))
        tv.paste(al, ((W - al.width) // 2, 1760 - al.height // 2), al)
        rz, dy = rozet_kare(t)
        if cik < 1:
            rz.putalpha(rz.split()[3].point(lambda v: int(v * cik)))
        tv.paste(rz, (round(905 - rz.width / 2), round(185 + dy - rz.height / 2)), rz)
    return tv


def parca(arg):
    k, f0, f1, out = arg
    hazirla()
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
