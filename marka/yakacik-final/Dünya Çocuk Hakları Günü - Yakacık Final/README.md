# Dünya Çocuk Hakları Günü - Yakacık Final (Instagram hikâye videosu)

- **Teslim:** `cikti/Dünya Çocuk Hakları Günü - Yakacık Final.mp4` (1080x1920, 30 fps, 42 sn, -14 LUFS). Açıklama: `instagram-aciklama.txt`.
- **Konsept:** "Hak ağacı". Boş ağaç → çocukların çizimleriyle dolan ağaç → her fotoğraf bir "hak" notu taşır → 16 fotoğraf ağacın beyaz tahtasını doldurur → "Her çocuk eşit. Her çocuk değerli. Her çocuğun hakları saklı."
- **Girdiler:** bu klasördeki 16 fotoğraf + 2 video (WhatsApp). Hepsi kullanıldı (16 fotoğrafın tamamı, 2 videonun ikisi).
- **Kaynak:** `kaynak/hikaye.py` (kare kare PIL render; `python3 hikaye.py render <çıktı.mp4>`), `kaynak/ses.py` (efekt sesleri, kareye kilitli). Müzik: `muzik/fon-muzigi.mp3` (ElevenLabs Music v2, sözsüz, 120 BPM).
- **Karışım:** `ffmpeg` ile müzik + efekt, `loudnorm -14 LUFS`. Alt lacivert bant + logo her karede (Instagram alt arayüz payı).
- **Hak notları** (BM Çocuk Hakları Sözleşmesi başlıkları): oynama, sağlık, bir adı olma, korunma, eğitim, fikrini söyleme, eşit olma, yaşama, dinlenme, düşünme, katılma, beslenme, ailesiyle yaşama. Hangi fotoğrafa hangi not düştüğü `hikaye.py` içindeki `SAHNELER` listesinde; değiştirmesi tek satır.
