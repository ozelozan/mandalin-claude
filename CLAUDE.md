# Çalışma kuralları

- Bu depo (`mandalin-claude`) kullanıcının ana çalışma klasörüdür. Tüm işler burada yapılır ve saklanır.
- Her iş kendi klasöründe tutulur (ör. `omer-asaf/`). Depo köküne dağınık dosya bırakılmaz.
- Teslim edilen dosyalar, onları üreten betikler ve kullanılan girdiler (görsel, video vb.) aynı iş klasöründe durur; üretim betikleri `<iş-klasörü>/kaynak/` altına konur.
- Geçici (scratchpad / /tmp) klasörler yalnızca ara işlem içindir; kalıcı her şey bu depoya kopyalanır, commit edilir ve push edilir.
- **Her iş bitince değişiklikler `main` dalına birleştirilir ve push edilir.** Kullanıcı bunu 23 Kasım 2026'da açıkça onayladı. Oturum yan dalda (`claude/...`) çalışsa bile iş sonunda `main`'e merge edilir; kullanıcının Mac'i (`~/Mini_MAN/mandalin-claude`) yalnızca `main`'i çeker, yan dalda kalan iş görünmez.
- `node_modules/`, dönüştürme sırasında oluşan PDF/JPG önizlemeleri gibi yeniden üretilebilir dosyalar commit edilmez.

## İşler

- `gunluk-ozet/` — günlük takvim özetleri.
- `omer-asaf/` — RKR207 Eğitsel Oyunlar ödevi (PowerPoint sunumu, Word belgesi, ana oyun videosu).
