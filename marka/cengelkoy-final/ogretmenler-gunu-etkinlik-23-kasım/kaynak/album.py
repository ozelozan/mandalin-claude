# Öğretmenler Günü Gecesi fotoğraf albümü v2: beyaz çerçeveli baskılar, sahnenin bulanık ışığı önünde,
# vuruşta düşerek / kayarak / büyüyerek gelir ve albüm gibi üst üste birikir.
# Kullanım: python3 album.py <çalışma-klasörü> [sahne-no ...]   -> <çalışma>/govde.mp4
# Sonra: node kur.js plan-album.js <çalışma> <çıktı.mp4> kart && ... final  (başlık, müzik, 4 logolu kapanış)
import sys, os, math, subprocess
from multiprocessing import Pool
from PIL import Image, ImageOps, ImageFilter, ImageEnhance, ImageDraw

W, H, FPS = 1920, 1080, 25
BPM, FAZ = 103.0, 0.085
B = 60 / BPM
F = lambda k: 0 if k == 0 else round((FAZ + B * k) * FPS)
EV = '/Volumes/Mini_MAN/mandalin-claude/marka/cengelkoy-final/ogretmenler-gunu-etkinlik-23-kasım'
FO = EV + '/fotoğraflar/'
FFMPEG = os.path.expanduser('~/tools/bin/ffmpeg')
DUR, LAND = 11, 7     # giriş animasyonu kare sayısı / vuruşa oturan kare (Ozan: plaket dışı sahneler daha hızlı)
DUR_PL, LAND_PL = 18, 11   # plaketlerde eski, daha yumuşak hız
ZT = 6            # sahne geçişi kare sayısı

ka = lambda n: FO + 'karsilama/' + n + '.JPG'
he = lambda n: FO + 'hediye/' + n + '.JPG'
ma = lambda n: FO + 'masada fotoğraflar/' + n + '.JPG'
ko = lambda n: FO + 'konusma/' + n + '.JPG'
pl = lambda n: FO + 'plaket/' + n + '.JPG'
eg = lambda n: FO + 'eglence/' + n + '.JPG'
TIP = ['drop', 'slideL', 'slideR', 'pop']

# kart: (foto, merkez x, merkez y, açı, iç genişlik, iniş vuruşu, giriş tipi, [odak fx, fy, en/boy])
def L4(fotolar, b0, adim=2, tipler=('drop', 'slideR', 'slideL', 'pop')):
    yer = [(500, 330, -4), (1420, 320, 3), (540, 770, 3), (1390, 765, -3)]
    return [(f, x, y, a, 700, b0 + i * adim, tipler[i % 4]) for i, (f, (x, y, a)) in enumerate(zip(fotolar, yer))]

SAHNELER = [
    dict(ad='acilis', b=(0, 18), arka=he('DSC04719'),
         kart=[(ko('DSC04925'), 960, 560, -2, 1240, 13, 'pop')]),
    dict(ad='karsilama', b=(18, 30), arka=ka('DSC04693'),
         kart=[(ka('DSC04690'), 480, 545, -5, 430, 19, 'drop'),
               (ka('DSC04693'), 960, 520, 3, 430, 22, 'slideR'),
               (ka('DSC04706'), 1440, 550, -3, 430, 25, 'slideL')]),
    dict(ad='hediye', b=(30, 48), arka=he('DSC04716'),
         kart=[(he('DSC04714'), 400, 530, -4, 400, 31, 'drop'),
               (he('DSC04716'), 800, 560, 3, 400, 34, 'slideL'),
               (he('DSC04713'), 1180, 520, -2, 400, 37, 'slideR'),
               (he('DSC04715'), 1560, 555, 4, 400, 40, 'pop')]),
    dict(ad='masa1', b=(48, 64), arka=ma('DSC04728'),
         kart=L4([ma('DSC04722'), ma('DSC04728'), ma('DSC04730'), ma('DSC04746')], 49)),
    dict(ad='masa2', b=(64, 80), arka=ma('DSC04762'),
         kart=L4([ma('DSC04759'), ma('DSC04762'), ma('DSC04769'), ma('DSC04772')], 65, tipler=('slideL', 'drop', 'pop', 'slideR'))),
    dict(ad='konusma', b=(80, 100), arka=ko('DSC04925'),
         kart=[(ko('DSC04784'), 330, 545, -4, 380, 82, 'drop'),
               (ko('DSC04792'), 750, 520, 3, 380, 85, 'slideL'),
               (ko('DSC04919'), 1170, 550, -3, 380, 88, 'slideR'),
               (ko('DSC04927'), 1590, 525, 4, 380, 91, 'pop', 0.38, 0.5, 2 / 3)]),
    dict(ad='plaket', b=(100, 128), arka=pl('DSC04944'),
         kart=[(pl(n), [250, 615, 980, 1345, 1710][i % 5] + (60 if (i // 5) % 2 else 0),
                [400, 690, 470, 650][(i // 5) % 4], [-5, 3, -2, 4, -3, 2][i % 6], 330, 101 + i, TIP[i % 4])
               for i, n in enumerate(['DSC04931', 'DSC04934', 'DSC04936', 'DSC04940', 'DSC04944', 'DSC04945', 'DSC04948', 'DSC04950',
                                      'DSC04952', 'DSC04955', 'DSC04958', 'DSC04959', 'DSC04962', 'DSC04965', 'DSC04966', 'DSC04970'])]
         + [(FO + 'plaket/zeynep-veysel hoca.jpg', 1100, 560, 3, 360, 117, 'drop')]   # Zeynep ve Veysel Hoca
         + [(EV + '/cikti/fotograf/DSC04988-2A-bufe-dekor.jpg', 960, 560, -1.5, 1300, 120, 'drop')]),
    dict(ad='eglence1', b=(128, 144), arka=eg('DSC04869'),
         kart=L4([eg('DSC04864'), eg('DSC04862'), eg('DSC04869'), eg('DSC04883')], 129)),
    dict(ad='eglence2', b=(144, 160), arka=eg('DSC04894'),
         kart=L4([eg('DSC04894'), eg('DSC04895'), eg('DSC04912'), eg('DSC04899')], 145, tipler=('pop', 'slideL', 'slideR', 'drop'))),
]


def ac(yol, uzun=1800):
    im = Image.open(yol)
    im.draft('RGB', (uzun * 2, uzun * 2))
    im = ImageOps.exif_transpose(im).convert('RGB')
    im.thumbnail((uzun * 2, uzun * 2), Image.LANCZOS)
    ort = sum(ImageOps.grayscale(im).resize((64, 64)).getdata()) / 4096
    if ort < 75:   # gece salonu: karanlık fotoğrafı hafif aç
        im = ImageEnhance.Brightness(im).enhance(min(1.35, 85 / max(ort, 30)))
    return im


def arka_plan(yol):
    im = ac(yol, 1100)
    s = max(2112 / im.width, 1188 / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - 2112) // 2, (im.height - 1188) // 2
    im = im.crop((x, y, x + 2112, y + 1188)).filter(ImageFilter.GaussianBlur(38))
    im = ImageEnhance.Brightness(im).enhance(0.42)
    im = ImageEnhance.Color(im).enhance(0.85)
    # vinyet
    v = Image.new('L', (2112, 1188), 0)
    ImageDraw.Draw(v).ellipse((-300, -250, 2412, 1438), fill=255)
    v = v.filter(ImageFilter.GaussianBlur(220))
    return Image.composite(im, Image.new('RGB', im.size, (8, 8, 12)), v)


def kart_yap(yol, gen, fx=0.5, fy=0.4, oran=None):
    im = ac(yol)
    if oran:
        hh = im.height
        ww = min(im.width, round(hh * oran))
        x = min(max(round(im.width * fx - ww / 2), 0), im.width - ww)
        im = im.crop((x, 0, x + ww, hh))
    yuk = round(gen * im.height / im.width)
    im = im.resize((gen, yuk), Image.LANCZOS)
    p = max(14, round(min(gen, yuk) * 0.045))
    kart = Image.new('RGB', (gen + 2 * p, yuk + 2 * p), (250, 249, 246))
    kart.paste(im, (p, p))
    m = 40
    tuval = Image.new('RGBA', (kart.width + 2 * m, kart.height + 2 * m), (0, 0, 0, 0))
    gol = Image.new('L', tuval.size, 0)
    ImageDraw.Draw(gol).rectangle((m + 8, m + 14, m + 8 + kart.width, m + 14 + kart.height), fill=150)
    gol = gol.filter(ImageFilter.GaussianBlur(16))
    tuval.putalpha(gol)
    tuval.paste(kart, (m, m))
    a = tuval.split()[3]
    a.paste(255, (m, m, m + kart.width, m + kart.height))
    tuval.putalpha(a)
    return tuval


def ease_out_cubic(t): return 1 - (1 - t) ** 3
def ease_out_back(t, s=1.4): t -= 1; return 1 + t * t * ((s + 1) * t + s)


def poz(k, f):
    """kart k için f karesindeki (x, y, açı, ölçek, opaklık); görünmüyorsa None"""
    t0 = k['iner'] - k['land']
    if f < t0:
        return None
    p = min((f - t0) / k['dur'], 1.0)
    x, y, a, s, o = k['x'], k['y'], k['a'], 1.0, 1.0
    if p < 1:
        e = ease_out_back(p, 1.2)
        c = ease_out_cubic(p)
        if k['tip'] == 'drop':
            y = k['y'] - (1 - e) * 900; a = k['a'] + (1 - c) * 14; s = 1 + (1 - c) * 0.08
        elif k['tip'] == 'slideL':
            x = k['x'] - (1 - e) * 1500; a = k['a'] - (1 - c) * 12
        elif k['tip'] == 'slideR':
            x = k['x'] + (1 - e) * 1500; a = k['a'] + (1 - c) * 12
        else:
            s = 0.55 + 0.45 * e; o = min(1, p * 2.5); a = k['a'] + (1 - c) * 6
    return x, y, a, s, o


def bas(tuval, img, x, y, a, s, o, onbellek=None):
    if onbellek is not None and onbellek.get('anahtar') == (a, s):
        r = onbellek['r']
    else:
        r = img if s == 1 else img.resize((max(1, round(img.width * s)), max(1, round(img.height * s))), Image.BICUBIC)
        r = r.rotate(a, resample=Image.BICUBIC, expand=True)
        if onbellek is not None:
            onbellek.update(anahtar=(a, s), r=r)
    if o < 1:
        r = r.copy(); r.putalpha(r.split()[3].point(lambda v: int(v * o)))
    tuval.paste(r, (round(x - r.width / 2), round(y - r.height / 2)), r)


def sahne_render(i):
    sc = SAHNELER[i]
    W_ = sys.argv[1]
    b0, b1 = sc['b']
    f0, f1 = F(b0), F(b1)
    n = f1 - f0
    arka = arka_plan(sc['arka'])
    kartlar = []
    for kk in sc['kart']:
        yol, x, y, a, gen, iner, tip = kk[:7]
        fx, fy, oran = (kk[7], kk[8], kk[9]) if len(kk) > 7 else (0.5, 0.4, None)
        kartlar.append(dict(img=kart_yap(yol, gen, fx, fy, oran), x=x, y=y, a=a, iner=F(iner) - f0, tip=tip, ob={},
                            dur=DUR_PL if sc['ad'] == 'plaket' else DUR, land=LAND_PL if sc['ad'] == 'plaket' else LAND))
    out = f'{W_}/album/{i:02d}-{sc["ad"]}.mp4'
    pr = subprocess.Popen([FFMPEG, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-crf', '14', '-preset', 'fast', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    son = i == len(SAHNELER) - 1
    for f in range(n):
        q = f / max(n - 1, 1)
        ox, oy = round(40 + 112 * q), round(30 + 48 * q)   # yavaş arka plan kayması
        t = arka.crop((ox, oy, ox + W, oy + H))
        for k in kartlar:
            pz = poz(k, f)
            if pz:
                x, y, a, s, o = pz
                bas(t, k['img'], x, y, a, s, o, k['ob'] if (s == 1 and o == 1 and a == k['a']) else None)
        # sahne geçişi: çıkışta öne doğru büyüyüp kararır, girişte geriden yerine oturur
        z, d = 1.0, 0.0
        if i > 0 and f < ZT:
            e = ease_out_cubic(f / ZT); z = 1.10 - 0.10 * e; d = 0.55 * (1 - e)
        if not son and f >= n - ZT:
            e = (f - (n - ZT) + 1) / ZT; e = e * e; z = 1 + 0.12 * e; d = 0.55 * e
        if z != 1.0:
            cw, ch = round(W / z), round(H / z)
            t = t.crop(((W - cw) // 2, (H - ch) // 2, (W - cw) // 2 + cw, (H - ch) // 2 + ch)).resize((W, H), Image.BILINEAR)
        if d > 0:
            t = ImageEnhance.Brightness(t).enhance(1 - d)
        pr.stdin.write(t.tobytes())
    pr.stdin.close(); pr.wait()
    return out, n


if __name__ == '__main__':
    W_ = sys.argv[1]
    os.makedirs(W_ + '/album', exist_ok=True)
    secili = [int(a) for a in sys.argv[2:]] or list(range(len(SAHNELER)))
    with Pool(min(6, len(secili))) as p:
        sonuc = p.map(sahne_render, secili)
    print(sonuc)
    if len(secili) == len(SAHNELER):
        lf = W_ + '/album/liste.txt'
        open(lf, 'w').write('\n'.join(f"file '{o}'" for o, _ in sonuc))
        subprocess.run([FFMPEG, '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lf, '-c', 'copy', W_ + '/govde.mp4'], check=True)
        print('govde kare', sum(nn for _, nn in sonuc), 'beklenen', F(160))
