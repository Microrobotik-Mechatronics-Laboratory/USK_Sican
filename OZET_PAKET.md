# 24. USK — Bildiri Paketi (tümüyle sıçan · gelecek odaklı · atıflı)

> **NOT (sürüm):** Kongreye gönderilecek NİHAİ özet **USK_ozet_final.docx**'tir. Oradaki BULGULAR bölümü, quad moment kolunun adım aralığında az değiştiğini de belirtecek biçimde hafifçe güncellenmiştir (299 kelime). Aşağıdaki metin çalışma/referans sürümüdür (294 kelime) ve tam kaynak künyelerini içerir.

### Konu: Duyusal ve motor sistemler · Sunum: Poster · Çalışma: SIÇAN (Rattus norvegicus, Sprague-Dawley)

> **Format doğrulandı** (USK resmî kuralları, usktubas.org): Amaç / Gereç ve Yöntem / Bulgular / Sonuç **dört bölüm zorunlu** — tam makale değil, özet için de böyle. Sınır: **300 kelime (anahtar sözcükler HARİÇ)**; destek satırı sınıra dahil. Denek türü ve sayısı Gereç-Yöntem'de belirtilmeli. Anahtar sözcük 3–5. Başlığın yalnız ilk harfi büyük. TR + EN zorunlu.

---

# A) AKADEMİK ÖZET

## 🇹🇷 Türkçe (294 kelime + destek · edilgen çatı)

**BAŞLIK:** Sıçan lokomosyonunda kinematikten kas kuvvetlerine ve nöral sinyallere: açık kaynaklı bir nöromekanik altyapı

**AMAÇ:** Lokomosyon, sinir sisteminden kaslara ve oradan eklem hareketine uzanan bir zincirle ortaya çıkar. Bu zincir ölçülmeden, lokomosyonun nöral kontrolü anlaşılamaz. Bu çalışmanın amacı, sıçanda (Rattus norvegicus, Sprague-Dawley) bu zinciri kurmaktır. Bunun için sıçan, koşu bandında işaretçisiz kaydedilecektir. Bu hareketten kas kuvvetleri çıkarılacaktır (kinematikten kinetiğe). Ardından bu kuvvetleri süren nöral sinyaller belirlenecektir. Böylece gözlenen hareket, altında yatan nöral kodlamaya bağlanacaktır.

**GEREÇ VE YÖNTEM:** Bu bildiride sunulan ilk aşama, deney öncesi yöntemi kurmak için bilgisayar ortamında (in silico) yürütülmüştür; canlı hayvan kullanılmamıştır (n=1 model). Denek, yayımlanmış bir sıçan arka bacak kas-iskelet modelidir (Johnson ve ark., 2008; 6 gövde/segment, 38 kas). Model, bir fizik motoruna (MuJoCo) aktarılmıştır. Ayrıca bağımsız olarak OpenSim'de yeniden kurulmuştur. Bir tırıs döngüsü, distal ayak yörüngelerinden ters kinematikle oluşturulmuştur. Kas yolları, kemik etrafındaki sarılmayı içerecek biçimde tanımlanmıştır.

**BULGULAR:** Model, iki bağımsız yolla hesaplanmıştır: Python'da elle yazılan bir ileri kinematik motoru ve OpenSim'de yeniden kurulum. İki uygulamanın kemik hareketleri birebir örtüşmüştür (<0,1 mm). Böylece modelin aktarımı doğrulanmıştır. Dört baş kas (quadriceps) dahil 38 kasın tümü, doğru anatomik bağlantılar ve 13 sarma nesnesiyle yeniden üretilmiştir. İşlevsel bir kontrol de yapılmıştır. Kas-tendon boyları, eklem açısıyla doğru yönde değişmiştir: diz büküldükçe ekstansörler uzamış, fleksörler kısalmıştır. Diz moment kolları (r=−dL/dθ), dört baş kasta ≈+3,7 mm'de kümelenmiştir. Fleksörlerde ise ters işaretli çıkmıştır (ör. semimembranosus ≈−3,9 mm). Model ve kod açık kaynak yayımlanmıştır.

**SONUÇ:** Bu aşamada üretilen hareket, kuvvet içermeyen öngörülmüş bir yeniden oluşturmadır. Asıl katkı ise sıçan deneyine hazır nöromekanik altyapıdır. Program üç adımlıdır. (i) İşaretçisiz kaydedilecek (Mathis ve ark., 2018) sıçan kinematiği bu modele oturtulacaktır. (ii) Ters dinamik ve moment kollarıyla eklem torkları, ardından Hill-tipi statik optimizasyonla kas kuvvetleri hesaplanacaktır. (iii) Kas boyu ve kuvvet, propriyoseptif afferent modelleriyle ateşleme hızlarına çevrilecektir (kas iğciği Ia/II, Golgi tendon organı Ib; Mileusnic ve ark., 2006). Böylece kas-iskelet katmanı, sıçan lokomosyonunu omurilik devre modellerine bağlayan bir nöral arayüz kazanır.

**DESTEK:** _[Oğuz Hoca — TÜBİTAK vb. proje no.; yoksa bu satırı sil.]_

**ANAHTAR SÖZCÜKLER:** lokomosyon, nöromekanik, kas-iskelet modelleme, ters dinamik, proprioseptif geri bildirim

## 🇬🇧 English (294 words + support)

**TITLE:** From kinematics to muscle forces and neural signals in rat locomotion: an open-source neuromechanical infrastructure

**AIM:** Locomotion emerges through a chain from the nervous system to muscles to joint motion. Without measuring it, the neural control of locomotion cannot be resolved. This study builds that chain in the rat (Rattus norvegicus, Sprague-Dawley) and recovers, from treadmill locomotion recorded markerlessly, the muscle forces (kinematics to kinetics) and the neural signals driving them, linking observed movement to its neural code.

**MATERIALS AND METHODS:** The first stage here was carried out in silico to establish the method beforehand; no live animals were used (n=1 model). The subject is a published rat hindlimb musculoskeletal model (Johnson et al., 2008; 6 body segments, 38 muscles). The model was ported to a physics engine (MuJoCo) and independently rebuilt in OpenSim; a trot cycle was reconstructed by inverse kinematics on distal-foot trajectories, wrapping muscle paths around bone.

**RESULTS:** Bone kinematics matched to <0.1 mm across two independent implementations — a hand-written Python forward-kinematics engine and an OpenSim rebuild — verifying the port. All 38 muscles, including the four-headed quadriceps, were reproduced with correct anatomical attachments and 13 wrap objects. As a functional check, muscle–tendon lengths changed in the correct direction with joint angle; knee moment arms (r=−dL/dθ) clustered at ≈+3.7 mm across the quadriceps and were opposite-signed in flexors. Model and code were released open-source.

**CONCLUSION:** The motion here is a force-free, prescribed reconstruction; the contribution is neuromechanical infrastructure ready for the rat experiment. The program has three steps: (i) fitting markerless-recorded (Mathis et al., 2018) rat kinematics onto this model; (ii) joint torques from inverse dynamics and moment arms, then muscle forces via Hill-type static optimization; (iii) mapping muscle length and force to firing rates through proprioceptive afferent models (spindle Ia/II, Golgi tendon organ Ib; Mileusnic et al., 2006). The musculoskeletal layer thereby gains a neural interface linking rat locomotion to spinal circuit models.

**KEYWORDS:** locomotion, neuromechanics, musculoskeletal modeling, inverse dynamics, proprioceptive feedback

---

# A2) KAYNAKLAR (poster/özet dipnotu — tam künye)

1. **Johnson WL, Jindrich DL, Roy RR, Edgerton VR.** A three-dimensional model of the rat hindlimb: musculoskeletal geometry and moment arms. *Journal of Biomechanics.* 2008;41(3):610–619.
2. **Mathis A, Mamidanna P, Cury KM, Abe T, Murthy VN, Mathis MW, Bethge M.** DeepLabCut: markerless pose estimation of user-defined body parts with deep learning. *Nature Neuroscience.* 2018;21(9):1281–1289.
3. **Mileusnic MP, Brown IE, Lan N, Loeb GE.** Mathematical models of proprioceptors. I. Control and transduction in the muscle spindle. *Journal of Neurophysiology.* 2006;96(4):1772–1788.

---

# B) HERKESİN ANLAYACAĞI ÖZET

Hareket, sinir sisteminden kaslara giden sinyallerle olur. Bir motor komut gider, kas kasılır, kuvvet üretir, eklem döner ve uzuv hareket eder. Bu zincirin ortasında bir mekanik basamak vardır: yürürken hangi kasın ne kadar kuvvet ürettiği. Bunu ölçmeden, sinir sisteminin hareketi nasıl yönettiğini anlamak zordur.

Asıl hedefimiz bu kuvvetleri gerçek veriden çıkarmaktır. Bir sıçanı koşu bandında kamerayla kaydedeceğiz (işaretçisiz izleme). Hareketinden, her kasın üretmesi gereken kuvveti hesaplayacağız (kinematikten kinetiğe). Bu kuvvetleri ekip arkadaşımıza vereceğiz. O da bu kasları ateşleyen sinir sinyallerini çözecek.

Gerçek kayıt öncesi, yöntemi kurup denemek için bunu bilgisayarda modelledik. Yayımlanmış bir sıçan arka bacak iskelet-kas modelini kullandık (Johnson ve ark., 2008; kemikleri ve kaslarıyla). Modeli bir fizik motoruna (MuJoCo) aktardık, OpenSim'de bağımsız olarak yeniden kurduk ve bir tırıs yürüyüşünü yeniden oluşturduk. Önemli not: gördüğünüz animasyon gerçek bir kayıt değildir; modelin ürettiği yapay bir harekettir. İki bağımsız uygulamada kemik hareketi birebir örtüştü (<0,1 mm). 38 kasın tümü doğru anatomik yerinde yeniden üretildi. Kaslar işlevsel olarak da doğru davrandı: dört baş kasın diz moment kolu ≈3,7 mm, fleksörlerde ters yönde.

---

# C) GÖRSEL: yalın iskelet — `rat_hindlimb_still_500.png` (özet) / `rat_hindlimb_gait.gif` (poster).

# D) KONTROL: [ ] yazar (Oğuz Hoca) · [ ] destek satırı · [ ] dil (TR/EN) · [ ] GÖNDER
