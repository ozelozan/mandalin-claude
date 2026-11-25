# İki kurum logosu yan yana: Çağdaş Bilgi Eğitim Kurumları (yatay) | Çağdaş Bilgi Koleji (amblem).
# Orijinal logo dosyaları yalnızca ölçeklenir (yeniden çizim/renk değişikliği yok). Çıktı: şeffaf katmanlar + önizleme.
import sys
from PIL import Image, ImageDraw
L = '/Volumes/Mini_MAN/mandalin-claude/marka/kurum_logolar/'
OUT = sys.argv[1]
W, H = 1920, 1080
cy = 460
# (dosya, kutu genişliği, kutu yüksekliği, sütun merkezi)
LOGOLAR = [('çağdaş bilgi logo.png', 640, 170, 610), ('cagdas_bilgi_koleji_logo-renkli.png', 330, 310, 1330)]
AYRAC_X = 1010
hepsi = Image.new('RGBA', (W, H), (0, 0, 0, 0))
for i, (f, bw, bh, cx) in enumerate(LOGOLAR):
    im = Image.open(L + f).convert('RGBA')
    a = im.split()[3].point(lambda v: 255 if v > 12 else 0)
    im = im.crop(a.getbbox())
    s = min(bw / im.width, bh / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    one = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    one.alpha_composite(im, (round(cx - im.width / 2), round(cy - im.height / 2)))
    one.save(f'{OUT}/logo-{i + 1}.png')
    hepsi.alpha_composite(one)
ay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
ImageDraw.Draw(ay).rectangle([AYRAC_X - 1, cy - 120, AYRAC_X, cy + 120], fill=(196, 200, 212, 255))
ay.save(f'{OUT}/ayrac.png')
prev = Image.new('RGBA', (W, H), (255, 255, 255, 255))
prev.alpha_composite(ay); prev.alpha_composite(hepsi)
prev.convert('RGB').save(f'{OUT}/onizleme.jpg', quality=90)
