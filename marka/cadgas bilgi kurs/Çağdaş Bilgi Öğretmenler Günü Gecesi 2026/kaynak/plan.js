// Çağdaş Bilgi Eğitim Kurumları Öğretmenler Günü Gecesi (24 Kasım 2026, Sur Salon) - yatay etkinlik videosu kurgu planı v3
// v3 (Ozan): plaket ve ödül fotoğraflarından 3 sahne (beyaz zeminli baskılar, foto-sahne.py); süre yine 2:00.
// v2 (Ozan): toplam 2:00; boş sahneler 1,5x hızlı ve kısa (7,5 sn); müzik logo kartında 6 sn yumuşak sönümle biter.
// Müzik: muzik/fon-muzigi-v1.mp3 (Magnific / ElevenLabs Music v2, sözsüz), 120 BPM, faz 0.488 sn.
// Müzik 24. saniyeden başlar (muzikBas): patlama videoda 15. vuruş (8,0 sn), logo kartı 223. vuruş (112 sn).
// b = vuruş sayısı (0,5 sn), ss = kaynak başlangıç sn, hiz 1.5 = hızlandırılmış. Yavaş çekim yok (titreme yapıyor, Final dersi).
// Bölüm başları 4'lük ölçü başına (15 + 4n) denk gelir; bölüm geçişleri zoom geçişidir.
// Sıra kronolojik (dosya numarası = çekim sırası).
const EV = '/Volumes/Mini_MAN/mandalin-claude/marka/cadgas bilgi kurs/Çağdaş Bilgi Öğretmenler Günü Gecesi 2026';

module.exports = {
  fps: 25, bpm: 120, faz: 0.488,
  kamera: EV + '/videolar',
  muzik: EV + '/muzik/fon-muzigi-v1.mp3',
  muzikBas: 24.0,
  muzikSonus: 8.0,     // logo kartı girdiği andan (112 sn) itibaren yumuşak sönüm
  kartVurus: 223,
  sonAkor: 233,        // +3 vuruş: beyaza geçiş (~118,5 sn)
  bitisSn: 120.0,
  baslik: ['ÇAĞDAŞ BİLGİ EĞİTİM KURUMLARI', 'Öğretmenler Günü Gecesi', '24 Kasım 2026'],
  kartMesaj: '24 Kasım Öğretmenler Günümüz Kutlu Olsun',
  bolumler: [
    { ad: 'salon', clips: [                          // boş sahneler (başlık ilk planın üstünde)
      { id: 'C0143', ss: 0.1, b: 9, hiz: 1.5 },      // SUR SALON tabelası, içeri giriş (başlık yalnız bu planda)
      { id: 'C0146', ss: 0.5, b: 3, hiz: 1.5 },      // logolu masa bayrakları
      { id: 'C0151', ss: 2.5, b: 3, hiz: 1.5 } ] },  // sahne ekranında logo -> patlama (C0141 v2'de çıktı)            // sahne ekranında logo -> patlama
    { ad: 'karsilama', clips: [
      { id: 'C0152', ss: 11.5, b: 8 },
      { id: 'C0153', ss: 0.8, b: 6 },
      { id: 'C0154', ss: 2.8, b: 6 },
      { id: 'C0158', ss: 3.0, b: 8 } ] },
    { ad: 'muzik', clips: [
      { id: 'C0163', ss: 1.0, b: 8 },
      { id: 'C0160', ss: 2.0, b: 8 } ] },
    { ad: 'kurucu', clips: [
      { id: 'C0171', ss: 1.0, b: 8 },
      { id: 'C0164', ss: 7.0, b: 6 },
      { id: 'C0169', ss: 2.0, b: 6 } ] },
    { ad: 'masalar', clips: [                        // masalarda çekiliş kâsesi
      { id: 'C0174', ss: 3.0, b: 6 },
      { id: 'C0176', ss: 5.0, b: 5 },
      { id: 'C0179', ss: 8.0, b: 5 } ] },
    { ad: 'yemek', clips: [
      { id: 'C0180', ss: 7.5, b: 5 },                // servis (duvar/kasa anı alınmadı)
      { id: 'C0181', ss: 1.5, b: 6 },
      { id: 'C0183', ss: 1.2, b: 5 } ] },            // kolej tanıtımı ekranda
    { ad: 'plaket', clips: [
      { id: 'C0159', ss: 2.0, b: 4 },                // plaketler masada
      { id: 'C0185', ss: 3.0, b: 4 },
      { id: 'C0187', ss: 2.5, b: 3 },
      { id: 'C0188', ss: 1.8, b: 3 },
      { sahne: 'plaket1', b: 14 },                   // fotoğraf: 7 plaket baskısı
      { sahne: 'plaket2', b: 12 } ] },               // fotoğraf: 4 tekli + 2 toplu plaket
    { ad: 'cekilis', clips: [
      { id: 'C0194', ss: 0.0, b: 4 },
      { id: 'C0217', ss: 1.0, b: 4 },
      { id: 'C0221', ss: 0.3, b: 4 },
      { sahne: 'odul', b: 16 } ] },                  // fotoğraf: 6 ödül + ödül verenler toplu
    { ad: 'eglence', clips: [
      { id: 'C0223', ss: 1.5, b: 4 },
      { id: 'C0225', ss: 0.3, b: 5 },
      { id: 'C0229', ss: 1.0, b: 4 },
      { id: 'C0237', ss: 11.0, b: 5 },
      { id: 'C0238', ss: 0.3, b: 5 },
      { id: 'C0240', ss: 0.5, b: 4 },
      { id: 'C0242', ss: 1.0, b: 4 },
      { id: 'C0243', ss: 2.5, b: 5 },
      { id: 'C0244', ss: 2.0, b: 4 },
      { id: 'C0245', ss: 2.8, b: 4 } ] },
  ],
};
