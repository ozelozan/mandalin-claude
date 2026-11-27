# Seslendirme + muzik (sesin altinda, sidechain) + zamanlanmis efektler -> ses/miks.wav (-14 LUFS)
import subprocess, os
K=os.path.dirname(os.path.abspath(__file__)); S=os.path.join(os.path.dirname(K),'ses')
FF=os.path.expanduser('~/tools/bin/ffmpeg'); SURE=25.8
# (dosya, saniye, ses duzeyi)
EF=[('pop',0.0,.45),('pop',0.56,.4),('pop',0.78,.45),('pop',1.1,.45),('pop',1.54,.6),
    ('whoosh1',1.82,.7),('whoosh2',2.0,.6),('whoosh1',2.58,.6),('whoosh2',3.28,.6),
    ('vurus',3.98,1.0),('pop',4.36,.9),('parilti',5.05,.55),
    ('pop',5.94,.9),('pop',6.2,.3),('pop',6.32,.3),('pop',6.44,.3),('pop',6.56,.3),('pop',6.68,.3),('pop',6.8,.3),
    ('pop',6.96,.9),('whoosh2',7.5,.4),('whoosh1',8.12,.6),
    ('kalem1',7.7,.5),('parilti',10.55,.8),('whoosh2',12.5,.7),('damga',12.8,.7),('pop',12.9,.8),
    ('whoosh1',16.85,.55),('pop',17.66,.45),('pop',19.02,.45),('pop',20.14,.45),('pop',20.96,.45),
    ('parilti',24.2,.9),('vurus',24.28,.7)]
cmd=[FF,'-y','-v','error','-i',f'{S}/vo-ayla.mp3','-i',f'{S}/muzik.mp3']
for f,_,_ in EF: cmd+=['-i',f'{S}/{f}.mp3']
fc=['[0:a]aresample=48000,asplit=2[vo][vok]',
    f'[1:a]aresample=48000,volume=0.32,afade=t=out:st={SURE-1.2}:d=1.2[muz]',
    '[muz][vok]sidechaincompress=threshold=0.04:ratio=6:attack=15:release=300[muzd]']
for i,(f,t,v) in enumerate(EF):
    ms=int(t*1000); fc.append(f'[{i+2}:a]aresample=48000,volume={v},adelay={ms}|{ms}[e{i}]')
fc.append('[vo][muzd]'+''.join(f'[e{i}]' for i in range(len(EF)))+f'amix=inputs={len(EF)+2}:normalize=0:duration=longest,atrim=0:{SURE},loudnorm=I=-14:TP=-1.5:LRA=11[out]')
cmd+=['-filter_complex',';'.join(fc),'-map','[out]','-ar','48000',f'{S}/miks.wav']
subprocess.run(cmd,check=True); print('ok',f'{S}/miks.wav')
