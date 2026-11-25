# Fotoğraf sahneleri: beyaz zeminli (polaroid tarzı) baskılar, salonun bulanık ışığı önünde vuruşta
# düşer / kayar / büyür ve üst üste birikir. Final gecesi album.py'sinden uyarlandı.
# Kullanım (kur.js çağırır): python3 foto-sahne.py <sahne> <b0> <kare-sayısı> <çıktı.mp4> <bpm> <faz>
#   b0: sahnenin videodaki başlangıç vuruşu (vuruş zamanlaması kur.js ile aynı formül)
import sys, os, subprocess
from PIL import Image, ImageOps, ImageFilter, ImageEnhance, ImageDraw

W, H, FPS = 1920, 1080, 25
FO = '/Volumes/Mini_MAN/mandalin-claude/marka/cadgas bilgi kurs/Çağdaş Bilgi Öğretmenler Günü Gecesi 2026/fotoğraflar/'
FFMPEG = os.path.expanduser('~/tools/bin/ffmpeg')
pl = lambda n: FO + 'plaket/DSC' + n + '.JPG'
od = lambda n: FO + 'ödül/DSC' + n + '.JPG'
DUR, LAND = 14, 9      # giriş animasyonu kare sayısı / vuruşa oturduğu kare

# kart: (foto, merkez x, merkez y, açı, fotoğraf genişliği, iniş vuruşu (sahne içi), giriş tipi)
SAHNELER = {
    # plaket töreni, 1. bölüm: 7 kişi soldan sağa, iki sıra kademeli
    'plaket1': dict(arka=pl('00071'), kart=[
        (pl(n), 215 + i * 248, [420, 640][i % 2], [-4, 3, -2, 4, -3, 2, -4][i], 300, 1 + i * 1.5, ['drop', 'slideL', 'pop', 'slideR'][i % 4])
        for i, n in enumerate(['00054', '00055', '00058', '00059', '00062', '00063', '00065'])]),
    # 2. bölüm: dört tekli plaket, sonra üç kişilik iki toplu plaket ortada büyük
    'plaket2': dict(arka=pl('00083'), kart=[
        (pl('00068'), 270, 330, -3, 300, 1, 'slideL'),       # tekliler iki yanda sütun
        (pl('00070'), 1650, 330, 3, 300, 2, 'slideR'),
        (pl('00071'), 290, 755, 3, 300, 3, 'drop'),
        (pl('00073'), 1630, 755, -3, 300, 4, 'pop'),
        (pl('00083'), 755, 545, -2.5, 400, 6, 'slideL'),     # üç kişilik toplu plaketler ortada
        (pl('00084'), 1165, 540, 2.5, 400, 7, 'slideR')]),
    # hediye çekilişi ödülleri: 6 kişi, en sonda ödül verenlerin toplu fotoğrafı
    'odul': dict(arka=od('00129'), kart=[
        (od(n), 220 + i * 296, [430, 650][i % 2], [-3, 4, -2, 3, -4, 2][i], 290, 1 + i, ['pop', 'drop', 'slideR', 'slideL'][i % 4])
        for i, n in enumerate(['00116', '00118', '00120', '00123', '00125', '00126'])]
        + [(od('00129'), 960, 555, -1.5, 980, 8.5, 'drop')]),
}


def duzelt(im):
    """renk/ışık: parlaklık yüzdeliklerine göre seviye, orta tonları hedefe çek, turuncu zemini hafif nötrle"""
    g = ImageOps.grayscale(im).resize((256, 256))
    h = g.histogram(); top = sum(h)
    def yuzde(p):
        s = 0
        for i, v in enumerate(h):
            s += v
            if s >= top * p: return i
        return 255
    lo, hi = yuzde(0.004), yuzde(0.997)
    lo, hi = min(lo, 24), max(hi, 200)
    ort = sum(i * v for i, v in enumerate(h)) / top
    m = min(max((ort - lo) / (hi - lo), 0.05), 0.95)
    import math
    gam = min(max(math.log(0.40) / math.log(m), 0.70), 1.15)     # orta tonlar ~%40
    lut = [min(255, max(0, round(255 * (min(max((i - lo) / (hi - lo), 0), 1) ** gam)))) for i in range(256)]
    im = im.point(lut * 3)
    r, gg, b = im.split()
    r = r.point(lambda v: round(v * 0.975)); b = b.point(lambda v: min(255, round(v * 1.02)))
    im = Image.merge('RGB', (r, gg, b))
    im = ImageEnhance.Color(im).enhance(1.05)
    return ImageEnhance.Contrast(im).enhance(1.04)


def ac(yol, uzun=1600):
    im = Image.open(yol)
    im.draft('RGB', (uzun * 2, uzun * 2))
    im = ImageOps.exif_transpose(im).convert('RGB')
    im.thumbnail((uzun, uzun), Image.LANCZOS)
    return im


def arka_plan(yol):
    im = ac(yol, 1100)
    s = max(2112 / im.width, 1188 / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - 2112) // 2, (im.height - 1188) // 2
    im = im.crop((x, y, x + 2112, y + 1188)).filter(ImageFilter.GaussianBlur(40))
    im = ImageEnhance.Brightness(im).enhance(0.40)
    im = ImageEnhance.Color(im).enhance(0.85)
    v = Image.new('L', (2112, 1188), 0)
    ImageDraw.Draw(v).ellipse((-300, -250, 2412, 1438), fill=255)
    v = v.filter(ImageFilter.GaussianBlur(220))
    return Image.composite(im, Image.new('RGB', im.size, (8, 8, 12)), v)


def kart_yap(yol, gen):
    im = duzelt(ac(yol))
    if im.height > im.width:      # dikey: üstteki ekranı ve alttaki boş zemini kırp (3:4)
        hh = round(im.width * 4 / 3); y = round((im.height - hh) * 0.55)
        im = im.crop((0, y, im.width, y + hh))
    yuk = round(gen * im.height / im.width)
    im = im.resize((gen, yuk), Image.LANCZOS)
    p = max(12, round(min(gen, yuk) * 0.05)); alt = round(p * 2.6)       # beyaz baskı zemini, alt kenar kalın
    kart = Image.new('RGB', (gen + 2 * p, yuk + p + alt), (250, 249, 246))
    kart.paste(im, (p, p))
    m = 40
    tuval = Image.new('RGBA', (kart.width + 2 * m, kart.height + 2 * m), (0, 0, 0, 0))
    gol = Image.new('L', tuval.size, 0)
    ImageDraw.Draw(gol).rectangle((m + 8, m + 14, m + 8 + kart.width, m + 14 + kart.height), fill=160)
    gol = gol.filter(ImageFilter.GaussianBlur(16))
    tuval.putalpha(gol)
    tuval.paste(kart, (m, m))
    a = tuval.split()[3]; a.paste(255, (m, m, m + kart.width, m + kart.height)); tuval.putalpha(a)
    return tuval


def ease_out_cubic(t): return 1 - (1 - t) ** 3
def ease_out_back(t, s=1.2): t -= 1; return 1 + t * t * ((s + 1) * t + s)


def poz(k, f):
    t0 = k['iner'] - LAND
    if f < t0: return None
    p = min((f - t0) / DUR, 1.0)
    x, y, a, s, o = k['x'], k['y'], k['a'], 1.0, 1.0
    if p < 1:
        e, c = ease_out_back(p), ease_out_cubic(p)
        if k['tip'] == 'drop':
            y = k['y'] - (1 - e) * 900; a = k['a'] + (1 - c) * 14; s = 1 + (1 - c) * 0.08
        elif k['tip'] == 'slideL':
            x = k['x'] - (1 - e) * 1500; a = k['a'] - (1 - c) * 12
        elif k['tip'] == 'slideR':
            x = k['x'] + (1 - e) * 1500; a = k['a'] + (1 - c) * 12
        else:
            s = 0.55 + 0.45 * e; o = min(1, p * 2.5); a = k['a'] + (1 - c) * 6
    return x, y, a, s, o


def bas(tuval, img, x, y, a, s, o, ob):
    if ob.get('anahtar') == (a, s):
        r = ob['r']
    else:
        r = img if s == 1 else img.resize((max(1, round(img.width * s)), max(1, round(img.height * s))), Image.BICUBIC)
        r = r.rotate(a, resample=Image.BICUBIC, expand=True)
        if s == 1: ob.update(anahtar=(a, s), r=r)
    if o < 1:
        r = r.copy(); r.putalpha(r.split()[3].point(lambda v: int(v * o)))
    tuval.paste(r, (round(x - r.width / 2), round(y - r.height / 2)), r)


if __name__ == '__main__':
    ad, b0, n, out, bpm, faz = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), sys.argv[4], float(sys.argv[5]), float(sys.argv[6])
    B = 60 / bpm
    Fa = lambda k: round((faz + B * k) * FPS)
    f0 = Fa(b0)
    sc = SAHNELER[ad]
    arka = arka_plan(sc['arka'])
    kartlar = [dict(img=kart_yap(yol, gen), x=x, y=y, a=a, iner=Fa(b0 + ib) - f0, tip=tip, ob={})
               for (yol, x, y, a, gen, ib, tip) in sc['kart']]
    pr = subprocess.Popen([FFMPEG, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-crf', '13', '-preset', 'fast', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for f in range(n):
        q = f / max(n - 1, 1)
        ox, oy = round(40 + 112 * q), round(30 + 48 * q)      # yavaş arka plan kayması
        t = arka.crop((ox, oy, ox + W, oy + H))
        if f < 4:                                               # videodan yumuşak giriş
            t = ImageEnhance.Brightness(t).enhance(0.4 + 0.15 * f)
        for k in kartlar:
            pz = poz(k, f)
            if pz: bas(t, k['img'], *pz, k['ob'])
        pr.stdin.write(t.tobytes())
    pr.stdin.close(); pr.wait()
