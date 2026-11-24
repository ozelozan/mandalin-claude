# 4 kurum logosu: eşit sütunlar, ince ayraç çizgisi. Çıktı: şeffaf katmanlar (logolar, çizgiler) + önizleme
import sys
from PIL import Image, ImageDraw
L='/Volumes/Mini_MAN/mandalin-claude/marka/kurum_logolar/'
OUT=sys.argv[1]
files=['çengelköy logo.png','yakacık final logo.png','beykoz logo.png','cengelkoy final vip logo.png']
W,H=1920,1080; M=150; colw=(W-2*M)/4; cy=470
BOXW,BOXH=300,215
logos=Image.new('RGBA',(W,H),(0,0,0,0))
for i,f in enumerate(files):
    im=Image.open(L+f).convert('RGBA')
    a=im.split()[3].point(lambda v:255 if v>12 else 0); im=im.crop(a.getbbox())
    s=min(BOXW/im.width,BOXH/im.height); im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    cx=M+colw*(i+0.5)
    logos.alpha_composite(im,(round(cx-im.width/2),round(cy-im.height/2)))
    # her logo ayrı katman (sırayla giriş için)
    one=Image.new('RGBA',(W,H),(0,0,0,0)); one.alpha_composite(im,(round(cx-im.width/2),round(cy-im.height/2))); one.save(f'{OUT}/logo-{i+1}.png')
lines=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(lines)
for i in range(1,4):
    x=round(M+colw*i); d.rectangle([x-1,cy-95,x,cy+95],fill=(196,200,212,255))
lines.save(f'{OUT}/ayrac.png')
prev=Image.new('RGBA',(W,H),(255,255,255,255)); prev.alpha_composite(lines); prev.alpha_composite(logos); prev.convert('RGB').save(f'{OUT}/onizleme.jpg',quality=90)
