#!/usr/bin/env python3
"""Cam kumlama dalga deseni — yatayda kesintisiz tekrar eden vektör (SVG + PDF).

Ölçüler mm. Desen yüksekliği 1200 mm (120 cm), tekrar (rapor) genişliği W.
Tüm eğriler yalnızca 2π/W'nin tam katı frekanslarla kurulur; bu yüzden x=0 ve x=W
uçlarında konum ve eğim birebir aynıdır: paneller yan yana dizildiğinde çizgiler
birbirini kusursuz tamamlar.

Katmanlar:
  ZEMIN_GRI    : altın çizginin altı, gri (kumlama) dolgu
  ZEMIN_BEYAZ  : altın çizginin üstü, beyaz dolgu
  CIZGI_BEYAZ  : gri bölgede kalan ince dalga çizgileri (beyaz)
  CIZGI_GRI    : beyaz bölgede kalan ince dalga çizgileri (gri)
  CIZGI_GOLD   : ortadaki (60 cm) altın çizgi
"""
import math, os, sys

W = 2400.0        # rapor genişliği (mm) – 240 cm
H = 1200.0        # yükseklik (mm) – 120 cm
MID = H / 2       # altın çizginin ekseni: tam ortada, 60 cm
N = 34            # ince çizgi sayısı (her şerit)
STEP = 40.0       # Bezier parça uzunluğu (mm)

GRI = (0.62, 0.63, 0.65)
BEYAZ = (1, 1, 1)
CIZGI_GRI = (0.55, 0.56, 0.58)
GOLD = (0.80, 0.64, 0.30)
K = 2 * math.pi / W


def gold(x):
    """Ortadaki altın çizgi: 60 cm ekseni etrafında yumuşak tek dalga."""
    return MID + 55 * math.sin(K * x + 0.4) + 14 * math.sin(2 * K * x + 1.9)


def gold_d(x):
    return 55 * K * math.cos(K * x + 0.4) + 28 * K * math.cos(2 * K * x + 1.9)


def ribbon(t, side):
    """t in [0,1]. side=0 / 1: iki ayrı kurdele. Çizgiler altın çizgi etrafında
    burularak döner (kurdele kıvrımı); altın çizgi demetin tam ortasından geçer."""
    u = 2 * t - 1
    if side == 0:
        R, f1, p1, A, p2, sh = 300, 2, 0.3, 70, 1.1, 0.0
    else:
        R, f1, p1, A, p2, sh = 210, 1, 2.3, 45, 4.0, 25.0

    def f(x):
        return gold(x) + u * R * math.cos(f1 * K * x + p1) + u * u * A * math.sin(K * x + p2) \
            + sh * math.sin(3 * K * x + p1) + 18 * u * math.sin(3 * K * x + p2)

    def d(x):
        return gold_d(x) - u * R * f1 * K * math.sin(f1 * K * x + p1) \
            + u * u * A * K * math.cos(K * x + p2) \
            + sh * 3 * K * math.cos(3 * K * x + p1) + 18 * u * 3 * K * math.cos(3 * K * x + p2)
    return f, d


def bez(f, d, x0=0.0, x1=W):
    """Hermite → kübik Bezier. [(p0, c1, c2, p3), ...] (y aşağı: SVG koordinatı)."""
    segs = []
    n = int(round((x1 - x0) / STEP))
    for i in range(n):
        a = x0 + i * STEP
        b = a + STEP
        ya, yb = f(a), f(b)
        h = STEP / 3
        segs.append(((a, ya), (a + h, ya + d(a) * h), (b - h, yb - d(b) * h), (b, yb)))
    return segs


# --------------------------------------------------------------- geometri
def build(reps=1):
    """Desen nesnelerini (y aşağı, SVG koordinatı) üretir. reps: önizleme için tekrar."""
    span = W * reps
    gf = lambda x: H - gold(x)          # matematikte y yukarı; çevir
    gd = lambda x: -gold_d(x)
    gold_segs = bez(gf, gd, 0, span)

    layers = {}
    # gri zemin: altın çizginin altı
    layers['ZEMIN_GRI'] = [('fill', GRI, gold_segs, 'alt', None)]
    layers['ZEMIN_BEYAZ'] = [('fill', BEYAZ, gold_segs, 'ust', None)]
    lines = []
    for side in (0, 1):
        for i in range(N):
            t = i / (N - 1)
            f, d = ribbon(t, side)
            segs = bez(lambda x, f=f: H - f(x), lambda x, d=d: -d(x), 0, span)
            w = 1.2 if side == 0 else 1.0       # mm, kumlama için güvenli inceliğin üstü
            lines.append((segs, w))
    # aynı çizgi: beyaz zeminde gri, gri zeminde beyaz görünür (bölge kırpması)
    layers['CIZGI_GRI'] = [('stroke', CIZGI_GRI, sg, w, 'ust') for sg, w in lines]
    layers['CIZGI_BEYAZ'] = [('stroke', BEYAZ, sg, w, 'alt') for sg, w in lines]
    layers['CIZGI_GOLD'] = [('stroke', GOLD, gold_segs, 6.0, None)]
    layers['_gold'] = gold_segs
    return span, layers


def fill_path(segs, which, span):
    # alt: eğri → sağ alt → sol alt ; üst: eğri → sağ üst → sol üst
    yend = H if which == 'alt' else 0.0
    return segs, [(span, yend), (0.0, yend)]


# --------------------------------------------------------------- SVG
def svg_d(segs, close_pts=None):
    p0 = segs[0][0]
    out = [f"M{p0[0]:.2f},{p0[1]:.2f}"]
    for _, c1, c2, p3 in segs:
        out.append(f"C{c1[0]:.2f},{c1[1]:.2f} {c2[0]:.2f},{c2[1]:.2f} {p3[0]:.2f},{p3[1]:.2f}")
    if close_pts:
        for x, y in close_pts:
            out.append(f"L{x:.2f},{y:.2f}")
        out.append("Z")
    return " ".join(out)


def rgb(c):
    return "#%02x%02x%02x" % tuple(round(v * 255) for v in c)


def write_svg(path, reps=1, clip_lines=True):
    span, layers = build(reps)
    o = [f'<?xml version="1.0" encoding="UTF-8"?>',
         f'<svg xmlns="http://www.w3.org/2000/svg" width="{span/10:g}cm" height="{H/10:g}cm" '
         f'viewBox="0 0 {span:g} {H:g}">',
         f'<!-- Cam kumlama dalga deseni | rapor {W/10:g} x {H/10:g} cm | yatay kesintisiz tekrar -->',
         f'<defs><clipPath id="kadraj"><rect width="{span:g}" height="{H:g}"/></clipPath>'
         f'<clipPath id="ust"><path d="{svg_d(*fill_path(layers["_gold"], "ust", span))}"/></clipPath>'
         f'<clipPath id="alt"><path d="{svg_d(*fill_path(layers["_gold"], "alt", span))}"/></clipPath></defs>',
         '<g clip-path="url(#kadraj)">']
    for name in ['ZEMIN_BEYAZ', 'ZEMIN_GRI', 'CIZGI_GRI', 'CIZGI_BEYAZ', 'CIZGI_GOLD']:
        zone = layers[name][0][4]
        o.append(f'<g id="{name}"' + (f' clip-path="url(#{zone})">' if zone else '>'))
        for kind, col, segs, extra, _z in layers[name]:
            if kind == 'fill':
                s, cl = fill_path(segs, extra, span)
                o.append(f'<path d="{svg_d(s, cl)}" fill="{rgb(col)}"/>')
            else:
                o.append(f'<path d="{svg_d(segs)}" fill="none" stroke="{rgb(col)}" '
                         f'stroke-width="{extra:.2f}" stroke-linecap="butt"/>')
        o.append('</g>')
    o.append('</g></svg>')
    open(path, 'w').write("\n".join(o))


# --------------------------------------------------------------- PDF (elle, bağımlılıksız)
def write_pdf(path, reps=1):
    span, layers = build(reps)
    pt = 72 / 25.4
    def P(x, y):  # mm (y aşağı) → pt (y yukarı)
        return f"{x*pt:.3f} {(H-y)*pt:.3f}"
    c = [f"0 0 {span*pt:.3f} {H*pt:.3f} re W n"]
    for name in ['ZEMIN_BEYAZ', 'ZEMIN_GRI', 'CIZGI_GRI', 'CIZGI_BEYAZ', 'CIZGI_GOLD']:
        c.append(f"/OC /{name} BDC")
        zone = layers[name][0][4]
        if zone:
            g = layers['_gold']; _, cl = fill_path(g, zone, span)
            c.append("q " + " ".join([f"{P(*g[0][0])} m"] + [f"{P(*a)} {P(*b)} {P(*e)} c" for _, a, b, e in g]
                                     + [f"{P(*q)} l" for q in cl]) + " h W n")
        for kind, col, segs, extra, _z in layers[name]:
            seq = [f"{P(*segs[0][0])} m"] + [f"{P(*c1)} {P(*c2)} {P(*p3)} c" for _, c1, c2, p3 in segs]
            if kind == 'fill':
                _, cl = fill_path(segs, extra, span)
                seq += [f"{P(*q)} l" for q in cl] + ["h"]
                c.append(f"{col[0]:.3f} {col[1]:.3f} {col[2]:.3f} rg\n" + "\n".join(seq) + "\nf")
            else:
                c.append(f"{col[0]:.3f} {col[1]:.3f} {col[2]:.3f} RG {extra*pt:.3f} w\n" + "\n".join(seq) + "\nS")
        if zone:
            c.append("Q")
        c.append("EMC")
    stream = "\n".join(c).encode()
    names = ['ZEMIN_BEYAZ', 'ZEMIN_GRI', 'CIZGI_GRI', 'CIZGI_BEYAZ', 'CIZGI_GOLD']
    objs = []
    ocg_start = 5
    ocg_refs = " ".join(f"{ocg_start+i} 0 R" for i in range(len(names)))
    objs.append(f"<< /Type /Catalog /Pages 2 0 R /OCProperties << /OCGs [{ocg_refs}] /D << /Order [{ocg_refs}] >> >> >>")
    objs.append("<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
    props = " ".join(f"/{n} {ocg_start+i} 0 R" for i, n in enumerate(names))
    objs.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {span*pt:.3f} {H*pt:.3f}] "
                f"/Resources << /Properties << {props} >> >> /Contents 4 0 R >>")
    objs.append(None)  # stream
    for n in names:
        objs.append(f"<< /Type /OCG /Name ({n}) >>")
    out = bytearray(b"%PDF-1.5\n%\xe2\xe3\xcf\xd3\n")
    offs = []
    for i, ob in enumerate(objs, 1):
        offs.append(len(out))
        if ob is None:
            out += f"{i} 0 obj\n<< /Length {len(stream)} >>\nstream\n".encode() + stream + b"\nendstream\nendobj\n"
        else:
            out += f"{i} 0 obj\n{ob}\nendobj\n".encode()
    xref = len(out)
    out += f"xref\n0 {len(objs)+1}\n0000000000 65535 f \n".encode()
    for o_ in offs:
        out += f"{o_:010d} 00000 n \n".encode()
    out += f"trailer\n<< /Size {len(objs)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    open(path, 'wb').write(out)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..")
    write_svg(os.path.join(out, "cam-kumlama-dalga-120cm-rapor.svg"))
    write_pdf(os.path.join(out, "cam-kumlama-dalga-120cm-rapor.pdf"))
    write_svg(os.path.join(out, "onizleme-3-rapor-yan-yana.svg"), reps=3)
    write_pdf(os.path.join(out, "onizleme-3-rapor-yan-yana.pdf"), reps=3)
    # süreklilik testi: uçlarda değer ve eğim eşit mi
    errs = []
    for t in (0, .3, .7, 1):
        for s in (1, -1):
            f, d = ribbon(t, s)
            errs += [abs(f(0) - f(W)), abs(d(0) - d(W))]
    errs += [abs(gold(0) - gold(W)), abs(gold_d(0) - gold_d(W))]
    print("max uç farkı:", max(errs))
