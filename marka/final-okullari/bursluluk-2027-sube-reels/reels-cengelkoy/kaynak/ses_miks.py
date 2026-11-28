# Seslendirme + muzik (sesin altinda, sidechain) + zamanlanmis efektler -> ses/miks.wav (-14 LUFS)
import subprocess, os
K=os.path.dirname(os.path.abspath(__file__)); S=os.path.join(os.path.dirname(K),'ses')
FF=os.path.expanduser('~/tools/bin/ffmpeg'); SURE=26.0
VO='vo-deniz.wav'   # Deniz Altaş gerçek seslendirme, boşlukları kesilmiş (kaynak/ses_duzenle.py)
# (dosya, saniye, ses duzeyi)
EF=[('pop',0.0,.45),('pop',0.62,.4),('pop',0.82,.45),('pop',1.18,.45),('pop',1.56,.6),
    ('whoosh1',1.78,.7),('whoosh2',1.85,.5),('pop',2.62,.6),('whoosh1',3.06,.6),
    ('vurus',3.98,1.0),('pop',4.2,.9),('pop',4.62,.35),('parilti',5.0,.5),
    ('pop',5.74,.9),('pop',6.2,.3),('pop',6.28,.3),('pop',6.36,.3),('pop',6.44,.3),('pop',6.52,.3),('pop',6.6,.3),
    ('pop',6.66,.9),('whoosh2',7.2,.35),('kalem1',7.75,.5),('whoosh1',8.08,.6),
    ('pop',9.72,.6),('pop',10.24,.75),('parilti',10.24,.55),('pop',10.72,.6),('pop',11.6,.6),('pop',12.08,.85),
    ('whoosh2',13.05,.6),('damga',13.2,.75),('pop',13.45,.7),('parilti',14.12,.45),
    ('whoosh1',16.52,.5),('pop',17.5,.45),('pop',18.84,.45),('pop',19.98,.45),('pop',20.66,.45),
    ('parilti',21.6,.5),('parilti',23.98,.9),('vurus',24.05,.7)]
cmd=[FF,'-y','-v','error','-i',f'{S}/{VO}','-i',f'{S}/muzik.mp3']
for f,_,_ in EF: cmd+=['-i',f'{S}/{f}.mp3']
fc=['[0:a]aresample=48000,asplit=2[vo][vok]',
    f'[1:a]aresample=48000,volume=0.32,afade=t=out:st={SURE-1.2}:d=1.2[muz]',
    '[muz][vok]sidechaincompress=threshold=0.04:ratio=6:attack=15:release=300[muzd]']
for i,(f,t,v) in enumerate(EF):
    ms=int(t*1000); fc.append(f'[{i+2}:a]aresample=48000,volume={v},adelay={ms}|{ms}[e{i}]')
fc.append('[vo][muzd]'+''.join(f'[e{i}]' for i in range(len(EF)))+f'amix=inputs={len(EF)+2}:normalize=0:duration=longest,atrim=0:{SURE},loudnorm=I=-14:TP=-1.5:LRA=11[out]')
cmd+=['-filter_complex',';'.join(fc),'-map','[out]','-ar','48000',f'{S}/miks.wav']
subprocess.run(cmd,check=True); print('ok',f'{S}/miks.wav')
