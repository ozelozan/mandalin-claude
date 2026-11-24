#!/usr/bin/env node
// Öğretmenler Günü Gecesi etkinlik videosu: node kur.js plan.js <çalışma-klasörü> <çıktı.mp4> [adım]
// Adımlar: olc | segmentler | govde | kart | final (varsayılan hepsi)
// Çengelköy kur.js hattından türedi; farkları: klip başına otomatik pozlama, 2x ölçekte pürüzsüz
// Ken Burns, bölüm geçişlerinde zoom geçişi, 4 kurum logolu beyaz kapanış.
const { execFileSync, spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const cfg = require(path.resolve(process.argv[2]));
const W = path.resolve(process.argv[3]);
const OUT = path.resolve(process.argv[4]);
const ADIM = process.argv[5] || 'hepsi';
const KAYNAK = __dirname;
fs.mkdirSync(W + '/seg', { recursive: true });

const FPS = cfg.fps;
const B = 60 / cfg.bpm;
const F = (k) => (k === 0 ? 0 : Math.round((cfg.faz + B * k) * FPS));
const TOPLAM = Math.round(cfg.bitisSn * FPS);
const GEO = '/System/Library/Fonts/Supplemental/Georgia.ttf';
const GEO_B = '/System/Library/Fonts/Supplemental/Georgia Bold.ttf';
const GEO_I = '/System/Library/Fonts/Supplemental/Georgia Italic.ttf';
const NAVY = '0x1B1F5E';
const ZT = 7;        // zoom geçişi kare sayısı
const ZAMP = 0.30;   // zoom geçişi genliği

const run = (args) => execFileSync('ffmpeg', ['-v', 'error', '-y', ...args], { stdio: ['ignore', 'inherit', 'inherit'] });
const runAsync = (args) => new Promise((res, rej) => {
  const p = spawn('ffmpeg', ['-v', 'error', '-y', ...args], { stdio: ['ignore', 'inherit', 'inherit'] });
  p.on('close', (c) => (c === 0 ? res() : rej(new Error('ffmpeg ' + c + ' ' + args.join(' ')))));
});
const src = (c) => `${cfg.kamera}/${c.id}.MP4`;
// fotoğraf planı: { foto: 'tam/yol.jpg', fy: 0..1 (16:9 bandın dikey konumu), b }
const cid = (c) => (c.foto ? 'F' + path.basename(c.foto).replace(/\.[^.]+$/, '') + '_' + (c.fy ?? 0.5) + (c.kz ? '_' + c.kz + '_' + c.fx : '') : c.id);

// ---- plan ----
const plan = [];
let beat = 0, idx = 0;
cfg.bolumler.forEach((s, si) => {
  s.clips.forEach((c, ci) => {
    const f0 = F(beat), f1 = F(beat + c.b);
    const zin = ci === 0 && si > 0;
    const zout = ci === s.clips.length - 1 && si < cfg.bolumler.length - 1;
    // dosya adı içerikten: plan değişince yalnızca değişen segmentler yeniden işlenir
    const key = [cid(c).replace(/[^A-Za-z0-9]/g, ''), c.ss, f1 - f0, c.hiz || 1, +zin, +zout, idx % 2].join('_');
    plan.push({ i: idx, si, ci, c, n: f1 - f0, f0, zin, zout, key, file: `${W}/seg/${key}.mp4` });
    beat += c.b; idx++;
  });
});
const SON_VURUS = beat;
if (SON_VURUS !== cfg.kartVurus) console.warn('UYARI: gövde', SON_VURUS, 'vuruşta bitiyor, kart', cfg.kartVurus);

// ---- ölçüm: klip başına ortalama parlaklık -> gamma ----
const OLCU = W + '/olcu.json';
function olc() {
  const out = fs.existsSync(OLCU) ? JSON.parse(fs.readFileSync(OLCU)) : {};
  for (const p of plan) {
    if (out[p.key] !== undefined) continue;
    if (p.c.foto) { out[p.key] = null; continue; }
    const hiz = p.c.hiz || 1;
    const vals = [];
    for (const fr of [0.2, 0.5, 0.8]) {
      const t = p.c.ss + (p.n / FPS) * hiz * fr;
      const r = execFileSync('ffmpeg', ['-v', 'error', '-ss', String(t), '-i', src(p.c), '-frames:v', '1',
        '-vf', 'scale=480:-2,signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-', '-f', 'null', '-']).toString();
      const m = r.match(/YAVG=([\d.]+)/); if (m) vals.push(parseFloat(m[1]));
    }
    out[p.key] = vals.reduce((a, b) => a + b, 0) / vals.length;
  }
  fs.writeFileSync(OLCU, JSON.stringify(out, null, 1));
  console.log('ölçüm tamam');
}

function gamma(y) {
  // video aralığı 16-235 -> 0-1; hedef ortalama ~0.34 (gece salonu, karanlık kalmasın ama gürültü artmasın)
  const v = Math.min(Math.max((y - 16) / 219, 0.03), 0.95);
  const g = Math.log(v) / Math.log(0.34);
  return Math.min(Math.max(g, 0.9), 1.55);
}

function zoomExpr(p) {
  const N = p.n;
  const yon = p.i % 2 === 0;  // dönüşümlü içeri / dışarı yavaş itme
  const kb = yon ? `(1.0+0.05*on/${N})` : `(1.05-0.05*on/${N})`;
  let z = kb;
  if (p.zin) z += `*(1+${ZAMP}*pow(max(1-on/${ZT}\\,0)\\,3))`;
  if (p.zout) z += `*(1+${ZAMP}*pow(max((on-${N - ZT})/${ZT}\\,0)\\,3))`;
  return z;
}

function fotoArgs(p) {
  // EXIF yönü düzeltilmiş 16:9 bant (3840x2160) hazırlanır, video planlarıyla aynı zoom ve geçiş uygulanır
  const c = p.c, n = p.n, png = p.file.replace('.mp4', '.png');
  if (!fs.existsSync(png)) execFileSync('python3', ['-c', `
import sys
from PIL import Image, ImageOps
im=ImageOps.exif_transpose(Image.open(sys.argv[1])).convert('RGB'); w,h=im.size; fy=float(sys.argv[3])
bw,bh=(w,round(w*9/16)) if w*9/16<=h else (round(h*16/9),h)
kz=float(sys.argv[4]); fx=float(sys.argv[5]); bw,bh=round(bw*kz),round(bh*kz)
x=min(max(round(w*fx-bw/2),0),w-bw); y=round((h-bh)*fy)
im.crop((x,y,x+bw,y+bh)).resize((3840,2160),Image.LANCZOS).save(sys.argv[2])`, c.foto, png, String(c.fy ?? 0.5), String(c.kz || 1), String(c.fx ?? 0.5)]);
  const parts = [`zoompan=z='${zoomExpr(p)}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:s=1920x1080:fps=${FPS}`,
    "curves=all='0/0 0.5/0.5 0.88/0.84 1/0.90'", 'unsharp=5:5:0.25:5:5:0'];
  const bl = [];
  if (p.zin) bl.push(`lt(n\\,4)`);
  if (p.zout) bl.push(`gte(n\\,${n - 4})`);
  if (bl.length) parts.push(`boxblur=8:1:enable='${bl.join('+')}'`);
  parts.push('format=yuv420p');
  return ['-loop', '1', '-framerate', String(FPS), '-i', png, '-vf', parts.join(','), '-frames:v', String(n), '-r', String(FPS),
    '-c:v', 'libx264', '-crf', '13', '-preset', 'fast', '-pix_fmt', 'yuv420p', p.file];
}

function segArgs(p, pass, trf, gam) {
  const c = p.c, hiz = c.hiz || 1, n = p.n;
  const dur = n * hiz / FPS + 0.3;
  const pre = hiz === 1
    ? `tmix=frames=3,select='not(mod(n\\,4))',setpts=N/(${FPS}*TB)`
    : `tmix=frames=2,select='not(mod(n\\,2))',setpts=N/(${FPS}*TB)`;
  const a = ['-ss', String(c.ss), '-t', String(dur), '-i', src(c), '-an'];
  if (pass === 'detect') return [...a, '-vf', `${pre},vidstabdetect=shakiness=7:accuracy=15:result=${trf}`, '-f', 'null', '-'];
  const parts = [pre,
    `vidstabtransform=input=${trf}:smoothing=22:zoom=4:optzoom=0:interpol=bicubic`,
    // açılan karanlık planlarda siyahlar sütlenmesin diye hafif kontrast
    `eq=gamma=${gam.toFixed(3)}:saturation=1.07:contrast=${gam > 1.2 ? 1.07 : 1.0}`,
    // vurgu yumuşatma: sahne ekranı ve lambalar patlamasın (beyaz tavanı ~%88)
    "curves=all='0/0 0.06/0.045 0.5/0.5 0.75/0.73 0.88/0.82 1/0.88'",
    'colorbalance=rs=0.02:bs=-0.015:rh=-0.01:bh=0.01',
  ];
  if (gam > 1.15) parts.push('hqdn3d=2.5:2:4:4');
  parts.push('scale=3840:2160:flags=lanczos',
    `zoompan=z='${zoomExpr(p)}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:s=1920x1080:fps=${FPS}`,
    'unsharp=5:5:0.35:5:5:0');
  const bl = [];
  if (p.zin) bl.push(`lt(n\\,4)`);
  if (p.zout) bl.push(`gte(n\\,${n - 4})`);
  if (bl.length) parts.push(`boxblur=8:1:enable='${bl.join('+')}'`);
  parts.push('format=yuv420p');
  return [...a, '-vf', parts.join(','), '-frames:v', String(n), '-r', String(FPS),
    '-c:v', 'libx264', '-crf', '13', '-preset', 'fast', '-pix_fmt', 'yuv420p', p.file];
}

async function segmentler() {
  const olcu = JSON.parse(fs.readFileSync(OLCU));
  const only = process.env.ONLY ? process.env.ONLY.split(',').map(Number) : null;   // deneme: ONLY=5,10
  const kuyruk = plan.filter((p) => !fs.existsSync(p.file) && (!only || only.includes(p.i)));
  console.log('segment:', kuyruk.length, '/', plan.length);
  let k = 0;
  const isci = async () => {
    while (k < kuyruk.length) {
      const p = kuyruk[k++];
      const trf = p.file.replace('.mp4', '.trf');
      if (p.c.foto) { await runAsync(fotoArgs(p)); process.stdout.write('.'); continue; }
      await runAsync(segArgs(p, 'detect', trf));
      await runAsync(segArgs(p, 'render', trf, gamma(olcu[p.key])));
      process.stdout.write('.');
    }
  };
  await Promise.all([isci(), isci(), isci(), isci()]);
  console.log('\nsegmentler tamam');
}

function govde() {
  const lf = `${W}/govde.txt`;
  fs.writeFileSync(lf, plan.map((p) => `file '${p.file}'`).join('\n'));
  run(['-f', 'concat', '-safe', '0', '-i', lf, '-c', 'copy', `${W}/govde.mp4`]);
}

const ease = (t0, d) => `(1-pow(1-min(max((t-${t0})/${d}\\,0)\\,1)\\,3))`;
const lin = (t0, d) => `min(max((t-${t0})/${d}\\,0)\\,1)`;

function kart() {
  // beyaz zemin, logolar vuruşlarda sırayla, ayraç + mesaj, son akordan sonra saf beyaza
  const lk = `${W}/logo-karti`;
  fs.mkdirSync(lk, { recursive: true });
  execFileSync('python3', [`${KAYNAK}/logo-karti.py`, lk]);
  const k0 = F(cfg.kartVurus) - 12;           // gövdeyle 12 karelik beyaz geçiş (final() ile aynı)
  const n = TOPLAM - k0;
  const ts = (k) => (F(k) - k0) / FPS;        // vuruşun kart içindeki zamanı
  const beyazT = ts(cfg.sonAkor + 3);
  const cik = `(1-${lin(beyazT, 1.4)})`;
  let filt = `[0:v]format=rgba[bg];`;
  let cur = '[bg]';
  for (let i = 0; i < 4; i++) {
    const t = ts(cfg.kartVurus + 1 + i);
    filt += `[${i + 1}:v]format=rgba,fade=in:st=${t.toFixed(3)}:d=0.45:alpha=1,fade=out:st=${beyazT.toFixed(3)}:d=1.4:alpha=1[l${i}];`;
    filt += `${cur}[l${i}]overlay=x=0:y='18*(1-${ease(t, 0.6)})':eval=frame[o${i}];`;
    cur = `[o${i}]`;
  }
  const ta = ts(cfg.kartVurus + 5);
  filt += `[5:v]format=rgba,fade=in:st=${ta.toFixed(3)}:d=0.6:alpha=1,fade=out:st=${beyazT.toFixed(3)}:d=1.4:alpha=1[ay];${cur}[ay]overlay[o4];`;
  const tm = ts(cfg.kartVurus + 6);
  filt += `[o4]drawtext=fontfile='${GEO_I}':text='${cfg.kartMesaj}':fontsize=50:fontcolor=${NAVY}:x=(w-text_w)/2:y='700+16*(1-${ease(tm, 0.8)})':alpha='${ease(tm, 0.7)}*${cik}',format=yuv420p[v]`;
  run(['-f', 'lavfi', '-i', `color=c=white:s=1920x1080:r=${FPS}`,
    ...[1, 2, 3, 4].flatMap((i) => ['-loop', '1', '-i', `${lk}/logo-${i}.png`]), '-loop', '1', '-i', `${lk}/ayrac.png`,
    '-filter_complex', filt, '-map', '[v]', '-frames:v', String(n), '-r', String(FPS),
    '-c:v', 'libx264', '-crf', '13', '-preset', 'fast', '-pix_fmt', 'yuv420p', `${W}/kart.mp4`]);
}

function final() {
  const govdeN = F(SON_VURUS);
  const xoff = (govdeN - 12) / FPS;   // kart k0 = F(kart)-6 ... beyaz geçiş 12 kare
  // açılış başlığı bandı
  run(['-f', 'lavfi', '-i', 'color=c=black:s=1920x1080,format=rgba', '-vf',
    `geq=r=0:g=0:b=0:a='190*exp(-pow((Y-560)/250\\,2))'`, '-frames:v', '1', `${W}/bant.png`]);
  const [b1, b2, b3] = cfg.baslik;
  const fo = `(1-${lin(5.6, 0.8)})`;
  const baslik =
    `drawtext=fontfile='${GEO_B}':text='${b1}':fontsize=38:fontcolor=white@0.9:x=(w-text_w)/2:y='440+12*(1-${ease(1.0, 1.2)})':alpha='${ease(1.0, 1.0)}*${fo}',` +
    `drawbox=x=(iw-90)/2:y=500:w=90:h=2:color=white@0.75:t=fill:enable='between(t,1.3,6.4)',` +
    `drawtext=fontfile='${GEO_I}':text='${b2}':fontsize=104:fontcolor=white:shadowcolor=black@0.5:shadowx=2:shadowy=3:x=(w-text_w)/2:y='522+14*(1-${ease(1.5, 1.3)})':alpha='${ease(1.5, 1.1)}*${fo}',` +
    `drawtext=fontfile='${GEO}':text='${b3}':fontsize=40:fontcolor=white@0.9:x=(w-text_w)/2:y='668+12*(1-${ease(2.3, 1.2)})':alpha='${ease(2.3, 1.0)}*${fo}'`;
  const muzikF = `[3:a]atrim=0:${cfg.bitisSn},asetpts=PTS-STARTPTS,afade=t=out:st=${cfg.bitisSn - (cfg.muzikSonus || 1.2)}:d=${cfg.muzikSonus || 1.2},loudnorm=I=-14:TP=-1.5:LRA=11[a]`;
  const filt =
    `[0:v][1:v]xfade=transition=fadewhite:duration=${12 / FPS}:offset=${xoff}[v0];` +
    `[2:v]format=rgba,fade=in:st=0.4:d=1.0:alpha=1,fade=out:st=5.5:d=1.0:alpha=1[bant];` +
    `[v0][bant]overlay=shortest=1[v1];` +
    `[v1]${baslik},fade=in:st=0:d=1.0,format=yuv420p[v];` + muzikF;
  run(['-i', `${W}/govde.mp4`, '-i', `${W}/kart.mp4`, '-loop', '1', '-i', `${W}/bant.png`, '-i', cfg.muzik,
    '-filter_complex', filt, '-map', '[v]', '-map', '[a]', '-frames:v', String(TOPLAM),
    '-c:v', 'libx264', '-crf', '17', '-preset', 'slow', '-pix_fmt', 'yuv420p',
    '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
    '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-movflags', '+faststart', OUT]);
}

(async () => {
  console.log('toplam kare', TOPLAM, 'gövde vuruşu', SON_VURUS, 'gövde kare', F(SON_VURUS), 'segment', plan.length);
  const h = ADIM === 'hepsi';
  if (h || ADIM === 'olc') olc();
  if (h || ADIM === 'segmentler') await segmentler();
  if (h || ADIM === 'govde') govde();
  if (h || ADIM === 'kart') kart();
  if (h || ADIM === 'final') final();
})();
