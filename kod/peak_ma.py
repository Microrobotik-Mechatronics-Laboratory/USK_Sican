"""peak_ma.py — Quad diz moment kolu eğrisi + tepe + trot (lokomosyon) aralığındaki değişim.
Çalıştır:  python peak_ma.py
Gerekli:   opensim, rat_hindlimb_0.2.osim, rat_trot.mot, build_osim.py (+ rig.py, wrap.py)
Ne yapar:  quad (RF/VL/VI/VM) diz moment kolunu diz açısına karşı hesaplar (OpenSim
           computeMomentArm — ma_validate.py ile AYNI yöntem), tepe noktasını ve trotun
           kullandığı açı aralığındaki toplam değişimi yazdırır.
Not:       Açıklama belgesindeki 3,75 mm (tepe) ve 0,47 mm (trot aralığındaki değişim)
           sayıları bu scriptten çıkar.
"""
import numpy as np, opensim, build_osim
opensim.Logger.setLevelString('Off')

def trot_knee_range(path='rat_trot.mot'):
    """rat_trot.mot'tan knee_flx sütununun min/max'ı (derece; inDegrees=yes)."""
    txt = open(path).read().splitlines()
    hi = next(i for i, l in enumerate(txt) if l.strip().lower().startswith('time'))
    hdr = txt[hi].split('\t')
    ki = next(i for i, c in enumerate(hdr) if 'knee' in c.lower())
    vals = [float(l.split('\t')[ki]) for l in txt[hi + 1:] if l.strip()]
    return min(vals), max(vals)

# Modeli kur (sarmalı) ve diz moment kolunu tara
m, bod = build_osim.build(True); s = m.initSystem()
cs = m.getCoordinateSet(); knee = cs.get('knee_flx'); mus = m.getMuscles()
QUAD = ['RF', 'VL', 'VI', 'VM']
deg = np.linspace(-150, -20, 40)
r = []
for d in deg:
    knee.setValue(s, np.radians(d)); m.realizePosition(s)
    r.append(np.mean([mus.get(n).computeMomentArm(s, knee) * 1000 for n in QUAD]))
r = np.array(r)

pi = int(np.argmax(r))
print(f"Quad diz moment kolu tepesi : {r[pi]:.2f} mm  @ {deg[pi]:.0f} derece")
try:
    kmin, kmax = trot_knee_range()
    band = (deg >= kmin) & (deg <= kmax)
    print(f"Trot (lokomosyon) aralığı   : {kmin:.0f} ... {kmax:.0f} derece")
    print(f"Bu aralıkta moment kolu     : {r[band].min():.2f} ... {r[band].max():.2f} mm "
          f"(toplam değişim {r[band].max() - r[band].min():.2f} mm)")
except FileNotFoundError:
    print("(rat_trot.mot bulunamadı — yalnızca eğri/tepe hesaplandı)")
