# Çağdaş Bilgi Öğretmenler Günü Gecesi (24 Kasım 2026, Sur Salon): yatay etkinlik videosu

Kaynak videolar (git dışı, 7,6 GB, 76 klip, 1080p 100 fps): `~/Mini_MAN/mandalin-claude/marka/cadgas bilgi kurs/Çağdaş Bilgi Öğretmenler Günü Gecesi 2026/videolar/`
Çıktı: aynı klasörde `cikti/`, müzik `muzik/fon-muzigi-v1.mp3` (git dışı).

## Çalıştırma
```
export PATH=~/tools/bin:$PATH
cd kaynak
node kur.js plan.js <çalışma-klasörü> <çıktı.mp4>     # adımlar: olc | segmentler | govde | kart | final
```
`kur.js`, Final Okulları gecesinin hattından (`marka/cengelkoy-final/ogretmenler-gunu-etkinlik-23-kasım/kaynak/kur.js`) türedi.
Plan değişince yalnızca değişen segmentler yeniden işlenir.

## Kurgu (v1; v2 farkları Sürümler bölümünde)
- Yatay 1920x1080, 25 fps, 2:18. Sıra kronolojik (dosya numarası = çekim sırası).
- Müzik: Magnific (ElevenLabs Music v2) ile üretilen sözsüz, hareketli parça, 120 BPM, faz 0,488 sn. Parça 12. saniyeden başlar;
  patlama videonun 20. saniyesinde (39. vuruş), logo kartı 259. vuruşta parçanın çözülüşüne oturur.
- Bölümler: boş sahneler + başlık (Sur Salon tabelası, masalar, sahne ekranı) → karşılama → canlı müzik → kurucu konuşması →
  masalarda çekiliş kâsesi → yemek, solist, kolej tanıtımı → plaket töreni → sahnede hediye çekilişi → eğlence/halay → iki logo.
- Başlık: "ÇAĞDAŞ BİLGİ EĞİTİM KURUMLARI / Öğretmenler Günü Gecesi / 24 Kasım 2026" (Montserrat Bold/ExtraBold, beyaz + gölge,
  koyu yumuşak bant, kırmızı ayraç). Fontlar `kaynak/fonts/` (Türkçe tam, OFL).
- Kapanış: beyaz zemin, solda Çağdaş Bilgi Eğitim Kurumları, sağda Çağdaş Bilgi Koleji, ortada ince gri ayraç, altta
  "24 Kasım Öğretmenler Günümüz Kutlu Olsun" (`kaynak/logo-karti.py`, orijinal logolar yalnız ölçeklenir).

## Görüntü işleme (kur.js)
- 100 fps kaynak 4 kare karışımla 25 fps'e; yavaş çekim yok (Final gecesinde titreme yapmıştı).
- vidstab sabitleme (smoothing 22, zoom %4), klip başına otomatik pozlama (gamma 0,90-1,55), vurgu tavanı ~%88 (sahne ekranı patlamaz),
  karanlık planlara hafif gürültü azaltma; 2x ölçekte yavaş itme/çekme, bölüm geçişlerinde zoom geçişi.

## Alınmayan anlar
- C0152 sonu, C0153 sonu, C0245 sonu: kameraya çok yakın geçen kişi. C0157: kameraya yaklaşan yüz.
- C0237 7,5-10 sn: kameranın önünde bulanık eller (v1 kontrolünde 11,0 sn'ye kaydırıldı).
- C0180 başı: duvar ve içecek kasası; sonu: garsonun sırtı kadrajı kapatıyor.
- C0185 başı (yer karosu), C0189/C0190 başı (boş pist), C0206 başı, C0237 başı (karanlık sırtlar).

## Sürümler
- v1 (25 Kasım 2026): `cikti/Cagdas-Bilgi-Ogretmenler-Gunu-Gecesi-2026-v1.mp4` (2:18, -14,0 LUFS, tepe -2 dBFS; render sonrası `volume=-1dB`, video kopya). Saniyelik karelerle izlendi, kulakla dinlenmedi.
- v2 (25 Kasım 2026, Ozan'ın isteği): `cikti/Cagdas-Bilgi-Ogretmenler-Gunu-Gecesi-2026-v2.mp4` (2:00, -14,5 LUFS, tepe -1,9 dBFS). Boş sahneler 20 sn yerine 7,5 sn ve 1,5x hızlı (C0141 çıktı); başlık yalnız Sur Salon planında (0,5-4,4 sn). Müzik 24. sn'den başlar, patlama videonun 8. sn'sinde. C0154, C0240, C0244 kısaldı, C0178 çıktı. Müzik logo kartından itibaren 8 sn doğrusal sönümle biter. v1'deki ani kesilmenin nedeni, loudnorm'un sönümü yükseltmesi ve ardından gelen 1 sn'lik fade'di. Ses artık ayrı işleniyor (`muzik.wav`), loudnorm fade'den önce uygulanıyor. Kulakla dinlenmedi.
