# USK Bildirisi — Teslim Paketi

## İçerik
- **ACIKLAMA_yontem_farklar_dogrulama.docx** — asıl açıklama belgesi: ana makaleden (Johnson 2008) farklar, ne yaptığımız, doğrulama, örtüşmeler, hangi kod dosyası ne yapıyor (kod parçalarıyla), program rolleri, avantaj/dezavantaj, model-dosya sözlüğü. Model fotoğrafı ve iki şekil gömülüdür.
- **USK_ozet_final.docx** — **kongreye gönderilecek NİHAİ özet** (TR + EN, ≤300 kelime). Sonundaki "Ek materyaller" bölümü özet metnine dahil değildir, yalnız paket notudur.
- **OZET_PAKET.md** — özetin çalışma/referans sürümü + tam kaynak künyeleri + herkesin anlayacağı özet. (Nihai metin docx'tedir.)
- **gorsel/** — `rat_hindlimb_gait.gif` (trot animasyonu) + `rat_hindlimb_still_500.png` (iskelet fotoğrafı).
- **kod/** — minimum çalışır kod seti + model (`rat_hindlimb_0.2.osim`) + `rat_trot.mot`. Çalıştırma sırası `kod/OKU.md`'de.

## Model dosyaları — hangi .osim ne (önemli)
- **rat_hindlimb_0.2.osim — GİRDİ:** kodun okuduğu kaynak. Johnson 2008 portu, legacy OpenSim 3.3 formatı, **38 kas**. Bu pakette bulunan tek .osim budur.
- **rat_rebuilt.osim — ÇIKTI:** `build_osim.py` çalışınca üretilir; OpenSim 4.x formatı, aynı 38 kaslı model. Pakette hazır gelmez.
- **rat_big_clean.osim — ANİMASYON:** 35 kaslı, büyütülmüş görselleştirme sürümü (3 kalça kası gizli). Bu minimal pakette yoktur.
- Özetteki **"38 kas" tam modeli**, **"35 kas" yalnız animasyon sürümünü** anlatır. Kod her zaman `rat_hindlimb_0.2.osim`'den kurar.

## Kısa harita — iki kol
- RENDER: `convert_vtp (mesh) → rig.fk (FK) → walk.ik (IK) → make_walk (MuJoCo animasyon)`
- ANALİZ: `build_osim (OpenSim) → ma_validate / clean_ma / peak_ma (moment kolları)`
