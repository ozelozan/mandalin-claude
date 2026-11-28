# Gercek seslendirmedeki bosluklari kisaltir (sesi kesmeden, 12 ms yumusak gecis), hafif canlilik verir.
# Kullanim: python ses_duzenle.py giris.wav cikis.wav
import sys, re, subprocess, os
FF=os.path.expanduser('~/tools/bin/ffmpeg'); src,dst=sys.argv[1:3]
log=subprocess.run([FF,'-i',src,'-af','silencedetect=n=-40dB:d=0.15','-f','null','-'],capture_output=True,text=True).stderr
st=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',log)]; en=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',log)]
dur=float(re.search(r'Duration: (\d+):(\d+):([\d.]+)',log).group(3))+60*int(re.search(r'Duration: (\d+):(\d+)',log).group(2))
gaps=list(zip(st,en))
KUYRUK=0.12  # kelime sonundan birakilan pay (sesin sonu kesilmesin)
BAS=0.08     # sonraki kelimeden once birakilan pay
keep=[]; cur=0.0
for i,(a,b) in enumerate(gaps):
    if a<=0.01:            # bastaki sessizlik: 60 ms birak
        cur=max(0,b-0.06); continue
    g=b-a
    if b>=dur-0.01:        # sondaki sessizlik: 250 ms birak
        keep.append((cur,a+0.25)); cur=None; break
    if g>KUYRUK+BAS+0.02:
        keep.append((cur,a+KUYRUK)); cur=b-BAS
if cur is not None: keep.append((cur,dur))
parts=[]; fc=[]
for i,(a,b) in enumerate(keep):
    fc.append(f'[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={b-a-0.012:.3f}:d=0.012[p{i}]')
fc.append(''.join(f'[p{i}]' for i in range(len(keep)))+f'concat=n={len(keep)}:v=0:a=1,'
          'highpass=f=70,equalizer=f=3500:t=q:w=1.2:g=2,acompressor=threshold=-18dB:ratio=2.5:attack=8:release=120:makeup=1,'
          'alimiter=limit=0.89:level=false[out]')
subprocess.run([FF,'-y','-v','error','-i',src,'-filter_complex',';'.join(fc),'-map','[out]','-ar','48000','-ac','1',dst],check=True)
print('parca',len(keep),'eski',round(dur,2))
for a,b in keep: print(round(a,2),round(b,2))
