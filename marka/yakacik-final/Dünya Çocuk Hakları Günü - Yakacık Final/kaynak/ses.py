# Ses efektleri: kare numaralarına kilitli (hikaye.py olaylar). Kullanım: python3 ses.py <sfx.wav>
import sys, json, subprocess, numpy as np, wave, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hikaye as h
SR = 44100
o = h.olaylar()
N = int(h.N / h.FPS * SR) + SR
buf = np.zeros(N, np.float32)
rng = np.random.RandomState(5)
def ekle(f, ses, g):
    i = int(f / h.FPS * SR)
    buf[i:i + len(ses)] += ses[:N - i] * g
def lp(x, a):
    y = np.zeros_like(x); s = 0.0
    al = np.broadcast_to(a, x.shape)
    for k, v in enumerate(x):
        s += al[k] * (v - s); y[k] = s
    return y
def vurus():      # yapışkan not / damga: alçak tok darbe + kâğıt çıtırtısı
    t = np.arange(int(.16 * SR)) / SR
    f0 = 150 * np.exp(-t * 14) + 55
    k = np.sin(2 * np.pi * np.cumsum(f0) / SR) * np.exp(-t * 22)
    n = lp(rng.randn(len(t)).astype(np.float32), .35) * np.exp(-t * 60) * .8
    return (k + n).astype(np.float32)
def havlu():      # kart girişi: kısa, yumuşak kâğıt süpürmesi
    t = np.arange(int(.26 * SR)) / SR
    n = rng.randn(len(t)).astype(np.float32)
    n = lp(n, .06 + .25 * np.sin(np.pi * t / .26) ** 2)
    return (n * np.sin(np.pi * t / .26) ** 1.5 * 1.4).astype(np.float32)
def pop(fr):
    t = np.arange(int(.09 * SR)) / SR
    return (np.sin(2 * np.pi * fr * t) * np.exp(-t * 45)).astype(np.float32)
def kalem():      # çizgi/yazı açılırken ince sürtünme
    t = np.arange(int(.3 * SR)) / SR
    n = rng.randn(len(t)).astype(np.float32)
    n = n - lp(n, .5)
    return (n * np.sin(np.pi * t / .3) * .25).astype(np.float32)
for f in o['damga']: ekle(f, vurus(), .9)
for f in o['not']: ekle(f, vurus(), .75)
for f in o['giris']: ekle(f, havlu(), .55)
for j, f in enumerate(o['final_kart']): ekle(f + 2, pop(520 + 40 * (j % 4)), .22)
for f in o['final_satir']: ekle(f, kalem(), .9)
buf = np.clip(buf, -1, 1)
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((buf * 32000).astype(np.int16).tobytes())
