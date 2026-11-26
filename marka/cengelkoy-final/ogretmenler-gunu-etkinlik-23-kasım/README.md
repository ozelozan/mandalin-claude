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
`node kaynak/kurucu.js <çalışma-klasörü> <çıktı.mp4>` → `cikti/Kurucu-Ertug-Ertas-Ogretmenler-Gunu-Konusmasi-v3.mp4` (1:27; v3: belini düzelttiği an çıktı, konuşma "Hoş geldiniz" ile başlar).
- Kaynak: C0073 (sunucunun çağrısı) + C0074 (konuşma). Kesimler faster-whisper kelime zamanlarına göre.
- Sunucu kamerası savrulan anlarda ses sürer, görüntü salona geçer.
- Çıkanlar: baştaki "Şimdi…" ve bekleme, sunucunun "dokuzuncu" demesini düzelten "kimine göre dokuz, on" bölümü, uzun alkış ve sessizlik boşlukları.
- Aynı kameradaki kesimlerde kadraj 1.0 / 1.12 dönüşümlü (sıçrama hissi olmasın). İsim yazısı: "Ertuğ Ertaş / Kurucu" (v4, 25 Kasım: "Final Okulları" ibaresi çıkarıldı; son sürüm `cikti/Kurucu-Ertug-Ertas-Ogretmenler-Gunu-Konusmasi-v4.mp4`).
- Ses: konuşma -16 LUFS, tepe -2 dBTP. Sonda alkış, ardından fon müziğinin son ölçüleriyle 4 logolu beyaz kart.

## Fotoğraf: DSC04988-2A büfe dekoru
`cikti/fotograf/DSC04988-2A-bufe-dekor.jpg` (5801x3234; orijinal `fotoğraflar/plaket/` içinde dokunulmadan duruyor).
- Arka büfedeki ve sol kemerli raflardaki içki şişeleri yerine vazo, pampas, zeytin dalı, pirinç figür, kitap ve şamdan.
- Üretim Magnific retouch (Nano Banana Pro) ile maskeli; büyük karede sağ bölme ve sol kemerler tutmadığı için ayrı kırpımlarla yapıldı.
- `kaynak/bufe-dekor.py` birleştirir: insan maskesindeki (SAM 3.1) her piksel orijinalden birebir geri yazılır (doğrulama: 739.120 insan pikseli, 0 değişen). Ara dosyalar `cikti/fotograf/ara-dosyalar/`.

## Paradise sürümü (Ozan'ın müziği)
`node kaynak/kur.js kaynak/plan-paradise.js <çalışma> <çıktı>` → `cikti/Final-Okullari-Ogretmenler-Gunu-Gecesi-2026-Paradise-v2.mp4` (2:42).
- Müzik `muzik/#40 Paradise (Official).mp4`: sözsüz (konuşma tanıma söz bulmadı), 103 BPM, faz 0,085 sn; tek parça, kesintisiz. b256'daki sakin bölüme düşüşte logo kartı girer, sonda 3 sn sönüm.
- Yavaş çekim yok (titreme yapıyordu). Girişte mekan planı azaltıldı; Çengelköy/Beykoz/Yakacık isimlikleri `fotoğraflar/denemeler` içinden (yalnız okundu). Yakacık isimliğinin yanındaki markalı rakı bardağı kırpımla kadraj dışı.
- Karşılama doğrudan tokalaşmayla başlar; kurucunun belini düzelttiği an (C0074 9.5-11.2) çıktı.
- Bölüm aralarında fotoğraf planları (hediye, Beykoz idari kadro masası, masada öğretmenler, büfe dekorlu toplu plaket). Personel/boş masa ve içki rafı görünen fotoğraflar kullanılmadı.
- Eğlence: önceki sürümde kullanılmayan C0078, C0082, C0088, C0100, C0106, C0123, C0129 + en iyi eski planlar.
- kur.js artık fotoğraf planı alır: `{ foto, fy, kz, fx, b }`.

## Fotoğraf albümü videosu (24 Kasım 2026)
`node kaynak/kur.js kaynak/plan-fotograf.js <çalışma> <çıktı>` → `cikti/Final-Okullari-Ogretmenler-Gunu-Gecesi-2026-Fotograf-Albumu-v1.mp4` (1:44).
- Paradise müziği, 33 kolaj (tek/ikili/üçlü/dörtlü/büyük+iki küçük), olay sırası: karşılama, hediye, masalar, konuşmalar, plaketler, eğlence; sonda aynı 4 logolu beyaz kart.
- Kolajlar `kaynak/kolaj.py` ile `<etkinlik>/kolaj/` klasörüne üretilir (yeniden üretilebilir, git dışı).
- Tebrik kartı fotoğrafı bulanık olduğu için yerine hediye ikilisi kondu; video baştan sona izlendi.

## Fotoğraf albümü v2: çerçeveli baskılar (24 Kasım 2026)
`python3 kaynak/album.py <çalışma>` (govde.mp4) + `node kaynak/kur.js kaynak/plan-album.js <çalışma> <çıktı> kart|final`
→ `cikti/Final-Okullari-Ogretmenler-Gunu-Gecesi-2026-Fotograf-Albumu-v2.mp4` (1:44).
- Ozan v1 kolajları beğenmedi. v2: her fotoğraf beyaz çerçeveli baskı, sahnenin bulanık ışığı önüne vuruşta düşer/kayar/büyür, albüm gibi birikir; sahne geçişi öne büyüyüp kararma.
- Sahneler: açılış (sahne, Öğretmenler Günü ekranı), karşılama (3 farklı misafir), hediye (4), masalar (2x4), konuşmacılar (sunucu, kurucu, solist, mavi gömlekli konuşmacı: tek sahne, farklı kişiler), 16 plaket üst üste birikir + toplu fotoğraf, eğlence (2x4), 4 logolu beyaz kapanış.
- `fotoğraflar/denemeler kullanma` klasörü kullanılmaz (Ozan adını değiştirdi).
- v3 (25 Kasım): plaketlere `plaket/zeynep-veysel hoca.jpg` eklendi (b117); plaket dışı sahnelerde giriş animasyonu 11 kare (plaketlerde 18), sahne geçişi 6 kare. Çıktı `cikti/...-Fotograf-Albumu-v3.mp4`.
- v4 (25 Kasım): kısa sürüm 1:11. Plaket bölümü aynı, diğer sahnelerde baskılar 1-2 vuruşta bir; müzik 56 vuruş ileriden kesintisiz başlar (1,5 sn ses girişi), logo kartı parçanın düşüşüne oturur. `cikti/...-Fotograf-Albumu-v4.mp4`.
- v5 (25 Kasım): plaketler plaket verene göre sıralı (1. kurucu 04931-36, 2. kurucu 04940-48, 3: 04959/62, 4: 04965/66, 5: 04955/58, 6: 04950/52), sonra 04970 + Zeynep-Veysel Hoca ortada yan yana, en son toplu; konuşmacılar soldan: kurucu, mavi gömlekli, sunucu, solist. `cikti/...-Fotograf-Albumu-v5.mp4` (1:11).
- Kopya sürüm (25 Kasım): v5 + 6 masa fotoğrafı (04737, 04752, 04751, 04738, 04749, 04731) masalardan sonra 3+3 dizilimde. `python3 kaynak/album-ek.py` + `plan-album-ek.js` → `cikti/...-Fotograf-Albumu-v5-ek-masalar.mp4` (1:18). v5 değişmedi. Not: 04752/04751/04749 arka planında içki rafı görünüyor (Ozan istedi).

## Çengelköy Final Reels (10. yıl, 26 Kasım 2026)
`python3 kaynak/reels-cengelkoy.py <çalışma> <çıktı>` → `cikti/Cengelkoy-Final-Ogretmenler-Gunu-Gecesi-2026-Reels-v1.mp4` (dikey, 48 sn).
- Yakacık Reels v3'ün uyarlaması (aynı müzik, aynı geçişler, çerçeveli baskılar, hareketli 3B rozet). Rozet "10. YILIMIZ": `sticker/rozet-10.png` (GPT 2.6, Yakacık rozeti referans; 10b alternatif).
- Sıra Ozan'ın: 04792 açılış (tam ekran, başlık "Öğretmenler Günü Gecesi", tarih yok) → masalar 04722+04724, 04728+04737, 04742+04759, 04772+04774 → 04690 → plaketler 04936, 04959, 04962, 04965, 04966, 04970, Zeynep-Veysel Hoca → eğlence 04802+04883, 04912 (tek baskı) → 45. sn'de beyaz zeminde yalnızca Çengelköy Final logosu.
- Her sahnede alt ortada Çengelköy Final logosu (logo-beyaz-yazi.png 557. satırdan bölünüp amblem + beyaz yazı yan yana, plakasız). Açıklama `instagram-aciklama-reels-10-yil.txt`.
- v2 (26 Kasım): Ozan'ın isteğiyle sondaki tek baskı (04912) çıktı; süresi masa çiftlerine (8'er vuruş) ve eğlence çiftine (10 vuruş) dağıtıldı, süre yine 48 sn. `cikti/...-Reels-v2.mp4`.
