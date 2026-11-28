# Kullanim: python gorsel-hazirla.py <kaynak-klasor> <gorseller-klasoru>
# Fotoğrafları EXIF yönüne göre düzeltir, uzun kenarı 1800 px JPG olarak f1..fN adıyla kaydeder.
import sys, os
from PIL import Image, ImageOps
src, out = sys.argv[1], sys.argv[2]
files = sorted(f for f in os.listdir(src) if f.lower().endswith(('.jpg', '.jpeg', '.png')))
for i, f in enumerate(files, 1):
    im = ImageOps.exif_transpose(Image.open(os.path.join(src, f))).convert('RGB')
    im.thumbnail((1800, 1800), Image.LANCZOS)
    im.save(os.path.join(out, f'f{i}.jpg'), quality=84, optimize=True)
    print(f'f{i}.jpg', im.size, f)
