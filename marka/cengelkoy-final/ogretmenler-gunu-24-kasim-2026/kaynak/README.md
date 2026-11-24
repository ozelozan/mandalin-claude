# Öğretmenler Günü hikayeleri — Çengelköy Final Okulları (24 Kasım 2026)

6 adet 1080×1920 Instagram hikayesi (HTML). Tarayıcıda açınca pencereye sığacak şekilde küçülür.

| Dosya | Fotoğraf | Metin |
|---|---|---|
| hikaye-1.html | f1 — çiçekli öğrenciler (tam ekran) | Yıldızımsın Öğretmenim |
| hikaye-2.html | f6 — 8 öğretmen (tam ekran) | Emeğiniz geleceğimizin ışığı |
| hikaye-3.html | f5 + f3 — öğretmen grupları | İyi ki varsınız |
| hikaye-4.html | f7 + f9 — çiçekli öğretmenler | Her çiçek bir teşekkür |
| hikaye-5.html | f4 + f8 — sınıflar | Minik yıldızlarımızdan öğretmenlerine sevgiyle |
| hikaye-6.html | f10 + f11 — sınıflar | Yolumuzu aydınlatan tüm öğretmenlerimize |

f2 (f1'in neredeyse aynısı) kullanılmadı.

- Logo: `gorseller/logo-beyaz-yazi.png` (koyu zeminde beyaz yazılı resmi logo, plaka yok).
- Yazı ölçüleri (1080 px'te): etiket 26 · başlık 56-76 · alt metin 28-34. Montserrat.
- Fotoğraf kareleri `object-position` ile ayarlı; kişiler kırpılmaz. Fotoğraf değişirse bu değer yeniden kontrol edilmeli.
- Fotoğrafları yeniden hazırlamak (EXIF yönü düzeltilir): `~/tools/venv-img/bin/python3 kaynak/gorsel-hazirla.py "<kaynak-klasör>" gorseller`
- PNG almak: `bash kaynak/png-al.sh <çıktı-klasörü>` (Chromium ~/tools altında).
