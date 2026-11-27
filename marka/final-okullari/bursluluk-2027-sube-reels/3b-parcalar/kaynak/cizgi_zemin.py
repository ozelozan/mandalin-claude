# Acik PSD'nin birlesik goruntusunden (7162x9941) sari cizgi+oklari seffaf PNG'ye, bos zemini ayri PNG'ye cikarir.
# Kullanim: python cizgi_zemin.py birlesik.png cikti_klasoru sube [zemin]
import sys, numpy as np, cv2
from PIL import Image; Image.MAX_IMAGE_PIXELS=None
src,out,sube=sys.argv[1:4]; zemin='zemin' in sys.argv[4:]
a=np.array(Image.open(src).convert('RGB')).astype(np.float32); H,W,_=a.shape; s=W/1440.0
R,G,B=a[...,0],a[...,1],a[...,2]
bg=np.array([39,52,127],np.float32)
score=np.minimum(R,G)-B                      # sari: yuksek; lacivert/beyaz/kirmizi: dusuk
Y=np.median(a[(score>170)&(np.arange(H)[:,None]<1500)],axis=0)   # ust bolgedeki cizgi rengi
d=Y-bg; t=((a-bg)*d).sum(2)/float((d*d).sum())
alpha=np.clip(t,0,1)*np.clip((score-15)/60,0,1)
# yazi blogu, ogrenci, web bandi, tarih rozeti kutularini disarida birak (1440 olcekli referans; ok uclari korunur)
sube_kutu={'cengelkoy':(330,486,875,605),'beykoz':(330,486,812,605)}[sube]
for x0,y0,x1,y1 in [sube_kutu,(250,600,1200,1392),(975,505,1255,1040),(440,1470,1030,1640),(450,262,992,428)]:
    alpha[int(y0*s):int(y1*s),int(x0*s):int(x1*s)]=0
k=lambda r:cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2*r+1,2*r+1))
# kucuk kirintilari temizle
n,lab,st,_=cv2.connectedComponentsWithStats((alpha>0.08).astype(np.uint8),connectivity=8)
keep=np.zeros(n,bool); keep[1:]=st[1:,cv2.CC_STAT_AREA]>4000
alpha[~keep[lab]]=0
rgba=np.dstack([np.broadcast_to(Y,(H,W,3)),alpha*255]).clip(0,255).astype(np.uint8)
Image.fromarray(rgba).save(f'{out}/cizgiler-{sube}.png',optimize=False); print('cizgi rengi',Y.round(), 'parca',int(keep.sum()))
if zemin:
    # icerik maskesi: zeminden belirgin farkli her sey + 60 px pay; maskesiz pikselleri yumusak yayarak doldur
    diff=np.abs(a-bg).max(2)>14
    f=8; h8,w8=H//f,W//f; m=diff[:h8*f,:w8*f].reshape(h8,f,w8,f).any(axis=(1,3))
    m=cv2.dilate(m.astype(np.uint8),k(10))>0
    small=cv2.resize(a,(w8,h8),interpolation=cv2.INTER_AREA); w=(~m).astype(np.float32)
    acc=np.zeros_like(small); ws=np.zeros_like(w)
    for sig in [6,20,60,180]:
        bs=cv2.GaussianBlur(small*w[...,None],(0,0),sig); bw=cv2.GaussianBlur(w,(0,0),sig)
        fill=bs/np.maximum(bw,1e-6)[...,None]; take=(ws==0)&(bw>0.05)
        acc[take]=fill[take]; ws[take]=1
    acc[~m]=small[~m]; acc=cv2.GaussianBlur(acc,(0,0),120)   # cok yumusak gecis, kare izi kalmasin
    full=cv2.resize(acc,(W,H),interpolation=cv2.INTER_CUBIC)+np.random.default_rng(1).uniform(-0.5,0.5,(H,W,3))
    Image.fromarray(full.clip(0,255).astype(np.uint8)).save(f'{out}/zemin.png'); print('zemin tamam')
