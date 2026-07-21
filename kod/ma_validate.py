# =============================================================================
# ADIM 1 — Diz moment kolu doğrulaması (Johnson 2008 ile karşılaştırma)
# OpenSim 4.5 · native wrapping (2 torus DAHİL, MuJoCo'nun aksine)
# kod/ klasörüne koy ve çalıştır:  python ma_validate.py
# Parametre düzeltmesine İHTİYAÇ YOK — moment kolu tamamen geometriktir.
# =============================================================================
import numpy as np, build_osim, rig
DEG = np.pi / 180.0

m, bod = build_osim.build(True)
s   = m.initSystem()
cs  = m.getCoordinateSet()
knee = cs.get('knee_flx')
musc = m.getMuscles()
kc = cs.get('knee_flx')
print("knee_flx aralığı (°):", np.degrees(kc.getRangeMin()), "..", np.degrees(kc.getRangeMax()))

def set_pose(d):
    for k, v in d.items():
        if any(cs.get(i).getName() == k for i in range(cs.getSize())):
            cs.get(k).setValue(s, v, False)
    m.assemble(s); m.realizePosition(s)

# Diz ROM taraması: tam fleksiyon (~ -120°) .. ekstansiyon (0°)
knee_deg = list(range(-120, -19, 10))   # -120..-20 (geçerli/gait aralığı); 0° dahil etme
names = [musc.get(i).getName() for i in range(musc.getSize())]
base  = dict(rig.defaults)

# --- 1. geçiş: dizi geçen kasları bul (ROM boyunca |MA| > 0.5 mm olanlar) ---
peak = {n: 0.0 for n in names}
curves = {kd: {} for kd in knee_deg}
for kd in knee_deg:
    d = dict(base); d['knee_flx'] = kd * DEG; set_pose(d)
    for n in names:
        ma = musc.get(n).computeMomentArm(s, knee) * 1000.0  # m -> mm
        curves[kd][n] = ma
        peak[n] = max(peak[n], abs(ma))
knee_cross = [n for n in names if peak[n] > 0.5]

# --- 2. geçiş: sadece dizi geçen kasların eğrilerini yazdır ---
print("Sign: + = ekstansör tarafı (senin clean_ma.py çıktınla işaret uyumunu KONTROL ET)\n")
print("knee° | " + " ".join(f"{n:>6s}" for n in knee_cross))
for kd in knee_deg:
    print(f"{kd:5d} | " + " ".join(f"{curves[kd][n]:6.2f}" for n in knee_cross))

print("\nHer kasın |MA| tepe değeri (mm):")
for n in sorted(knee_cross, key=lambda x: -peak[x]):
    print(f"  {n:5s} {peak[n]:6.2f}")

# Tek nokta kontrolü — abstract'taki +3,7 mm burada çıkmalı:
d = dict(base); d['knee_flx'] = rig.defaults.get('knee_flx', -1.0); set_pose(d)
print("\nVarsayılan diz açısında quadriceps moment kolları (abstract ~+3.7 mm):")
for n in ['RF', 'VL', 'VI', 'VM']:
    if n in names:
        print(f"  {n:5s} {musc.get(n).computeMomentArm(s, knee)*1000:6.2f} mm")

# -----------------------------------------------------------------------------
# NE YAPACAKSIN:
#   1) Bu eğrileri Johnson 2008'in diz moment-kolu figürleriyle (Fig. 4-5) karşılaştır.
#   2) İşaret uyumlu, büyüklükler ~aynı aralıktaysa -> DIŞ DOĞRULAMA sağlandı.
#      Bana değerleri gönder, abstract'a doğrulanmış cümleyi eklerim.
#   3) computeMomentArm işaret konvansiyonu senin r=-dL/dθ'ndan farklı çıkarsa,
#      işareti ters çevir; büyüklük aynı kalır.
# -----------------------------------------------------------------------------
