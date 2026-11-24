# DSC04988-2A: arka büfedeki içki şişelerinin yerine dekor (vazo, pampas, figür, kitap).
# Üretim: Magnific retouch (Nano Banana Pro) maskeli; insan maskesi SAM 3.1.
# Bu betik yalnızca birleştirir: üretilen pikseller sadece büfe bölgelerine girer,
# insan maskesindeki her piksel orijinal fotoğraftan birebir geri yazılır.
# Kullanım: python3 bufe-dekor.py <ara-dosya-klasörü> <orijinal.jpg> <çıktı.jpg>
import sys
import numpy as np
from PIL import Image, ImageFilter, ImageChops
SP, ORJ, OUT = sys.argv[1:4]
orj = Image.open(ORJ); icc = orj.info.get('icc_profile'); exif = orj.info.get('exif', b'')
orj = orj.convert('RGB')
gen = Image.open(SP + '/sonuc2.png').convert('RGB').resize((4500, 1560), Image.LANCZOS)  # orta büfe (kırpım 0,0-4500,1560)
m2 = Image.open(SP + '/degisim-maske2.png').convert('L')
for (x, y), dosya in [((3780, 330), 'sag-sonuc.png'), ((60, 760), 'sol-sonuc2.png')]:  # sağ bölme, sol kemerler
    p = Image.open(SP + '/' + dosya).convert('RGB')
    mk = m2.crop((x, y, x + p.width, y + p.height)).filter(ImageFilter.MaxFilter(31)).filter(ImageFilter.GaussianBlur(10))
    gen.paste(Image.composite(p, gen.crop((x, y, x + p.width, y + p.height)), mk), (x, y))
m1 = Image.open(SP + '/degisim-maske.png').convert('L')
alan = ImageChops.lighter(m1, m2).filter(ImageFilter.MaxFilter(151))      # süsler raf kutusundan taşabilir
insan = Image.open(SP + '/insan-maske.png').convert('L').point(lambda v: 255 if v > 127 else 0)
alan = ImageChops.subtract(alan, insan.filter(ImageFilter.MaxFilter(9))).filter(ImageFilter.GaussianBlur(4))
alan = ImageChops.subtract(alan, insan)                                    # insan üstünde kesin sıfır
son = orj.copy()
son.paste(Image.composite(gen, orj.crop((0, 0, 4500, 1560)), alan), (0, 0))
a, b = np.array(son), np.array(orj)
im = np.zeros(a.shape[:2], bool); im[:1560, :4500] = np.array(insan) > 0
print('insan pikseli', int(im.sum()), 'değişen', int((np.abs(a.astype(int) - b.astype(int)).sum(2)[im] > 0).sum()))
son.save(OUT, quality=98, subsampling=0, icc_profile=icc, exif=exif)
