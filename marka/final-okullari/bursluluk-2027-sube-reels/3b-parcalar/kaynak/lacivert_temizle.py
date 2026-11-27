# Afis zemin lacivertini (yaklasik #27347F) seffaf yapar, kenarlari yumusatir, bos alani kirpar.
import sys, numpy as np
from PIL import Image
im=np.array(Image.open(sys.argv[1]).convert('RGBA')).astype(np.float32)
bg=np.array([39,52,127],np.float32)
d=np.sqrt(((im[:,:,:3]-bg)**2).sum(2))
k=np.clip((d-28)/40,0,1)          # 28 alti tam seffaf, 68 ustu tam opak
im[:,:,3]=im[:,:,3]*k
out=Image.fromarray(im.clip(0,255).astype(np.uint8))
out=out.crop(out.getbbox()); out.save(sys.argv[2]); print(sys.argv[2],out.size)
