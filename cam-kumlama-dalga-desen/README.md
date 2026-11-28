# Cam kumlama dalga deseni

- `cam-kumlama-dalga-120cm-rapor.svg / .pdf` — üretim dosyası. Yükseklik 120 cm, tek rapor (tekrar birimi) genişliği 240 cm, ölçek 1:1.
- `onizleme-3-rapor-yan-yana.*` — üç rapor yan yana; birleşim yerlerinin görünmediğini gösterir.
- Yatayda kesintisiz: tüm eğriler rapor genişliğinin tam katı frekanslarla kuruldu, sağ ve sol uçta konum ve eğim aynı. Raporu sağa sola kopyalayıp yan yana koymak yeterli (ek bindirme gerekmez).
- Katmanlar (PDF'te katman, SVG'de grup): ZEMIN_BEYAZ, ZEMIN_GRI (altın çizginin altı), CIZGI_GRI (beyaz bölgedeki çizgiler), CIZGI_BEYAZ (gri bölgedeki çizgiler), CIZGI_GOLD (ortadaki 60 cm ekseni, 6 mm).
- İnce çizgiler 1.0–1.2 mm. Ölçüleri değiştirmek için `kaynak/uret.py` başındaki W, H, N değerleri.
