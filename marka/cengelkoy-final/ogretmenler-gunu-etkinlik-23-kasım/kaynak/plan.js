// Final Okulları Öğretmenler Günü Gecesi (23 Kasım 2026) - yatay etkinlik videosu kurgu planı v3
// v3: C0048 çıktı, sunucu 2. plan ve son plaket kaydırıldı (maytap dumanı).
// v2: ilk tam izlemeden sonra 7 plan düzeltildi (bulanık/yakın kişi, savrulan kamera)
// Müzik: muzik/fon-muzigi-v1.mp3 (Magnific / ElevenLabs Music v2, sözsüz), 110 BPM, ilk vuruş 0.505 sn.
// Sakin giriş 0-47. vuruş, patlama 47. vuruş (26.1 sn), son akor 287. vuruş (157 sn).
// b = vuruş sayısı, ss = kaynak başlangıç sn, hiz 0.5 = %50 ağır çekim (100 fps kaynak).
// Bölüm başları 4'lük ölçü başına (47 + 4n) denk gelir; bölüm geçişleri zoom geçişidir.
const EV = '/Volumes/Mini_MAN/mandalin-claude/marka/cengelkoy-final/ogretmenler-gunu-etkinlik-23-kasım';
const P = 'plaket töreni/';

module.exports = {
  fps: 25, bpm: 110, faz: 0.505,
  kamera: EV + '/videolar',
  muzik: EV + '/muzik/fon-muzigi-v1.mp3',
  kartVurus: 275,      // logo kartının girdiği vuruş
  sonAkor: 287,
  bitisSn: 163.5,      // video sonu (müzik sönümü + beyaz)
  baslik: ['FİNAL OKULLARI', 'Öğretmenler Günü Gecesi', '23 Kasım 2026'],
  kartMesaj: '24 Kasım Öğretmenler Günümüz Kutlu Olsun',
  bolumler: [
    { ad: 'salon', clips: [
      { id: 'C0013', ss: 0.4, b: 12, hiz: 0.5 },      // boş salon, masa lambaları (başlık üstünde)
      { id: 'C0027', ss: 1.3, b: 7, hiz: 0.5 },       // "Öğretmenler günümüz kutlu olsun" balonu
      { id: 'C0030', ss: 0.4, b: 7, hiz: 0.5 },       // isimlikli masa
      { id: 'C0037', ss: 1.5, b: 6, hiz: 0.5 },       // tebrik kartı tabağa bırakılıyor
      { id: 'C0020', ss: 0.5, b: 7, hiz: 0.5 },       // nostaljik raf
      { id: 'C0038', ss: 1.2, b: 8, hiz: 0.5 } ] },  // masa lambası yanıyor -> patlama
    { ad: 'karsilama', clips: [
      { id: 'C0041', ss: 0.3, b: 8 },
      { id: 'C0041', ss: 4.8, b: 6 },
      { id: 'C0042', ss: 1.2, b: 8 },
      { id: 'C0044', ss: 5.5, b: 6 } ] },
    { ad: 'hediye', clips: [
      { id: 'C0046', ss: 1.8, b: 8 },
      { id: 'C0047', ss: 2.8, b: 6 },
      { id: 'C0047', ss: 8.8, b: 5 },
      { id: 'C0052', ss: 0.5, b: 9 } ] },           // C0048 çıktı: önde bulanık kol ve bere
    { ad: 'yemek', clips: [
      { id: 'C0050', ss: 0.3, b: 4 },               // C0049 çıktı: kameraya çok yakın bulanık yüz
      { id: 'C0066', ss: 0.3, b: 4 },
      { id: 'C0066', ss: 6.0, b: 4 } ] },
    { ad: 'sunucu', clips: [
      { id: 'C0073', ss: 2.4, b: 5 },               // 6.5 sn sonrası kamera savruluyor
      { id: 'C0073', ss: 20.9, b: 7 } ] },          // 20.3'te kamera savrulması bitmemiş
    { ad: 'kurucu', clips: [
      { id: 'C0074 - kurucu', ss: 9.5, b: 6 },
      { id: 'C0074 - kurucu', ss: 38.3, b: 6 },
      { id: 'C0074 - kurucu', ss: 67.3, b: 6 },
      { id: 'C0074 - kurucu', ss: 112.3, b: 6 } ] },  // salon alkışlıyor (kameraman geçtikten sonra)
    { ad: 'plaket', clips: [
      { id: 'C0069', ss: 0.6, b: 8, hiz: 0.5 },        // plaketler masada
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
      { id: P + 'C0137-002', ss: 306.0, b: 7 } ] },   // son plaket: maytap anı alınmadı (önde garson kolu, duman sigara gibi görünüyor)
    { ad: 'eglence', clips: [
      { id: 'C0084', ss: 0.3, b: 4 },
      { id: 'C0087', ss: 0.2, b: 3 },
      { id: 'C0090', ss: 3.0, b: 4 },
      { id: 'C0097', ss: 8.6, b: 4 },
      { id: 'C0101', ss: 6.0, b: 3 },
      { id: 'C0102', ss: 8.0, b: 5 },
      { id: 'C0105', ss: 0.8, b: 4 },               // C0107 çıktı: önde bulanık garson
      { id: 'C0110', ss: 1.5, b: 4 },
      { id: 'C0110', ss: 7.5, b: 3 },
      { id: 'C0111', ss: 0.2, b: 4 },
      { id: 'C0115', ss: 0.3, b: 4 },
      { id: 'C0119', ss: 1.8, b: 5 },
      { id: 'C0124', ss: 1.0, b: 4 },
      { id: 'C0125', ss: 2.6, b: 3 },               // 8 sn civarı önde bulanık el
      { id: 'C0130', ss: 9.0, b: 4 },
      { id: 'C0130', ss: 18.5, b: 2 } ] },
  ],
};
