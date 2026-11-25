# Fotoğraf albümü kopya sürüm (v5 + 6 masa fotoğrafı daha), 25 Kasım 2026.
# album.py aynen kullanılır; masa2'den sonra "masa3" sahnesi eklenir, sonraki sahneler 12 vuruş kayar.
# Kullanım: python3 album-ek.py <çalışma>  ->  node kur.js plan-album-ek.js <çalışma> <çıktı> kart|final
import sys, os, subprocess, multiprocessing as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import album as A

EK = 12
ma = A.ma
masa3 = dict(ad='masa3', b=(50, 62), arka=ma('DSC04731'),
             kart=[(ma('DSC04737'), 360, 330, -3, 540, 51, 'drop'),
                   (ma('DSC04752'), 960, 320, 2, 540, 52, 'slideR'),
                   (ma('DSC04751'), 1560, 335, -2, 540, 53, 'slideL'),
                   (ma('DSC04738'), 360, 760, 3, 540, 54, 'pop'),
                   (ma('DSC04749'), 960, 770, -3, 540, 55, 'drop'),
                   (ma('DSC04731'), 1560, 755, 2, 540, 56, 'slideR')])

yeni = []
for sc in A.SAHNELER:
    b0, b1 = sc['b']
    if b0 >= 50:   # masa2 sonrası her şey kayar
        sc = dict(sc, b=(b0 + EK, b1 + EK), kart=[tuple(k[:5]) + (k[5] + EK,) + tuple(k[6:]) for k in sc['kart']])
    yeni.append(sc)
    if sc['ad'] == 'masa2':
        yeni.append(masa3)
A.SAHNELER[:] = yeni

if __name__ == '__main__':
    mp.set_start_method('fork')
    W_ = sys.argv[1]
    sys.argv = [sys.argv[0], W_]
    os.makedirs(W_ + '/album', exist_ok=True)
    with mp.Pool(6) as p:
        sonuc = p.map(A.sahne_render, range(len(A.SAHNELER)))
    lf = W_ + '/album/liste.txt'
    open(lf, 'w').write('\n'.join(f"file '{o}'" for o, _ in sonuc))
    subprocess.run([A.FFMPEG, '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lf, '-c', 'copy', W_ + '/govde.mp4'], check=True)
    print('govde kare', sum(n for _, n in sonuc), 'beklenen', A.F(A.SAHNELER[-1]['b'][1]))
