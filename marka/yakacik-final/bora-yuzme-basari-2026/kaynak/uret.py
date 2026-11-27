# Bora Mehmet Çelikdemir yüzme başarısı — Instagram post (1080x1350, 4:5)
# A: referans mantığı (mavi zemin + dekupe öğrenci + altın plaka)
# B: gerçek fotoğraf + alttan beyaz geçiş + başlık + logo alt ortada
# Öğrencinin yüzü ve bayraktaki logo orijinal fotoğraf pikselleridir; yeniden üretim yok.
import subprocess, pathlib

K = pathlib.Path(__file__).resolve().parent
OUT = K.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

FONTS = '<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,100..125,400..900;1,100..125,400..900&family=Public+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">'

BASE = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px;overflow:hidden}
body{position:relative;font-family:'Public Sans',sans-serif;-webkit-font-smoothing:antialiased}
.d{font-family:'Archivo',sans-serif;font-style:italic;font-weight:900;font-stretch:108%;text-transform:uppercase;line-height:.95;letter-spacing:-.01em}
.abs{position:absolute}
"""

SONUCLAR = [("2", "gumus", "50 M SERBEST", "İstanbul 2.si"),
            ("2", "gumus", "100 M SERBEST", "İstanbul 2.si"),
            ("4", "lacivert", "50 M SIRTÜSTÜ", "İstanbul 4.sü")]


def kartlar(tema):
    h = []
    for n, tip, brans, derece in SONUCLAR:
        h.append(f'<div class="kart {tema}"><div class="rozet {tip}">{n}</div>'
                 f'<div><div class="brans">{brans}</div><div class="derece">{derece}</div></div></div>')
    return "".join(h)


# ---------------- A: referans mantığı ----------------
A = f"""<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{BASE}
body{{background:radial-gradient(ellipse 900px 760px at 50% 34%,#3157C9 0%,#1D3393 42%,#101A5C 78%,#0B1245 100%)}}
.isin{{inset:0;background:repeating-linear-gradient(115deg,rgba(255,255,255,.035) 0 2px,transparent 2px 70px)}}
.dalga{{left:0;right:0;bottom:0;height:520px}}
.ust{{top:58px;left:0;right:0;text-align:center;color:#fff}}
.ust .k{{font-weight:700;letter-spacing:.16em;font-size:27px}}
.ust .k:before,.ust .k:after{{content:"";display:inline-block;width:46px;height:3px;background:#E0403A;vertical-align:middle;margin:0 18px 5px}}
.ust .b1{{font-size:66px;margin-top:18px;color:#fff;text-shadow:0 6px 24px rgba(0,0,0,.35)}}
.ust .b2{{font-size:104px;margin-top:4px;color:#F2C14E;text-shadow:0 6px 24px rgba(0,0,0,.35)}}
.ogr{{left:68px;top:-56px;width:923px}}
.golge{{left:0;right:0;top:905px;bottom:0;background:linear-gradient(180deg,rgba(11,18,69,0) 0,rgba(11,18,69,.92) 60px,#0B1245 110px)}}
.plaka{{left:50%;transform:translateX(-50%);top:922px;width:800px;padding:18px 0 16px;text-align:center;
  background:linear-gradient(180deg,#FBE3A0 0%,#E9B94A 45%,#C8902A 100%);border-radius:10px;
  box-shadow:0 14px 34px rgba(0,0,0,.45),inset 0 2px 0 rgba(255,255,255,.6)}}
.plaka .ad{{font-size:52px;color:#131C51;font-stretch:100%}}
.plaka .alt{{font-size:23px;font-weight:700;color:#131C51;margin-top:8px;letter-spacing:.02em}}
.etk{{top:1052px;left:0;right:0;text-align:center;color:#fff;font-size:24px;font-weight:600;letter-spacing:.02em}}
.etk b{{color:#F2C14E;font-weight:800}}
.kartlar{{top:1098px;left:60px;right:60px;display:flex;gap:16px}}
.kart{{flex:1;display:flex;align-items:center;gap:14px;padding:13px 16px;border-radius:12px}}
.kart.koyu{{background:rgba(255,255,255,.07);border:1.5px solid rgba(242,193,78,.75)}}
.kart.koyu .brans{{color:#fff}} .kart.koyu .derece{{color:#F2C14E}}
.rozet{{flex:none;width:52px;height:52px;border-radius:50%;display:flex;align-items:center;justify-content:center;
  font-family:'Archivo';font-weight:900;font-style:italic;font-size:30px}}
.rozet.gumus{{background:radial-gradient(circle at 35% 30%,#fff,#C9CED6 45%,#8D95A3);color:#131C51;box-shadow:0 0 0 3px rgba(255,255,255,.25)}}
.rozet.lacivert{{background:#131C51;color:#fff;box-shadow:0 0 0 3px #F2C14E}}
.brans{{font-family:'Archivo';font-weight:800;font-size:21px;letter-spacing:.01em;white-space:nowrap}}
.derece{{font-weight:800;font-size:22px;margin-top:2px}}
.logo{{left:50%;transform:translateX(-50%);top:1212px;display:flex;flex-direction:column;align-items:center;gap:8px}}
.logo .i{{height:64px}} .logo .y{{height:36px;filter:brightness(0) invert(1)}}
</style></head><body>
<div class="abs isin"></div>
<svg class="abs dalga" viewBox="0 0 1080 520" preserveAspectRatio="none">
 <g fill="none" stroke="rgba(255,255,255,.08)" stroke-width="3">
  <path d="M0 120 C180 80 360 160 540 120 S900 80 1080 120"/>
  <path d="M0 170 C180 130 360 210 540 170 S900 130 1080 170"/>
  <path d="M0 220 C180 180 360 260 540 220 S900 180 1080 220"/>
 </g></svg>
<div class="abs ust"><div class="k">YAKACIK FİNAL OKULLARI'NDAN</div>
<div class="d b1">YÜZMEDE İSTANBUL'DA</div><div class="d b2">ÇİFTE İKİNCİLİK!</div></div>
<img class="abs ogr" src="bora-dekupe.png">
<div class="abs golge"></div>
<div class="abs plaka"><div class="d ad">BORA MEHMET ÇELİKDEMİR</div>
<div class="alt">Özel Yakacık Final Anadolu Lisesi Öğrencimiz</div></div>
<div class="abs etk">24–26 Kasım 2026 · <b>Okul Sporları Gençler Yüzme İl Birinciliği</b></div>
<div class="abs kartlar">{kartlar("koyu")}</div>
<div class="abs logo"><img class="i" src="logo-isaret.png"><img class="y" src="logo-yazi.png"></div>
</body></html>"""

# ---------------- B: gerçek fotoğraf + beyaz geçiş ----------------
B = f"""<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{BASE}
body{{background:#fff}}
.foto{{left:-3px;top:-230px;width:1086px}}
.sol{{left:0;top:0;bottom:0;width:300px;background:linear-gradient(90deg,#fff 0,#fff 120px,rgba(255,255,255,.85) 175px,rgba(255,255,255,0) 215px)}}
.beyaz{{left:0;right:0;top:868px;bottom:0;background:linear-gradient(180deg,rgba(255,255,255,0) 0,rgba(255,255,255,.8) 70px,#fff 110px)}}
.cerceve{{inset:22px;border:2px solid #131C51;pointer-events:none}}
.cerceve2{{inset:30px;border:1.5px solid #CB3530;pointer-events:none}}
.etiket{{top:64px;left:64px;background:#CB3530;color:#fff;font-family:'Archivo';font-weight:800;font-style:italic;font-size:26px;padding:10px 20px 9px;letter-spacing:.03em}}
.tarih{{top:116px;left:64px;background:#131C51;color:#fff;font-weight:700;font-size:21px;padding:8px 20px;letter-spacing:.04em}}
.metin{{top:948px;left:0;right:0;text-align:center}}
.kicker{{font-weight:800;font-size:22px;letter-spacing:.14em;color:#CB3530}}
.ad{{font-size:55px;color:#131C51;margin-top:12px;white-space:nowrap}}
.okul{{font-size:23px;font-weight:600;color:#3A4370;margin-top:8px}}
.kartlar{{top:1112px;left:70px;right:70px;display:flex;gap:14px}}
.kart{{flex:1;display:flex;align-items:center;gap:12px;padding:11px 14px;border-radius:10px}}
.kart.acik{{background:#F3F5FB;border:1.5px solid #D9DEEE}}
.kart.acik .brans{{color:#131C51}} .kart.acik .derece{{color:#CB3530}}
.rozet{{flex:none;width:48px;height:48px;border-radius:50%;display:flex;align-items:center;justify-content:center;
  font-family:'Archivo';font-weight:900;font-style:italic;font-size:28px}}
.rozet.gumus{{background:radial-gradient(circle at 35% 30%,#fff,#C9CED6 45%,#8D95A3);color:#131C51;box-shadow:0 0 0 2px #B9BFCB}}
.rozet.lacivert{{background:#131C51;color:#fff}}
.brans{{font-family:'Archivo';font-weight:800;font-size:19px;white-space:nowrap}}
.derece{{font-weight:800;font-size:21px;margin-top:2px}}
.logo{{left:50%;transform:translateX(-50%);top:1196px;height:118px}}
</style></head><body>
<img class="abs foto" src="bora-orijinal.jpg">
<div class="abs sol"></div>
<div class="abs beyaz"></div>
<div class="abs etiket">TEBRİKLER BORA!</div>
<div class="abs tarih">24–26 KASIM 2026</div>
<div class="abs metin"><div class="kicker">İSTANBUL OKUL SPORLARI · GENÇLER YÜZME</div>
<div class="d ad">BORA MEHMET ÇELİKDEMİR</div>
<div class="okul">Özel Yakacık Final Anadolu Lisesi · İki İstanbul İkinciliği</div></div>
<div class="abs kartlar">{kartlar("acik")}</div>
<img class="abs logo" src="logo-tam.png">
<div class="abs cerceve"></div><div class="abs cerceve2"></div>
</body></html>"""

# ---------------- C: lacivert zemin + beyaz çerçeveli orijinal fotoğraf (dekupesiz) ----------------
from PIL import Image as _I
_I.open(K / "bora-orijinal.jpg").crop((205, 360, 965, 1190)).save(K / "bora-kirp.jpg", quality=95)
C = f"""<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{BASE}
body{{background:radial-gradient(ellipse 820px 700px at 50% 40%,#22398F 0%,#16236B 50%,#0D1449 100%)}}
.isin{{inset:0;background:repeating-linear-gradient(115deg,rgba(255,255,255,.03) 0 2px,transparent 2px 70px)}}
.ust{{top:62px;left:70px;right:70px;text-align:center;color:#fff}}
.ust .k{{font-weight:700;letter-spacing:.16em;font-size:24px}}
.ust .k:before,.ust .k:after{{content:"";display:inline-block;width:40px;height:3px;background:#E0403A;vertical-align:middle;margin:0 16px 5px}}
.ust .b{{font-size:88px;margin-top:16px;white-space:nowrap;color:#F2C14E;text-shadow:0 6px 24px rgba(0,0,0,.35)}}
.ust .s{{font-family:'Archivo';font-weight:800;font-style:italic;font-size:32px;margin-top:12px;letter-spacing:.01em}}
.cerceve{{left:50%;transform:translateX(-50%);top:292px;background:#fff;padding:14px;box-shadow:0 22px 50px rgba(0,0,0,.45)}}
.cerceve img{{display:block;width:560px;height:612px;object-fit:cover}}
.plaka{{left:50%;transform:translateX(-50%);top:888px;padding:16px 44px 15px;text-align:center;white-space:nowrap;
  background:linear-gradient(180deg,#FBE3A0 0%,#E9B94A 45%,#C8902A 100%);border-radius:10px;
  box-shadow:0 14px 34px rgba(0,0,0,.45),inset 0 2px 0 rgba(255,255,255,.6)}}
.plaka .ad{{font-size:40px;color:#131C51;font-stretch:100%}}
.plaka .alt{{font-size:20px;font-weight:700;color:#131C51;margin-top:7px}}
.etk{{top:1024px;left:70px;right:70px;text-align:center;color:#fff;font-size:22px;font-weight:600}}
.etk b{{color:#F2C14E;font-weight:800}}
.kartlar{{top:1070px;left:70px;right:70px;display:flex;gap:14px}}
.kart{{flex:1;display:flex;align-items:center;gap:12px;padding:12px 14px;border-radius:12px}}
.kart.koyu{{background:rgba(255,255,255,.07);border:1.5px solid rgba(242,193,78,.75)}}
.kart.koyu .brans{{color:#fff}} .kart.koyu .derece{{color:#F2C14E}}
.rozet{{flex:none;width:48px;height:48px;border-radius:50%;display:flex;align-items:center;justify-content:center;
  font-family:'Archivo';font-weight:900;font-style:italic;font-size:28px}}
.rozet.gumus{{background:radial-gradient(circle at 35% 30%,#fff,#C9CED6 45%,#8D95A3);color:#131C51;box-shadow:0 0 0 3px rgba(255,255,255,.25)}}
.rozet.lacivert{{background:#131C51;color:#fff;box-shadow:0 0 0 3px #F2C14E}}
.brans{{font-family:'Archivo';font-weight:800;font-size:19px;white-space:nowrap}}
.derece{{font-weight:800;font-size:21px;margin-top:2px}}
.logo{{left:50%;transform:translateX(-50%);top:1184px;display:flex;flex-direction:column;align-items:center;gap:7px}}
.logo .i{{height:60px}} .logo .y{{height:34px;filter:brightness(0) invert(1)}}
</style></head><body>
<div class="abs isin"></div>
<div class="abs ust"><div class="k">YAKACIK FİNAL OKULLARI'NDAN</div>
<div class="d b">TEBRİKLER BORA!</div>
<div class="s">Yüzmede İstanbul'da BÜYÜK BAŞARI</div></div>
<div class="abs cerceve"><img src="bora-kirp.jpg"></div>
<div class="abs plaka"><div class="d ad">BORA MEHMET ÇELİKDEMİR</div>
<div class="alt">Özel Yakacık Final Anadolu Lisesi Öğrencimiz</div></div>
<div class="abs etk">24–26 Kasım 2026 · <b>Okul Sporları Gençler Yüzme İl Birinciliği</b></div>
<div class="abs kartlar">{kartlar("koyu")}</div>
<div class="abs logo"><img class="i" src="logo-isaret.png"><img class="y" src="logo-yazi.png"></div>
</body></html>"""

for ad, html in [("A-referans", A), ("B-beyaz-gecis", B), ("C-lacivert-cerceve", C)]:
    src = K / f"{ad}.html"
    src.write_text(html, encoding="utf-8")
    png = OUT / f"bora-yuzme-{ad}.png"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--window-size=1080,1350", "--virtual-time-budget=8000", f"--screenshot={png}", f"file://{src}"],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(png)
