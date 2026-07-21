# Çalıştırma notu (minimum kod seti)

**Gereksinim:** Python 3.x, `numpy`, `scipy`, ve moment-kolu/OpenSim adımları için `opensim` (OpenSim 4.x Python paketi). Render için ek olarak `mujoco` + `Pillow`.

**Dosyalar aynı klasörde çalışır** (relative path). Model dosyası `rat_hindlimb_0.2.osim` ve `rat_trot.mot` bu klasörde olmalı. (Görsel render için ayrıca modelin `Geometry/` mesh klasörü gerekir; moment-kolu hesabı için gerekmez.)

## Boru hattı sırası
1. `convert_vtp.py`  — kemik mesh'lerini (VTK .vtp) dönüştürür (render için).
2. `rig.py`          — ileri kinematik (FK) motoru. Tek başına çalışmaz; diğerleri çağırır.
3. `walk.py`         — ters kinematik (IK); trotu üretir (rig.fk kullanır).
4. `build_osim.py`   — modeli OpenSim 4.x'te yeniden kurar (rig + wrap'a bağımlı).
5. `ma_validate.py`  — diz moment kollarını OpenSim `computeMomentArm` ile doğrular (+3,7 quad).
6. `clean_ma.py`     — moment kolunu r=−dL/dθ ile hesaplar (çapraz kontrol).
7. `peak_ma.py`      — quad eğrisi + tepe + trot aralığındaki değişim (3,75 mm / 0,47 mm).
8. `make_walk.py`    — trot animasyonunu çizer (MuJoCo mocap).

Detaylı açıklama için üst klasördeki **ACIKLAMA** Word belgesine bakın.
