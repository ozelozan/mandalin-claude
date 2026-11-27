# PSD (v1, 8 bit RGB) katmanlarini seffaf PNG olarak cikarir. Kullanim: python psd_katman_cikar.py dosya.psd cikti_klasoru onek
import struct,sys,os
import numpy as np
from PIL import Image
f=open(sys.argv[1],'rb'); out=sys.argv[2]; pre=sys.argv[3]; os.makedirs(out,exist_ok=True)
def ui(n): return int.from_bytes(f.read(n),'big')
f.read(26); f.seek(ui(4),1); f.seek(ui(4),1); ui(4); ui(4)
cnt=abs(struct.unpack('>h',f.read(2))[0]); recs=[]
for i in range(cnt):
    t,l,b,r=struct.unpack('>iiii',f.read(16)); nc=ui(2)
    chs=[(struct.unpack('>h',f.read(2))[0],ui(4)) for _ in range(nc)]
    f.read(8); f.read(4); el=ui(4); st=f.tell()
    f.seek(ui(4),1); f.seek(ui(4),1); nl=ui(1); name=f.read(nl).decode('latin1')
    f.seek(st+el); recs.append((name,t,l,b,r,chs))
for idx,(name,t,l,b,r,chs) in enumerate(recs):
    w,h=r-l,b-t; planes={}
    for cid,ln in chs:
        st=f.tell(); comp=ui(2)
        if cid<-1 or w==0 or h==0: f.seek(st+ln); continue
        if comp==0: arr=np.frombuffer(f.read(w*h),np.uint8).reshape(h,w)
        elif comp==1:
            counts=[ui(2) for _ in range(h)]; rows=[]
            for c in counts:
                d=f.read(c); o=bytearray(); i=0
                while i<len(d):
                    n=d[i]; i+=1
                    if n<128: o+=d[i:i+n+1]; i+=n+1
                    elif n>128: o+=bytes([d[i]])*(257-n); i+=1
                rows.append(np.frombuffer(bytes(o[:w]),np.uint8))
            arr=np.stack(rows)
        else: raise SystemExit('zip sikistirma desteklenmiyor')
        planes[cid]=arr; f.seek(st+ln)
    if not planes: continue
    a=planes.get(-1,np.full((h,w),255,np.uint8))
    img=np.dstack([planes[0],planes[1],planes[2],a])
    fn=f"{out}/{pre}-{idx}-{name.replace(' ','_')}.png"
    Image.fromarray(img,'RGBA').save(fn); print(fn,w,h,(l,t))
