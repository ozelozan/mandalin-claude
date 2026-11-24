// Final Okulları Öğretmenler Günü Gecesi - Paradise sürümü (Ozan'ın müziği), 24 Kasım 2026
// Müzik: muzik/#40 Paradise (Official).mp4, sözsüz, 103 BPM, vuruş fazı 0.085 sn (bas davul).
// Giriş b0-48 yükseliş, tam bölüm b48-256, b256'da sakin ara bölüme düşüş: logo kartı orada girer.
// Farklar (v3'e göre): yavaş çekim yok (titreme yapıyordu), mekan planı azaltıldı, Çengelköy/Beykoz/Yakacık
// isimlik fotoğrafları, karşılama doğrudan tokalaşmayla başlar, kurucunun beline dokunduğu plan çıktı,
// eğlencede daha önce kullanılmayan klipler, bölüm aralarında fotoğraf planları.
const EV = '/Volumes/Mini_MAN/mandalin-claude/marka/cengelkoy-final/ogretmenler-gunu-etkinlik-23-kasım';
const P = 'plaket töreni/';
const FD = EV + '/fotoğraflar/denemeler/';   // yalnızca okunur
const FM = EV + '/fotoğraflar/masada fotoğraflar/';
const FH = EV + '/fotoğraflar/hediye/';

module.exports = {
  fps: 25, bpm: 103, faz: 0.085,
  kamera: EV + '/videolar',
  muzik: EV + '/muzik/#40 Paradise (Official).mp4',
  kartVurus: 256,
  sonAkor: 270,        // beyaza dönüş sonAkor+3
  bitisSn: 162.0,
  muzikSonus: 3.0,
  baslik: ['FİNAL OKULLARI', 'Öğretmenler Günü Gecesi', '23 Kasım 2026'],
  kartMesaj: '24 Kasım Öğretmenler Günümüz Kutlu Olsun',
  bolumler: [
    { ad: 'giris', clips: [                       // b0-32
      { id: 'C0013', ss: 0.3, b: 10 },             // masa lambaları (başlık üstünde)
      { id: 'C0027', ss: 0.6, b: 5 },              // "Öğretmenler günümüz kutlu olsun" balonu
      { foto: FD + 'DSC04662.JPG', fy: 0.31, b: 4 },   // ÇENGELKÖY İLKOKULU isimliği
      { foto: FD + 'DSC04669.JPG', fy: 0.37, b: 4 },   // BEYKOZ İLKOKULU
      { foto: FD + 'DSC04676.JPG', fy: 0.70, kz: 0.70, fx: 0.50, b: 4 },   // YAKACIK İDARİ KADRO (soldaki markalı bardak kadraj dışı)
      { id: 'C0038', ss: 1.0, b: 5 } ] },          // lamba yanıyor
    { ad: 'karsilama', clips: [                    // b32-56, tokalaşma başlamış
      { id: 'C0041', ss: 4.4, b: 7 },               // 8.6 sonrası önden yakın geçiş
      { id: 'C0041', ss: 10.3, b: 2 },              // 12 sn sonrası önden yakın geçiş
      { id: 'C0042', ss: 1.8, b: 6 },
      { id: 'C0042', ss: 4.8, b: 4 },
      { id: 'C0044', ss: 0.0, b: 3 },
      { id: 'C0044', ss: 6.3, b: 2 } ] },
    { ad: 'hediye', clips: [                       // b56-80
      { foto: FH + 'DSC04719.JPG', fy: 0.5, b: 4 },
      { id: 'C0046', ss: 1.8, b: 6 },
      { id: 'C0047', ss: 2.8, b: 5 },
      { id: 'C0047', ss: 8.8, b: 4 },
      { id: 'C0052', ss: 0.5, b: 5 } ] },
    { ad: 'masa', clips: [                         // b80-96
      { foto: FM + 'DSC04722.JPG', fy: 0.75, b: 4 },   // BEYKOZ İDARİ KADRO masası
      { id: 'C0050', ss: 0.3, b: 4 },
      { id: 'C0066', ss: 0.3, b: 4 },
      { foto: FM + 'DSC04741.JPG', fy: 0.5, b: 4 } ] },   // 04751'in arkasında içki rafları vardı
    { ad: 'sunucu', clips: [                       // b96-108
      { id: 'C0073', ss: 2.4, b: 5 },
      { id: 'C0073', ss: 20.9, b: 7 } ] },
    { ad: 'kurucu', clips: [                       // b108-132 (9.5-11.2 belini düzeltiyor: alınmadı)
      { id: 'C0074 - kurucu', ss: 11.5, b: 6 },
      { id: 'C0074 - kurucu', ss: 40.0, b: 6 },
      { id: 'C0074 - kurucu', ss: 67.3, b: 7 },
      { id: 'C0074 - kurucu', ss: 112.3, b: 5 } ] },  // salon alkışı, kameraman geçtikten sonra
    { ad: 'plaket', clips: [                       // b132-200
      { id: 'C0069', ss: 0.6, b: 6 },
      { id: P + 'C0133', ss: 12.3, b: 4 },
      { id: P + 'C0134', ss: 15.3, b: 3 },
      { id: P + 'C0135', ss: 28.0, b: 3 },
      { id: P + 'C0135', ss: 82.0, b: 3 },
      { id: P + 'C0136-001', ss: 27.5, b: 3 },
      { id: P + 'C0136-001', ss: 66.0, b: 3 },
      { id: P + 'C0136-001', ss: 100.5, b: 3 },
      { id: P + 'C0136-001', ss: 172.5, b: 3 },
      { id: P + 'C0136-001', ss: 200.0, b: 3 },
      { id: P + 'C0136-001', ss: 252.0, b: 3 },
      { id: P + 'C0137-002', ss: 12.0, b: 3 },
      { id: P + 'C0137-002', ss: 69.0, b: 3 },
      { id: P + 'C0137-002', ss: 106.5, b: 3 },
      { id: P + 'C0137-002', ss: 153.5, b: 3 },
      { id: P + 'C0137-002', ss: 184.0, b: 3 },
      { id: P + 'C0137-002', ss: 246.5, b: 3 },
      { id: P + 'C0137-002', ss: 306.0, b: 7 },
      { foto: EV + '/cikti/fotograf/DSC04988-2A-bufe-dekor.jpg', fy: 0.5, b: 6 } ] },  // toplu plaket fotoğrafı
    { ad: 'eglence', clips: [                      // b200-256, dosya sırası
      { id: 'C0078', ss: 0.5, b: 4 },
      { id: 'C0082', ss: 0.3, b: 4 },
      { id: 'C0084', ss: 0.3, b: 4 },
      { id: 'C0088', ss: 0.3, b: 4 },
      { id: 'C0100', ss: 0.3, b: 4 },
      { id: 'C0102', ss: 8.8, b: 4 },               // 8.0-8.75 kamera savruluyor
      { id: 'C0106', ss: 0.2, b: 4 },
      { id: 'C0110', ss: 1.5, b: 4 },
      { id: 'C0115', ss: 0.3, b: 4 },
      { id: 'C0119', ss: 1.8, b: 4 },
      { id: 'C0123', ss: 0.0, b: 4 },
      { id: 'C0124', ss: 1.0, b: 4 },
      { id: 'C0129', ss: 2.0, b: 4 },
      { id: 'C0130', ss: 9.0, b: 4 } ] },
  ],
};
