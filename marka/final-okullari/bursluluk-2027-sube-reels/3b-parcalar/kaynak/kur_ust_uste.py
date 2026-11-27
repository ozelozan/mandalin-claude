# ChatGPT parcalarini kirpip parcalar/ altina koyar, afis duzeninde ust uste dizer (kontrol montaji).
import os
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
K=os.path.dirname(os.path.abspath(__file__)); D=os.path.dirname(K)
ad={'finalin':'yazi-finalin','bursluluk':'yazi-bursluluk','sinavi':'yazi-sinavi',
    'cengelkoy':'sube-cengelkoy','beykoz':'sube-beykoz','ogrenci':'ogrenci'}
P={}
for k,v in ad.items():
    im=Image.open(f'{D}/chatgpt/bursluluk-3b-{k}.png').convert('RGBA'); im=im.crop(im.getchannel('A').point(lambda a:255 if a>12 else 0).getbbox())
    im.save(f'{D}/parcalar/{v}.png'); P[k]=im; print(v,im.size)
P['tarih']=Image.open(f'{D}/parcalar/tarih-9-10-ocak.png'); P['bant']=Image.open(f'{D}/parcalar/online-kayit-bandi.png')
# referans afisteki kutular (1440x1999 olcekte): x0,y0,x1 -> genislige gore olcekle
yer={'tarih':(455,268,985),'sube':(330,478,870),'finalin':(280,605,1000),'bursluluk':(262,818,1175),
     'sinavi':(250,1030,1195),'bant':(445,1478,1022),'ogrenci':(975,0,1255)}
def koy(c,im,x0,y0,x1):
    w=x1-x0; h=round(im.height*w/im.width); c.alpha_composite(im.resize((w,h),Image.LANCZOS),(x0,y0))
for sube in ['cengelkoy','beykoz']:
    c=Image.open(f'{D}/parcalar/zemin.png').convert('RGBA').resize((1440,1999),Image.LANCZOS)
    c.alpha_composite(Image.open(f'{D}/parcalar/cizgiler-{sube}.png').resize((1440,1999),Image.LANCZOS))
    for k in ['tarih','sube','finalin','bursluluk','sinavi','bant']:
        koy(c,P[sube] if k=='sube' else P[k],*yer[k])
    o=P['ogrenci']; x0,_,x1=yer['ogrenci']; h=round(o.height*(x1-x0)/o.width)
    koy(c,o,x0,yer['bursluluk'][1]+40-h,x1)   # ayakkabilar BURSLULUK'un ustune basar
    c.convert('RGB').save(f'{D}/montaj-kontrol-{sube}.jpg',quality=90)
