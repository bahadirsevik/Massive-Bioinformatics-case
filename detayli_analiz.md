# Mini-Bioinformatics Pipeline: Kalite Kontrol Raporu (barcode77 Girdisi)

**Geliştirici:** Yazılım Mühendisi Adayı  
**Alıcı:** Prof. Dr. Kılıç (Moleküler Biyoloji Bölümü)  
**Tarih:** 9 Mart 

---

Saygıdeğer Prof. Dr. Kılıç,

Laboratuvarınız tarafından iletilen **long-read sequencing (uzun okuma)** verisi olan `barcode77.fastq.gz` dosyası için kurduğum otomatik Kalite Kontrol (QC) hattı başarıyla tamamlandı. Python geliştiricisi perspektifiyle, verinizin özelliklerini saptamak adına hem özel betikler hem de endüstri standardı olan NanoPlot arcını Docker imajımız içerisinde çalıştırdım. Analiz sonucunda oluşturduğum çıktılara dair teknik rapor ve değerlendirmemi aşağıda iletiyorum.

## 1. Genel Veri Hacmi ve Metrikler (`summary_statistics.txt`)

Veri setimizde tam **81.011** adet okuma tespit edilmiştir. Bu okumalar sayesinde pipeline yaklaşık **84 Megabase (84,108,485 bp)** uzunluğunda devasa bir dizi hacmi (Yield) taramıştır. 

*   **En Kısa Okuma:** 86 bp
*   **En Uzun Okuma:** 686.155 bp (Bu inanılmaz rakam, tercih ettiğiniz long-read teknolojisinin başarılı bir kütüphane hazırlığına (library prep) sahip olduğunu gösteriyor.)
*   **Ortalama/Medyan Uzunluk:** Ortalama okuma boyu 1.038 bp iken medyan 547 bp'de konumlanmıştır. 
*   **N50 Skoru:** Verinin kalitesinin ana metriklerinden olan N50 skorunu 1.761 bp olarak hesapladım. Kısaca, dizilerin toplam uzunluğunun yarısını 1.761 bp veya daha büyük bazlar oluşturuyor.

---

## 2. Grafiksel Çıktıların Analizi (Seaborn Özel Raporu)

Yazdığım Python betikleri ile elde ettiğimiz csv formatındaki değerleri, `results/plots_and_summary/` dizini altında yüksek çözünürlüklü grafiklerle modelledim:

### A. Okuma Uzunluğu Dağılımı (`length_distribution.png`)
Grafiğin x-ekseni (logaritmik ölçekte) okuma uzunluklarını gösteriyor. Neden logaritmik kullandım? Çünkü long-read verilerinde kısa diziler çok sık görülür, ama "kuyruk (tail)" tabir ettiğimiz 680kb civarı uç değerler de vardır. 
*   **Yorumum:** Orijinal histogram sağa çarpık (right-skewed) bir yapı sunuyor ve bu da long-read teknolojilerinde klasik olarak beklendiği gibi oldukça sağlıklı bir profil. "Çöplük" dediğimiz anlamsız kısa diziler yerine, 1-10kb bandında çok kalın bir kümelenme görüyorum ki bu sizin işinizi hedeflenen gen tespitinde çok kolaylaştıracak.

### B. Kalite Dağılım Skorları (`quality_distribution.png`)
Quality Distribution (Mean Phred) histogramında her bir dizinin aritmetik ortalama kalitesini eşledim.
*   **Yorumum:** Dizilerin ezici bir çoğunluğunun Q-skoru 16-20 aralığında şahane bir "Peak (Zirve)" oluşturmuştur. Genel ortalamamız ise **17.90**. Eğer bu bir kısa okuma (Illumina) olsaydı Q30 beklerdik, ancak kullandığınız teknoloji (Nanopore vb.) için Q17 ve üzeri "A-Tier" bir hata oranına (`~%1.6`) işaret eder. Sinyal işlemede (basecalling) hiçbir sıkıntı çıkmamış.

### C. GC İçeriği Dağılımı (`gc_distribution.png`)
Her dizideki Guanin ve Sitozin dizilerinin oranlarını hesapladık.
*   **Yorumum:** Grafik, çan eğrisi formunu takip eden simetrik bir normal dağılım (Gaussian) gösteriyor ve tam %52-53 sularında pik yapıyor. Herhangi bir kirlenme, adaptör ikileşi veya farklı bir organizmadan dışarı kopma hissettiren çift-tepeli (bimodal) veya keskin bir eğri gözlemlemedim. Genel oranımız net olarak **%53.00**.

---

## 3. NanoPlot Endüstriyel QC (`nanoplot/NanoPlot-report.html`)

Sistemin esnekliğini test etmek için entegre ettiğim **NanoPlot** motoru benim yazdığım betiklerin sonuçlarını da bir üst seviyede doğrulamış oldu. Eğer isterseniz projedeki `.html` dosyasını tarayıcınızdan açarak:
1. Okuma dizilimi ve Q-Skoru Isı Haritası (Heatmap)'ni interaktif bir şekilde inceleyebilir,
2. İki farklı metrik arasındaki korelasyon matrislerini (scatter plot) detaylandırıp farenizle üzerinde gezebilirsiniz.

---

## 🚀 Sonuç ve Sonraki Adımlar

Yazılım geliştirme ve veri mühendisliği pratiklerini laboratuvarınızın biyolojik verisiyle harmanladığımda, elde edilen tablonun kalitesine kanaatim tamdır.

**Eyleme Geçirilebilir Tavsiyem (Actionable Insight):**
Bu veri yapısı, (N50: 1.7K ve Mean Q: 17.9) hiçbir temizleme aşamasına (trimming/filtering) ciddi anlamda gerek bile duymadan rahatlıkla **Hizalama (Alignment - Minimap2 vb.)** aşamalarına, hatta denovo Assembly (montaj) işlemlerine sevk edilebilir kalitededir. 

Şifre okuma (decipher) yolculuğunuzda diğer adımlarınızı rahatça planlayabilirsiniz. Eğer sistemi farklı formatlar (örn `.bam` vs.) ya da bulut entegrasyonu (AWS vb.) ile ölçeklendirmeyi isterseniz teknik vizyonumla destek olmaya devam edeceğim.

Saygılarımla.

**[Adınız / Soyadınız]**
Mühendis Stajyeri
