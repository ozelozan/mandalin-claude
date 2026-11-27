# Çengelköy Final'in Bursluluk Sınavı Reels v1

Çıktı: `cikti/cengelkoy-final-bursluluk-reels-v1.mp4` (1080x1920, 30 fps, 25,8 sn, -14,8 LUFS, tepe -1,6 dB).

- Tek sahne: afiş parçaları seslendirmeye kilitli girer, ekran değişmez. QR yok.
- Ses: Ayla Demir (Magnific TTS 200, eleven_v3, stability 0.35, hız 1.05) → `ses/vo-ayla.mp3`, kelime zamanları `ses/vo-ayla-kelime.json`.
- Akış: 0 "Geleceğin için ilk adımı at!" kelime kelime · 2,0 çengelköy / final'in / BURSLULUK düşer · 4,0 SINAVI çakılır (sarsıntı + flaş) · 4,4 9-10 OCAK rozeti · 5,9 "4," ve 7,0 "11." büyük vurgu, diğer sınıflar sırayla · 8,2 öğrenci iner · 10,6 başlık parlar (ikinci vurgu) · 12,6 Online Kayıt bandı, 14,6 adres nabzı · 16,9 telefon hapı, rakamlar okundukça · 21,6 logo · 23,5 "Geleceğin Final'de!" + tüm afiş nabzı.
- Efektler: pop, parıltı (Magnific SFX), whoosh/vuruş/damga ve müzik VIP bursluluk Reels'inden. Miks: `kaynak/ses_miks.py` (müzik sidechain ile sesin altında).
- Görüntü: `hf/index.html` (HyperFrames 0.8.216, GSAP). Parçalar `../3b-parcalar/parcalar/`.
- Render: `cd hf && npx hyperframes@0.8.216 render -o ../cikti/goruntu.mp4 -q delivery --fps 30`, sonra ses miksle birleştir.
- Beykoz uyarlaması: şube yazısı, çizgiler, logo, telefon (0216 322 60 50) ve seslendirme değişir.

## v2 (27 Kas 2026) — Ozan revizyonları
`cikti/cengelkoy-final-bursluluk-reels-v2.mp4` (25,8 sn, -14,9 LUFS).
- Montserrat Türkçe karakterli yerel dosyadan (`hf/assets/fonts/`): GELECEĞİN / Geleceğin'deki bozuk Ğ ve İ düzeldi.
- Alt düzen: Online Kayıt bandı → altında ortalı, daha büyük logo (bantla birlikte 12,6 sn'de gelir, ikisi de sabit kalır) → telefon → tek satır "Geleceğin **Final'de!**" (Final'de sarı). Yapay zekâ notu kaldırıldı.
- Öğrenci U'nun üstüne oturuyor, bacaklar K'nin önünden sarkıyor (seat çizgisi görselin %59'u, BURSLULUK üst yüzü y=646).
- Çizgiler SVG olarak yeniden çizildi ve hedefleriyle sırayla geliyor: dalga+ok çengelköy ile (2,0), sol ok BURSLULUK ile (3,2), sağ ok SINAVI ile (4,0), üst yay rozete değerek (4,05), rozetin sağından çıkan yay öğrencinin arkasına (7,7). Ok kuyrukları ekran kenarına dayalı, bacak yanındaki ince çizgi yok.
