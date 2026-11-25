// Fotoğraf albümü v2 (çerçeveli baskılar): görüntü album.py ile <çalışma>/govde.mp4 olarak üretilir;
// kur.js bu planla yalnızca 'kart' ve 'final' adımlarında kullanılır (başlık, Paradise, 4 logolu beyaz kapanış).
const EV = '/Volumes/Mini_MAN/mandalin-claude/marka/cengelkoy-final/ogretmenler-gunu-etkinlik-23-kasım';
module.exports = {
  fps: 25, bpm: 103, faz: 0.085,
  kamera: EV + '/videolar',
  muzik: EV + '/muzik/#40 Paradise (Official).mp4',
  kartVurus: 104, sonAkor: 114, bitisSn: 71.5, muzikSonus: 3.0,
  muzikBas: 56 * 60 / 103,   // müzik 56 vuruş ileriden, kesintisiz; kart parçanın düşüşüne denk gelir
  baslik: ['FİNAL OKULLARI', 'Öğretmenler Günü Gecesi', '23 Kasım 2026'],
  kartMesaj: '24 Kasım Öğretmenler Günümüz Kutlu Olsun',
  bolumler: [{ ad: 'album', clips: [{ id: 'album.py', ss: 0, b: 104 }] }],
};
