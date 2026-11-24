#!/usr/bin/env node
// Kurucu konuşması videosu (Ertuğ Ertaş, 23 Kasım 2026): node kurucu.js <çalışma-klasörü> <çıktı.mp4>
// Sunucunun çağrısı + konuşma, gereksiz boşluklar çıkarılmış; sonda 4 kurum logolu beyaz kart.
// Kesim noktaları faster-whisper (medium) kelime zamanlarından alındı.
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const W = path.resolve(process.argv[2]);
const OUT = path.resolve(process.argv[3]);
const EV = '/Volumes/Mini_MAN/mandalin-claude/marka/cengelkoy-final/ogretmenler-gunu-etkinlik-23-kasım';
const VID = EV + '/videolar/';
const C73 = VID + 'C0073.MP4';
const C74 = VID + 'C0074 - kurucu.MP4';
const MUZIK = EV + '/muzik/fon-muzigi-v1.mp3';
const FPS = 25;
const GEO_B = '/System/Library/Fonts/Supplemental/Georgia Bold.ttf';
const GEO_I = '/System/Library/Fonts/Supplemental/Georgia Italic.ttf';
const NAVY = '0x1B1F5E';
fs.mkdirSync(W + '/k', { recursive: true });

// v: görüntü kaynağı, a: ses kaynağı (yoksa v), z: kadraj (1.12 = yakın; aynı kameradaki kesimlerde sıçrama hissini kırar)
const SEG = [
  { v: [C73, 14.10], a: [C73, 15.20], d: 1.20, z: 1.0, not: 'salon (sunucu kamerası 15.2-16.3 savruluyor), çağrı sesi başlar' },
  { v: [C73, 16.40], a: [C73, 16.40], d: 1.00, z: 1.0, not: 'sunucu: "Gelenekselleşen açılış konuşmasını yapmak üzere..."' },
  { v: [C74, 112.92], a: [C73, 17.40], d: 2.60, z: 1.0, not: 'salon alkışlıyor (sunucu kamerası savruluyor), ses sürüyor' },
  { v: [C73, 20.00], a: [C73, 20.00], d: 3.40, z: 1.0, not: '"...Ertuğ Ertaş\'ı alkışlarınızla sahneye davet ediyorum"' },
  { v: [C74, 0.20], d: 2.40, z: 1.0, not: 'mikrofon teslimi' },
  { v: [C74, 11.30], d: 4.94, z: 1.0, isim: true, not: '"Hoş geldiniz. Hepimize öğretmenler günü kutlu olsun." (11.0-11.3 belini düzeltiyor: alınmadı)' },
  { v: [C74, 31.04], d: 6.32, z: 1.12, not: '"Bizim kurulduğumuzdan beri bu onuncu öğretmenler günü."' },
  { v: [C74, 47.36], d: 10.04, z: 1.0, not: '"Çok uzun bir konuşma yapmamak adına... çok vaktinizi almamak için."' },
  { v: [C74, 61.20], d: 12.04, z: 1.12, not: '"Ama benim Final Okulları olarak onuncu, öğretmen olarak 29. öğretmenler günüm."' },
  { v: [C74, 74.00], d: 18.28, z: 1.0, not: '"İyi ki öğretmeniz, iyi ki aynı idealin... aynı umudun yolcularıyız"' },
  { v: [C74, 94.92], d: 14.48, z: 1.12, not: '"ve aslında siz arkadaşlarımız... öğretmenler gününüzü kutluyoruz." + alkış' },
];
const ALKIS_KUYRUK = [C74, 109.40, 2.6];  // son kesimden sonra beyaza geçerken süren alkış
// kart: müzik parçasının son ölçüleri (110 BPM, ilk vuruş 0.505); logolar vuruşlarda
const B = 60 / 110, VUR = (k) => 0.505 + k * B;
const KART_MUZIK0 = VUR(279);      // kart burada başlar
const KART_SON = 163.0;            // müzik sönümü
const KART_N = Math.round((KART_SON - KART_MUZIK0) * FPS);
const XF = 12;                     // gövde -> beyaz kart geçişi (kare)

const run = (args) => execFileSync('ffmpeg', ['-v', 'error', '-y', ...args], { stdio: ['ignore', 'inherit', 'inherit'] });

function yavg(file, t) {
  const r = execFileSync('ffmpeg', ['-v', 'error', '-ss', String(t), '-i', file, '-frames:v', '1',
    '-vf', 'scale=480:-2,signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-', '-f', 'null', '-']).toString();
  return parseFloat(r.match(/YAVG=([\d.]+)/)[1]);
}
function gamma(y) {
  const v = Math.min(Math.max((y - 16) / 219, 0.03), 0.95);
  return Math.min(Math.max(Math.log(v) / Math.log(0.34), 0.9), 1.55);
}

function segment(s, i) {
  const n = Math.round(s.d * FPS);
  const out = `${W}/k/${String(i).padStart(2, '0')}.mov`;
  if (fs.existsSync(out)) return out;
  const [vf, vs] = s.v;
  const [af, as] = s.a || s.v;
  const y = (yavg(vf, vs + s.d * 0.25) + yavg(vf, vs + s.d * 0.5) + yavg(vf, vs + s.d * 0.75)) / 3;
  const g = gamma(y);
  const trf = `${W}/k/${i}.trf`;
  const pre = `tmix=frames=3,select='not(mod(n\\,4))',setpts=N/(${FPS}*TB)`;
  run(['-ss', String(vs), '-t', String(s.d + 0.3), '-i', vf, '-an', '-vf', `${pre},vidstabdetect=shakiness=7:accuracy=15:result=${trf}`, '-f', 'null', '-']);
  const z = s.z;
  const v = [pre,
    `vidstabtransform=input=${trf}:smoothing=30:zoom=4:optzoom=0:interpol=bicubic`,
    `eq=gamma=${g.toFixed(3)}:saturation=1.07:contrast=${g > 1.2 ? 1.07 : 1.0}`,
    "curves=all='0/0 0.06/0.045 0.5/0.5 0.75/0.73 0.88/0.82 1/0.88'",
    'colorbalance=rs=0.02:bs=-0.015:rh=-0.01:bh=0.01',
    ...(g > 1.15 ? ['hqdn3d=2.5:2:4:4'] : []),
    ...(z > 1 ? [`scale=${Math.round(1920 * z / 2) * 2}:-2:flags=lanczos,crop=1920:1080`] : []),
    'unsharp=5:5:0.35:5:5:0', 'format=yuv420p'].join(',');
  // konuşma sesi: uğultu kes, hafif gürültü azalt, kesim yerlerinde 30 ms yumuşak geçiş
  const a = `highpass=f=80,afftdn=nf=-30,atrim=0:${n / FPS},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st=${n / FPS - 0.03}:d=0.03`;
  run(['-ss', String(vs), '-t', String(s.d + 0.3), '-i', vf, '-ss', String(as), '-t', String(s.d + 0.3), '-i', af,
    '-filter_complex', `[0:v]${v}[v];[1:a]aformat=sample_rates=48000:channel_layouts=stereo,${a}[a]`,
    '-map', '[v]', '-map', '[a]', '-frames:v', String(n), '-r', String(FPS),
    '-c:v', 'libx264', '-crf', '13', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', out]);
  console.log(i, s.not, 'gamma', g.toFixed(2));
  return out;
}

const ease = (t0, d) => `(1-pow(1-min(max((t-${t0})/${d}\\,0)\\,1)\\,3))`;
const lin = (t0, d) => `min(max((t-${t0})/${d}\\,0)\\,1)`;

function kart() {
  const lk = `${W}/logo-karti`;
  fs.mkdirSync(lk, { recursive: true });
  execFileSync('python3', [`${__dirname}/logo-karti.py`, lk]);
  const ts = (k) => VUR(k) - KART_MUZIK0;
  const beyazT = ts(290);
  let filt = '[0:v]format=rgba[bg];', cur = '[bg]';
  for (let i = 0; i < 4; i++) {
    const t = ts(280 + i);
    filt += `[${i + 1}:v]format=rgba,fade=in:st=${t.toFixed(3)}:d=0.45:alpha=1,fade=out:st=${beyazT.toFixed(3)}:d=1.4:alpha=1[l${i}];`;
    filt += `${cur}[l${i}]overlay=x=0:y='18*(1-${ease(t, 0.6)})':eval=frame[o${i}];`;
    cur = `[o${i}]`;
  }
  const ta = ts(284), tm = ts(285);
  filt += `[5:v]format=rgba,fade=in:st=${ta.toFixed(3)}:d=0.6:alpha=1,fade=out:st=${beyazT.toFixed(3)}:d=1.4:alpha=1[ay];${cur}[ay]overlay[o4];`;
  filt += `[o4]drawtext=fontfile='${GEO_I}':text='24 Kasım Öğretmenler Günümüz Kutlu Olsun':fontsize=50:fontcolor=${NAVY}:x=(w-text_w)/2:y='700+16*(1-${ease(tm, 0.8)})':alpha='${ease(tm, 0.7)}*(1-${lin(beyazT, 1.4)})',format=yuv420p[v]`;
  run(['-f', 'lavfi', '-i', `color=c=white:s=1920x1080:r=${FPS}`,
    ...[1, 2, 3, 4].flatMap((i) => ['-loop', '1', '-i', `${lk}/logo-${i}.png`]), '-loop', '1', '-i', `${lk}/ayrac.png`,
    '-filter_complex', filt, '-map', '[v]', '-frames:v', String(KART_N + XF), '-r', String(FPS),
    '-c:v', 'libx264', '-crf', '13', '-preset', 'fast', '-pix_fmt', 'yuv420p', `${W}/kurucu-kart.mp4`]);
}

function final(dosyalar) {
  const lf = `${W}/k/liste.txt`;
  fs.writeFileSync(lf, dosyalar.map((f) => `file '${f}'`).join('\n'));
  run(['-f', 'concat', '-safe', '0', '-i', lf, '-c', 'copy', `${W}/kurucu-govde.mov`]);
  const govdeN = SEG.reduce((t, s) => t + Math.round(s.d * FPS), 0);
  const govdeSn = govdeN / FPS;
  const xoff = (govdeN - XF) / FPS;
  // isim yazısı: konuşmanın ilk planında
  const i0 = SEG.slice(0, SEG.findIndex((s) => s.isim)).reduce((t, s) => t + Math.round(s.d * FPS), 0) / FPS + 0.6;
  const fo = `(1-${lin(i0 + 4.6, 0.6)})`;
  run(['-f', 'lavfi', '-i', 'color=c=black:s=1920x1080,format=rgba', '-vf',
    `geq=r=0:g=0:b=0:a='if(gt(Y\\,700)\\,175*pow((Y-700)/380\\,0.8)*max(0\\,1-pow(X/1250\\,2))\\,0)'`, '-frames:v', '1', `${W}/isim-bant.png`]);
  const isim =
    `drawbox=x=120:y=872:w='70*${ease(i0, 0.7)}':h=3:color=0xE30A17:t=fill:enable='between(t,${i0},${i0 + 5.2})',` +
    `drawtext=fontfile='${GEO_B}':text='Ertuğ Ertaş':fontsize=60:fontcolor=white:shadowcolor=black@0.45:shadowx=2:shadowy=2:x=120:y='892+12*(1-${ease(i0 + 0.1, 0.8)})':alpha='${ease(i0 + 0.1, 0.6)}*${fo}',` +
    `drawtext=fontfile='${GEO_I}':text='Kurucu, Final Okulları':fontsize=36:fontcolor=white@0.92:shadowcolor=black@0.45:shadowx=2:shadowy=2:x=122:y='968+12*(1-${ease(i0 + 0.35, 0.8)})':alpha='${ease(i0 + 0.35, 0.6)}*${fo}'`;
  const [kf, ks, kd] = ALKIS_KUYRUK;
  const kartSn = (KART_N + XF) / FPS;
  const filt =
    `[0:v][1:v]xfade=transition=fadewhite:duration=${XF / FPS}:offset=${xoff}[v0];` +
    `[3:v]format=rgba,fade=in:st=${i0 - 0.2}:d=0.6:alpha=1,fade=out:st=${i0 + 4.8}:d=0.6:alpha=1[bant];` +
    `[v0][bant]overlay=shortest=1[v1];[v1]${isim},fade=in:st=0:d=0.5,format=yuv420p[v];` +
    // ses: konuşma (-16 LUFS'a, hafif sıkıştırma) + alkış kuyruğu + kart müziği
    `[0:a]acompressor=threshold=-22dB:ratio=2.5:attack=8:release=200:makeup=3,loudnorm=I=-16:TP=-2:LRA=9,aformat=sample_rates=48000:channel_layouts=stereo[ko];` +
    `[2:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:${kd},asetpts=PTS-STARTPTS,highpass=f=80,volume=-4dB,afade=t=out:st=0.6:d=${kd - 0.6},adelay=${Math.round(govdeSn * 1000)}|${Math.round(govdeSn * 1000)}[al];` +
    `[4:a]atrim=${KART_MUZIK0 - XF / FPS}:${KART_SON},asetpts=PTS-STARTPTS,afade=t=in:d=0.9,volume=-3dB,adelay=${Math.round(xoff * 1000)}|${Math.round(xoff * 1000)}[mz];` +
    `[ko][al][mz]amix=inputs=3:normalize=0:duration=longest,alimiter=limit=0.79:level=disabled[a]`;
  const toplamN = govdeN - XF + KART_N + XF;
  run(['-i', `${W}/kurucu-govde.mov`, '-i', `${W}/kurucu-kart.mp4`, '-ss', String(ks), '-i', kf, '-loop', '1', '-i', `${W}/isim-bant.png`, '-i', MUZIK,
    '-filter_complex', filt, '-map', '[v]', '-map', '[a]', '-frames:v', String(toplamN), '-t', String(toplamN / FPS),
    '-c:v', 'libx264', '-crf', '17', '-preset', 'slow', '-pix_fmt', 'yuv420p',
    '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
    '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-movflags', '+faststart', OUT]);
  console.log('süre', (toplamN / FPS).toFixed(2), 'sn; konuşma gövdesi', govdeSn.toFixed(2));
}

const dosyalar = SEG.map(segment);
kart();
final(dosyalar);
