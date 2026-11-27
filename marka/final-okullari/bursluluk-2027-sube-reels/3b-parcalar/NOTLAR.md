# Final'in Bursluluk Sınavı 2027: ayrı 3B parçalar

Video ve branda için afişin her öğesi ayrı, şeffaf zeminli PNG olarak `parcalar/` klasöründe.

| Dosya | Kaynak | Boyut (px) |
|---|---|---|
| sube-cengelkoy.png | ChatGPT | 1907x470 |
| sube-beykoz.png | ChatGPT | 1781x586 |
| yazi-finalin.png | ChatGPT | 1875x555 |
| yazi-bursluluk.png | ChatGPT (öğrencisiz, K tam) | 1973x494 |
| yazi-sinavi.png | ChatGPT | 1755x637 |
| ogrenci.png | ChatGPT (kitap okuyan, oturan) | 785x1493 |
| tarih-9-10-ocak.png | Açık PSD katmanı | 2633x769 |
| online-kayit-bandi.png | Açık PSD katmanı, lacivert yama temizlendi | 2880x802 |
| cizgiler-cengelkoy.png / cizgiler-beykoz.png | PSD birleşik görüntüsünden sarı ayrıştırma; afişle birebir hizalı tam tuval | 7162x9941 |
| zemin.png | PSD'den, içerik silinip yumuşak dolgu; hafif koyu üst gölgesi korundu | 7162x9941 |

- `chatgpt/` ham indirmeler (2172x724 yatay, öğrenci 1024x1536). ChatGPT sohbeti: "3B Yazı Üretimi".
- `montaj-kontrol-*.jpg`: parçaların afiş düzeninde üst üste dizilmiş hali (yalnız kontrol amaçlı).
- Çizgiler afiş tuvali boyutunda: zemin.png'nin üstüne 0,0 konumuna konunca afişteki yerine oturur. Öğrencinin arkasında kalan çizgi parçası orijinalde de görünmediği için yok.
- Betikler `kaynak/`: `cizgi_zemin.py` (çizgi + zemin), `psd_katman_cikar.py` (PSD katmanlarını PNG'ye), `lacivert_temizle.py`, `kur_ust_uste.py` (kırpma + montaj).
- PSD'deki eski çengelköy katmanında lacivert hale vardı, bu yüzden şube adları ChatGPT'den yeniden üretildi.
- Branda için çözünürlük düşük: büyük baskıdan önce parçalar büyütülmeli (Magnific upscale, 4x).
