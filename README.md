# Sıçan Arka Bacak Nöromekanik Boru Hattı — 24. USK (Poster)

**Sıçan lokomosyonunda kinematikten kas kuvvetlerine ve nöral sinyallere: açık kaynaklı bir nöromekanik altyapı**
Deniz Çetin, Musa Dereli [, Barış Oğuz Gürses] — Ege Üniversitesi

> **Hocam, bu depoyu okumak için hiçbir şey indirmenize gerek yok.** Aşağıdaki özeti, şekli ve bağlantıdaki tüm dosyaları doğrudan tarayıcıda görebilirsiniz — bunlar yalnızca birkaç yüz KB veri harcar. Tüm paketi (~3 MB) indirmek yalnızca sağ üstteki yeşil **Code ▸ Download ZIP** düğmesine basarsanız olur; ona gerek yok.

![Sıçan arka bacak modeli — tırıs döngüsünden bir kare](gorsel/rat_hindlimb_still_500.png)

*Model-üretimi, kuvvet içermeyen kinematik rekonstrüksiyon (gerçek kayıt değildir). Hareketli sürüm: [gorsel/rat_hindlimb_gait.gif](gorsel/rat_hindlimb_gait.gif) — ~2.5 MB olduğundan yalnız izlemek isterseniz açın; içerik yukarıdaki karede görülüyor.*

## Özet (Türkçe)

**AMAÇ —** Lokomosyon, sinir sisteminden kaslara ve oradan eklem hareketine uzanan bir zincirle ortaya çıkar. Bu zincir ölçülmeden, lokomosyonun nöral kontrolü anlaşılamaz. Bu çalışmanın amacı, sıçanda (Rattus norvegicus, Sprague-Dawley) bu zinciri kurmaktır. Bunun için sıçan, koşu bandında işaretçisiz kaydedilecektir. Bu hareketten kas kuvvetleri (kinematikten kinetiğe), ardından bu kuvvetleri süren nöral sinyaller çıkarılarak gözlenen hareket nöral kodlamaya bağlanacaktır. 

**GEREÇ VE YÖNTEM —** Bu bildiride sunulan ilk aşama, deney öncesi yöntemi kurmak için bilgisayar ortamında (in silico) yürütülmüştür; canlı hayvan kullanılmamıştır (n=1 model). Denek, yayımlanmış bir sıçan arka bacak kas-iskelet modelidir (Johnson ve ark., 2008; 6 gövde/segment, 38 kas). Model, bir fizik motoruna (MuJoCo) aktarılmıştır. Ayrıca bağımsız olarak OpenSim'de yeniden kurulmuştur. Bir tırıs döngüsü, distal ayak yörüngelerinden ters kinematikle oluşturulmuştur. Kas yolları, kemik etrafındaki sarılmayı içerecek biçimde tanımlanmıştır. 

**BULGULAR —** Model, iki bağımsız yolla hesaplanmıştır: Python'da elle yazılan bir ileri kinematik motoru ve OpenSim'de yeniden kurulum. İki uygulamanın kemik hareketleri birebir örtüşmüştür (<0,1 mm). Böylece modelin aktarımı doğrulanmıştır. Dört baş kas (quadriceps) dahil 38 kasın tümü, doğru anatomik bağlantılar ve 13 sarma nesnesiyle yeniden üretilmiştir. Kas-tendon boyları eklem açısıyla doğru yönde değişmiş (diz büküldükçe ekstansörler uzamış, fleksörler kısalmış); diz moment kolları (r=−dL/dθ) dört baş kasta ≈+3,7 mm'de kümelenmiş ve adım döngüsü diz aralığında az değişmiş, fleksörlerde ters işaretli çıkmıştır (ör. semimembranosus ≈−3,9 mm). Model ve kod açık kaynak yayımlanmıştır. 

**SONUÇ —** Buradaki hareket ölçülmemiş; ayak yörüngesi seçilip ters kinematikle üretilmiş, kuvvet hesaplanmamıştır. Katkı, geometrisi doğrulanmış ve sıçan deneyine hazır nöromekanik altyapıdır. Program üç adımlıdır. (i) İşaretçisiz kaydedilecek (Mathis ve ark., 2018) sıçan kinematiği bu modele oturtulacaktır. (ii) Kas mimarisi (PCSA) parametrelendikten sonra, ters dinamik ve moment kollarıyla eklem torkları ve Hill-tipi statik optimizasyonla kas kuvvetleri hesaplanacaktır. (iii) Kas boyu ve kuvvet, propriyoseptif afferent modelleriyle ateşleme hızlarına çevrilecektir (kas iğciği Ia/II, Golgi tendon organı Ib; Mileusnic ve ark., 2006). Böylece kas-iskelet katmanı, sıçan lokomosyonunu omurilik devre modellerine bağlayan bir nöral arayüz kazanır.

İngilizce özet ve baskı düzeni: **[USK_ozet_final.pdf](USK_ozet_final.pdf)** (tıklayınca tarayıcıda açılır, inmez).

## İndirmeden okuma rehberi — hangi dosya ne

| İçerik | Bağlantı | Tarayıcıda nasıl görünür |
|---|---|---|
| **Gönderilecek özet (TR + EN)** | [USK_ozet_final.pdf](USK_ozet_final.pdf) | GitHub PDF'i önizler |
| **Yöntem · ana makaleden farklar · doğrulama · kod rolleri** (ayrıntılı) | [ACIKLAMA_yontem_farklar_dogrulama.pdf](ACIKLAMA_yontem_farklar_dogrulama.pdf) | PDF önizleme |
| Özetin çalışma sürümü + tam kaynak künyeleri | [OZET_PAKET.md](OZET_PAKET.md) | Markdown, otomatik render |
| Paket haritası / dosya sözlüğü | [BENI_OKU.md](BENI_OKU.md) | Markdown |
| Kod (ileri/ters kinematik, moment kolu, render) | [kod/](kod/) | `.py` dosyaları metin olarak açılır |
| Kodun çalıştırma sırası | [kod/OKU.md](kod/OKU.md) | Markdown |
| Model + hareket dosyası | `kod/rat_hindlimb_0.2.osim`, `kod/rat_trot.mot` | metin (XML) olarak açılır |

> **Neden PDF var:** Aynı belgelerin `.docx` sürümleri de depoda; ancak GitHub Word dosyalarını tarayıcıda **önizlemez** (tıklayınca iner). Okumak için yukarıdaki **PDF** bağlantılarını kullanın.

---
*Bu çalışma ilk aşamadır: hareket ölçülmemiş, ayak yörüngesi seçilip ters kinematikle üretilmiş, kuvvet hesaplanmamıştır. Katkı, geometrisi doğrulanmış ve sıçan deneyine hazır nöromekanik altyapıdır.*
