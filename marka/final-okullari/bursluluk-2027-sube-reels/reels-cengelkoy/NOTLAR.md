# Çengelköy Final'in Bursluluk Sınavı Reels v1

Çıktı: `cikti/cengelkoy-final-bursluluk-reels-v1.mp4` (1080x1920, 30 fps, 25,8 sn, -14,8 LUFS, tepe -1,6 dB).

- Tek sahne: afiş parçaları seslendirmeye kilitli girer, ekran değişmez. QR yok.
- Ses: Ayla Demir (Magnific TTS 200, eleven_v3, stability 0.35, hız 1.05) → `ses/vo-ayla.mp3`, kelime zamanları `ses/vo-ayla-kelime.json`.
- Akış: 0 "Geleceğin için ilk adımı at!" kelime kelime · 2,0 çengelköy / final'in / BURSLULUK düşer · 4,0 SINAVI çakılır (sarsıntı + flaş) · 4,4 9-10 OCAK rozeti · 5,9 "4," ve 7,0 "11." büyük vurgu, diğer sınıflar sırayla · 8,2 öğrenci iner · 10,6 başlık parlar (ikinci vurgu) · 12,6 Online Kayıt bandı, 14,6 adres nabzı · 16,9 telefon hapı, rakamlar okundukça · 21,6 logo · 23,5 "Geleceğin Final'de!" + tüm afiş nabzı.
- Efektler: pop, parıltı (Magnific SFX), whoosh/vuruş/damga ve müzik VIP bursluluk Reels'inden. Miks: `kaynak/ses_miks.py` (müzik sidechain ile sesin altında).
- Görüntü: `hf/index.html` (HyperFrames 0.8.216, GSAP). Parçalar `../3b-parcalar/parcalar/`.
- Render: `cd hf && npx hyperframes@0.8.216 render -o ../cikti/goruntu.mp4 -q delivery --fps 30`, sonra ses miksle birleştir.
- Beykoz uyarlaması: şube yazısı, çizgiler, logo, telefon (0216 322 60 50) ve seslendirme değişir.
