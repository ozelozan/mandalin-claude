# Vision dekupesinden soldaki diğer öğrenciyi, diğer okul bayrağını ve pano yazısı parçasını siler.
from PIL import Image
im = Image.open("ham-dekupe.png").convert("RGBA")
px = im.load(); W, H = im.size
CERT = (190, 634, 340, 748)          # başarı belgesi (korunur)
for y in range(H):
    for x in range(W):
        r, g, b, a = px[x, y]
        if a == 0: continue
        if x < 204 and not (CERT[0] <= x < CERT[2] and CERT[1] <= y < CERT[3] and x >= 198):
            px[x, y] = (0, 0, 0, 0); continue
        # Bayrak üst kenarının üstündeki pano yazısı (kırmızı harfler ve pembe kenarları)
        if 120 <= x < 470 and 560 <= y < 690:
            in_cert = CERT[0] <= x < CERT[2] and CERT[1] <= y < CERT[3]
            arm = x >= 378 and y >= 650
            if not in_cert and not arm and (r - g > 45 and r > 120):
                px[x, y] = (0, 0, 0, 0)
im.save("bora-dekupe.png")
print(im.getbbox())

# İkinci geçiş: belge üstü ve belge-tişört arası kalan harf kırıntıları
im = Image.open("bora-dekupe.png"); px = im.load()
for y in range(560, 692):
    for x in range(198, 472):
        r, g, b, a = px[x, y]
        if a == 0: continue
        in_cert = CERT[0] <= x < CERT[2] and CERT[1] <= y < CERT[3]
        if in_cert: continue
        if x >= 392 and y >= 659: continue                     # kol
        if x >= 395 and max(r, g, b) < 75: continue            # siyah tişört
        if y >= 676: continue                                  # bayrak üst kenarı
        px[x, y] = (0, 0, 0, 0)
im.save("bora-dekupe.png")
