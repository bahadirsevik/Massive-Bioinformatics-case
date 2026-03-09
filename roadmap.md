# 🧬 Bioinformatics Pipeline & Reporting - Detailed Coding Roadmap

Bu yol haritası, yazılım mühendisliği temiz kod prensipleri ve seçilen teknoloji setiyle (Snakemake + Docker + Python/Biopython + NanoPlot + Seaborn) adım adım nasıl ilerleyeceğimizi detaylandırır.

## 🛠️ Seçilen Teknoloji Seti (Tech Stack)
*   **Orkestrasyon (Pipeline):** Snakemake (Pythonic, temiz sözdizimi, tekrarlanabilirlik)
*   **Ortam İzolasyonu:** Docker (Tüm bağımlılıkların paketlenmesi, "bende çalışıyor" sorununun çözümü)
*   **Veri Analizi Scripti:** Python, Biopython (FASTQ parse etmek için) ve Pandas (veriyi yapılandırmak için)
*   **Görselleştirme:** Seaborn ve Matplotlib (İstatistiksel, şık statik grafikler)
*   **Long-read QC (Hazır Araç):** NanoPlot (Nanopore/PacBio verisi için endüstri standardı, hızlı ve HTML raporlama)

---

## 🚀 Aşama 1: Proje Kurulumu ve Demo Veri (Setup & Data)
**Hedef:** Proje dizini hiyerarşisini kurmak ve pipeline'da test etmek için küçük bir dummy veri elde etmek.

*   [ ] **1.1. Dizin Yapısının Kurulması:**
    *   `data/` (Girdi dosyaları için)
    *   `scripts/` (Python scriptlerimiz için)
    *   `results/` (Çıktılar, grafikler ve raporlar için)
    *   `Dockerfile` ve `Snakefile` ana dizinde (root).
    *   `.gitignore` oluşturulması (`data/` ve `results/` vs. takip edilmeyecek şekilde ayarlanır).
*   [ ] **1.2. Dummy FASTQ Verisi Hazırlanması:**
    *   Pipeline'ı test edebilmek için gerçek veya sentetik minik bir FASTQ (long-read) dosyası indirilip/yaratılıp `data/` klasörüne eklenecek.

## 🏗️ Aşama 2: Python Scriptlerinin Yazılması (Core Processing)
**Hedef:** Biyolojik veriyi analiz edip istatistiksel sonuç çıkartacak ve bu sonuçları görselleştirecek programların yazılması.

*   [ ] **2.1. `scripts/calculate_metrics.py` (Metrik Hesaplayıcı)**
    *   **Girdi:** Bir `.fastq` veya `.fastq.gz` dosyası (CLI argümanı ile alınacak).
    *   **İşlev:** Biopython `SeqIO` modülü ile dosyayı satır satır asenkron (veya generator pattern ile) okumak. (RAM dostu yaklaşım).
    *   **Hesaplamalar:**
        *   Her okumanın karakter (baz) uzunluğu.
        *   Her okumadaki G ve C harflerinin toplam uzunluğa oranı (% GC Content).
        *   Her okumanın Phred kalite skorlarının aritmetik ortalaması.
    *   **Çıktı:** Sonuçların Pandas ile bir DataFrame'e aktarılıp `results/metrics.csv` olarak kaydedilmesi.
*   [ ] **2.2. `scripts/plot_metrics.py` (Görselleştirme)**
    *   **Girdi:** `results/metrics.csv`
    *   **İşlev:** Seaborn kullanarak şık grafikler oluşturmak.
    *   **Çıktılar:**
        *   `results/gc_distribution.png` (Histogram veya KDE)
        *   `results/length_distribution.png` (Histogram, long-read olduğu için log-scale kullanımı gerekebilir)
        *   `results/quality_distribution.png` (Histogram)
        *   `results/summary_statistics.txt` (Min, Max, Mean, Median, N50 skorlarının hesaplanıp yazdırılması).

## 🐍 Aşama 3: Pipeline Orkestrasyonu (Snakemake)
**Hedef:** Hazır aracımız (NanoPlot) ve kendi yazdığımız scriptlerin birbirini tetikleyerek sıfırdan sona kadar tek komutla çalışmasını sağlayan `Snakefile`'ı yazmak.

*   [ ] **3.1. `Snakefile` Kurulumu:**
    *   `rule all:` Hedeflenen nihai dosyaların tanımlanması (pipeline bitti demesi için gereken dosyalar).
    *   `rule run_nanoplot:` Girdi FASTQ'yu alıp hazır araç olan NanoPlot'u çalıştıracak ve `results/nanoplot/` klasörüne rapor çıkaracak adım.
    *   `rule calculate_metrics:` `data/` klasöründeki FASTQ dosyasını `scripts/calculate_metrics.py`'a argüman olarak besleyen adım.
    *   `rule plot_metrics:` Bir önceki adımın çıktısı olan `metrics.csv`'ye ihtiyaç duyan ve grafikleri oluşturan adım.

## 🐳 Aşama 4: Konteynerleştirme (Docker)
**Hedef:** Profesörün makinesinde hiçbir Python/Snakemake kütüphanesi kurulu olmadan çalışabilmesini sağlayan izole ortamı inşa etmek.

*   [ ] **4.1. `Dockerfile` Yazılması:**
    *   `FROM mambaorg/micromamba` veya `miniforge3` gibi hızlı ve hafif bir base imaj seçilmesi.
    *   Bağımlılıkların Conda (veya Mamba) ile imaj içine kurulması (`snakemake`, `nanoplot`, `biopython`, `pandas`, `seaborn`).
    *   Çalışma dizininin (WORKDIR `/app`) ayarlanması.
*   [ ] **4.2. Docker Build & Pipeline Testi:**
    *   `docker build -t bio-pipeline .` ile imajın yaratılması.
    *   `docker run --rm -v $(pwd):/app bio-pipeline snakemake -c1` komutu ile projeyi izole bir şekilde baştan sona tetikleyip sonuçların host makineye çıkmasının test edilmesi.

## 📝 Aşama 5: Raporlama, Kullanım Kılavuzu ve İletişim
**Hedef:** Elde edilen çıktıları bir son kullanıcıya (Prof. Kılıç) anlaşılır şekilde iletmek ve projenin GitHub reposunu profesyonel seviyeye (README dahil) getirmek.

*   [ ] **5.1. Profesör İçin E-posta Taslağı (`email_draft.md`):**
    *   Profesöre hitap edilen, teknik (Docker, Pandas vb.) detaylarda boğmayan yönetici özeti.
    *   Pipeline'ın ürettiği `summary_statistics.txt` değerlerine atıfta bulunarak okuma uzunlukları ve kalite yeterliliği hakkında değerlendirme.
    *   "Alignment aşamasına geçilmeli mi?" sorusuna veriye dayalı argümantatif yanıt.
*   [ ] **5.2. `README.md` Dosyası:**
    *   Projenin ve pipeline'ın amacı.
    *   Kurulum adımları (Ön koşul: Sadece Docker).
    *   Kullanım: "Kendi FASTQ dosyanızı `data/` içine atıp şu Docker komutunu çalıştırın." tarzı kopyala-yapıştır net talimatlar.
*   [ ] **5.3. Kod Temizliği & Versiyonlama:**
    *   Bütün scriptlere açıklayıcı (DocString) temizliklerinin yapılması.
    *   GitHub'a `push` atılması.
