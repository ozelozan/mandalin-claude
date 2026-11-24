# Final Okulları Öğretmenler Günü Gecesi (23 Kasım 2026) - yatay etkinlik videosu

Kaynak videolar (git dışı, ~21 GB): `~/Mini_MAN/mandalin-claude/marka/cengelkoy-final/ogretmenler-gunu-etkinlik-23-kasım/videolar/`
(`01-denemeler/` ve `fotoğraflar/` kullanılmadı.) Çıktı: aynı klasörde `cikti/`, müzik `muzik/fon-muzigi-v1.mp3`.

## Çalıştırma
```
export PATH=~/tools/bin:$PATH
cd kaynak
node kur.js plan.js <çalışma-klasörü> <çıktı.mp4>          # hepsi: olc, segmentler, govde, kart, final
```
Plan değişince yalnızca değişen segmentler yeniden işlenir (segment adı içerikten türer).

## Kurgu
- Yatay 1920x1080, 25 fps, 2:43,5. Müzik: Magnific (ElevenLabs Music v2) ile üretilen sözsüz parça, 110 BPM, ilk vuruş 0,505 sn.
- Sakin giriş (0-26 sn) = salon detayları, ağır çekim, başlık. 47. vuruştaki patlamada karşılama başlar; bölümler 4'lük ölçü başında.
- Sıra: salon, karşılama, hediye, yemek, sunucu, kurucu konuşması, plaketler (17 kişi, her biri ~1,6 sn), eğlence, 4 kurum logosu, beyaz.
- Başlık: "FİNAL OKULLARI / Öğretmenler Günü Gecesi / 23 Kasım 2026" (Georgia, Çengelköy serisiyle aynı aile).
- Kapanış: beyaz zeminde Çengelköy Final, Yakacık Final, Beykoz Final, Çengelköy Final VIP; eşit sütun, ince gri ayraç, logolar vuruşlarda sırayla; son akordan sonra saf beyaz.

## Görüntü işleme
- 100 fps kaynak: 1x planlar 4 kare karışımla 25 fps'e, ağır çekim planlar %50 (2 kare karışım).
- vidstab sabitleme (smoothing 22, zoom %4).
- Klip başına otomatik pozlama: 3 karenin ortalama parlaklığı ölçülür, gamma 0,90-1,55 aralığında hedefe çekilir; açılan karanlık planlara hafif kontrast ve gürültü azaltma.
- Vurgu eğrisi beyaz tavanı ~%88: sahne ekranı patlamıyor (ölçüm: ≥235 piksel oranı kare başına en fazla %0,64).
- 2x ölçekte zoompan ile yavaş itme/çekme (dönüşümlü), bölüm geçişlerinde 7 karelik zoom geçişi + kısa bulanıklık.

## Kurallar (Ozan'ın açık talepleri)
- Bel altını gösteren kare yok (plaket kliplerinde yalnızca bacak görünen anlar var, alınmadı).
- Sigara içen kişi yok.
- Kameraya çok yakın / bulanık geçen kişi yok (v2'de 7 plan bu yüzden değişti).

## Kurucu konuşması videosu (Ertuğ Ertaş)
`node kaynak/kurucu.js <çalışma-klasörü> <çıktı.mp4>` → `cikti/Kurucu-Ertug-Ertas-Ogretmenler-Gunu-Konusmasi-v2.mp4` (1:28).
- Kaynak: C0073 (sunucunun çağrısı) + C0074 (konuşma). Kesimler faster-whisper kelime zamanlarına göre.
- Sunucu kamerası savrulan anlarda ses sürer, görüntü salona geçer.
- Çıkanlar: baştaki "Şimdi…" ve bekleme, sunucunun "dokuzuncu" demesini düzelten "kimine göre dokuz, on" bölümü, uzun alkış ve sessizlik boşlukları.
- Aynı kameradaki kesimlerde kadraj 1.0 / 1.12 dönüşümlü (sıçrama hissi olmasın). İsim yazısı: "Ertuğ Ertaş / Kurucu, Final Okulları".
- Ses: konuşma -16 LUFS, tepe -2 dBTP. Sonda alkış, ardından fon müziğinin son ölçüleriyle 4 logolu beyaz kart.

## Fotoğraf: DSC04988-2A büfe dekoru
`cikti/fotograf/DSC04988-2A-bufe-dekor.jpg` (5801x3234; orijinal `fotoğraflar/plaket/` içinde dokunulmadan duruyor).
- Arka büfedeki ve sol kemerli raflardaki içki şişeleri yerine vazo, pampas, zeytin dalı, pirinç figür, kitap ve şamdan.
- Üretim Magnific retouch (Nano Banana Pro) ile maskeli; büyük karede sağ bölme ve sol kemerler tutmadığı için ayrı kırpımlarla yapıldı.
- `kaynak/bufe-dekor.py` birleştirir: insan maskesindeki (SAM 3.1) her piksel orijinalden birebir geri yazılır (doğrulama: 739.120 insan pikseli, 0 değişen). Ara dosyalar `cikti/fotograf/ara-dosyalar/`.
