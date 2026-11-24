// Öğretmenler Günü Gecesi fotoğraf albümü videosu (Paradise, aynı logo kapanışı), 24 Kasım 2026
// Karışık kolaj düzenleri olay sırasıyla: karşılama, hediye, masalar, konuşmalar, plaketler, eğlence.
// Müzik b0'dan başlar; b160'taki (93.5 sn) sakin bölüme düşüşte logo kartı girer.
// Kolaj PNG'leri ilk kullanımda kolaj.py ile <etkinlik>/kolaj/ klasörüne üretilir (yeniden üretilebilir).
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const EV = '/Volumes/Mini_MAN/mandalin-claude/marka/cengelkoy-final/ogretmenler-gunu-etkinlik-23-kasım';
const FO = EV + '/fotoğraflar/';
const KOL = EV + '/kolaj';
fs.mkdirSync(KOL, { recursive: true });

const P = 0.3, L = 0.45;   // dikey odak: portre yüzler üstte, yatay ortaya yakın
const k = (d) => (n) => [FO + d + '/' + n + '.JPG', d === 'karsilama' || d === 'konusma' || d === 'plaket' || d === 'hediye' ? P : L];
const ka = k('karsilama'), he = k('hediye'), ma = k('masada fotoğraflar'), ko = k('konusma'), pl = k('plaket'), eg = k('eglence');
const hedL = [FO + 'hediye/DSC04719.JPG', L];

let sira = 0;
function kolaj(tip, fotolar, b) {
  sira++;
  const ad = `${String(sira).padStart(2, '0')}-${tip}-${fotolar.map((f) => path.basename(f[0]).replace(/\..*$/, '').replace('DSC0', '')).join('-')}`;
  const png = `${KOL}/${ad}.png`;
  if (!fs.existsSync(png)) {
    const js = `${KOL}/${ad}.json`;
    fs.writeFileSync(js, JSON.stringify({ tip, fotolar }));
    execFileSync('python3', [__dirname + '/kolaj.py', js, png]);
  }
  return { foto: png, fy: 0.5, b };
}

module.exports = {
  fps: 25, bpm: 103, faz: 0.085,
  kamera: EV + '/videolar',
  muzik: EV + '/muzik/#40 Paradise (Official).mp4',
  kartVurus: 160,
  sonAkor: 170,
  bitisSn: 104.0,
  muzikSonus: 3.0,
  baslik: ['FİNAL OKULLARI', 'Öğretmenler Günü Gecesi', '23 Kasım 2026'],
  kartMesaj: '24 Kasım Öğretmenler Günümüz Kutlu Olsun',
  bolumler: [
    { ad: 'karsilama', clips: [                                   // b0-28 (sakin giriş)
      kolaj('full', [ma('DSC04741')], 10),                         // başlık üstünde
      kolaj('p3', [ka('DSC04690'), ka('DSC04693'), ka('DSC04697')], 6),
      kolaj('p2', [ka('DSC04699'), ka('DSC04704')], 6),
      kolaj('p2', [ka('DSC04689'), ka('DSC04706')], 6) ] },
    { ad: 'hediye', clips: [                                       // b28-48 (yükseliş)
      kolaj('p2', [he('DSC04714'), he('DSC04716')], 6),
      kolaj('full', [hedL], 6),
      kolaj('p2', [he('DSC04713'), he('DSC04717')], 8) ] },   // tebrik kartı fotoğrafı bulanık olduğu için çıktı
    { ad: 'masalar', clips: [                                      // b48-80 (patlama)
      kolaj('big2', [ma('DSC04722'), ma('DSC04720'), ma('DSC04724')], 4),
      kolaj('full', [ma('DSC04728')], 4),
      kolaj('big2R', [ma('DSC04730'), ma('DSC04737'), ma('DSC04742')], 4),
      kolaj('full', [ma('DSC04746')], 4),
      kolaj('L2', [ma('DSC04755'), ma('DSC04759')], 4),
      kolaj('big2', [ma('DSC04762'), ma('DSC04764'), ma('DSC04767')], 4),
      kolaj('full', [ma('DSC04769')], 4),
      kolaj('big2R', [ma('DSC04772'), ma('DSC04776'), ma('DSC04779')], 4) ] },
    { ad: 'konusmalar', clips: [                                   // b80-100
      kolaj('p3', [ko('DSC04783'), ko('DSC04788'), ko('DSC04794')], 6),
      kolaj('full', [[FO + 'konusma/DSC04925.JPG', L]], 4),
      kolaj('p3', [ko('DSC04913'), ko('DSC04919'), ko('DSC04927')], 6),
      kolaj('p2', [ko('DSC04792'), ko('DSC04921')], 4) ] },
    { ad: 'plaketler', clips: [                                    // b100-128
      kolaj('p4', [pl('DSC04931'), pl('DSC04934'), pl('DSC04936'), pl('DSC04940')], 4),
      kolaj('p4', [pl('DSC04944'), pl('DSC04945'), pl('DSC04948'), pl('DSC04950')], 4),
      kolaj('p3', [pl('DSC04952'), pl('DSC04955'), pl('DSC04958')], 4),
      kolaj('p3', [pl('DSC04959'), pl('DSC04962'), pl('DSC04965')], 4),
      kolaj('p2', [pl('DSC04966'), pl('DSC04970')], 4),
      kolaj('full', [[EV + '/cikti/fotograf/DSC04988-2A-bufe-dekor.jpg', 0.5]], 8) ] },
    { ad: 'eglence', clips: [                                      // b128-160
      kolaj('full', [eg('DSC04864')], 4),
      kolaj('big2', [eg('DSC04861'), eg('DSC04862'), eg('DSC04865')], 4),
      kolaj('full', [eg('DSC04869')], 4),
      kolaj('big2R', [eg('DSC04877'), eg('DSC04883'), [FO + 'eglence/DSC04889.JPG', 0.35]], 4),
      kolaj('full', [eg('DSC04894')], 4),
      kolaj('L2', [eg('DSC04895'), eg('DSC04912')], 4),
      kolaj('full', [eg('DSC04899')], 4),
      kolaj('L2', [eg('DSC04834'), eg('DSC04852')], 4) ] },
  ],
};
