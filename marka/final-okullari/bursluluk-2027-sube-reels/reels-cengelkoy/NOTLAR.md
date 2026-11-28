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

## v3 (27 Kas 2026)
`cikti/cengelkoy-final-bursluluk-reels-v3.mp4`: telefon hapında "0216" rakamlarla aynı taban çizgisine hizalandı (align-items: baseline).

## v4 — Deniz Altaş gerçek seslendirme (28 Kas 2026)
`cikti/cengelkoy-final-bursluluk-reels-v4-deniz.mp4` (26 sn, -14,2 LUFS, tepe -1,4 dB).
- Ses: `deniz_altas seslendirme/Çengelköy Final Okulları_3.wav` (29,1 sn) → `kaynak/ses_duzenle.py` ile boşluklar 0,16 sn'ye kısaltıldı (12 ms geçiş), hafif EQ + kompresör, %3 hız → `ses/vo-deniz.wav` (24,9 sn). Kelime zamanları `ses/vo-deniz-kelime.json`.
- Sözle senkron yapı: her öğe adı söylendiğinde gelir, tekrar anılınca tepki verir (çengelköy/final'in nabzı, "9-10 Ocak"ta rozet iki kez atar, "4." ve "11." büyük vurgulu, "tüm"de bütün sınıflar dalga gibi zıplar, "öğrencilerimizi"de öğrenci oturur, "bekliyoruz"da 4 ve 11 göz kırpar).
- "Başarını fırsata dönüştürmek için hemen başvurunu yap" ekranda karşılığı olmadığı için alt boşlukta kelime kelime ara yazı (BAŞARINI FIRSATA DÖNÜŞTÜR! HEMEN [BAŞVUR]); "Online kayıt"ta yerini bant + logoya bırakır.
- Bant ve logo sabit: adres okunurken bandın üstünden ışık geçer, "Çengelköy Final Okulları"nda logonun arkası parlar.
- Beykoz için aynı hat: `deniz_altas seslendirme/Beykoz Final Okulları_3.wav`.

## v5 (28 Kas 2026): `cikti/cengelkoy-final-bursluluk-reels-v5-deniz.mp4`
- Ses hızlandırılmadı (atempo yok); kelime sonlarına 0,12 sn pay bırakıldı, "Okulları" net duyuluyor.
- Görüntü zamanları v4 sesine göre yazılı; `ses/zaman-esleme-v4-v5.json` (44 kelime eşlemesi) ile v5 sesine otomatik kaydırılıyor (index.html başındaki T() sarmalayıcısı ve ses_miks.py).
- Sınıflar satırında pop dizisi kaldırıldı, satır tamamlanınca tek efekt.
- 27,2 sn, -14,1 LUFS, tepe -1,4 dB.
- Ders: ses_miks.py'de seslendirme ve müzik aynı süreye sabitlenmezse (apad+atrim) ffmpeg sidechain/amix grafiği kilitlenip sonsuza dek bekliyor; ffmpeg'e her zaman -nostdin ver, uzun işlere timeout koy.
