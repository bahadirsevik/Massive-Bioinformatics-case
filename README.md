# Massive-Bioinformatics-case

Bu proje, long-read sequencing (uzun okuma) dizilimi verilerinin Kalite Kontrolünü (QC) yapmak, veri özelliklerini izlemek (GC oranı, uzunluk, ortalama Q skoru) ve sonuçları görselleştirmek üzere baştan sona kurgulanmış tekrarlanabilir bir **Snakemake** + **Docker** otomasyonudur.

## 🛠️ Teknolojiler
- **Orkestrasyon:** Snakemake
- **Çevre İzolasyonu:** Docker (Micromamba imajı üzerinden hızlı conda kurumu)
- **Veri Analizi:** Python (Biopython, Pandas)
- **Görselleştirme:** Seaborn, Matplotlib
- **Long-read QC Engine:** NanoPlot

## 📂 Dizin Yapısı
```
.
├── data/                   # Girdi verisi (.fastq) buraya konulmalı (Script ile de üretilebilir)
├── scripts/                # Python data processing ve visualizer kodları
├── results/                # (Pipeline çalışınca oluşur) Hesaplamalar ve grafikler
├── Snakefile               # Snakemake pipeline adımları
├── environment.yml         # Conda bağımlılık listesi
├── Dockerfile              # %100 tekrarlanabilir Docker izolasyon kabuğu
├── email_draft.md          # İletişim raporu örneği
└── README.md
```

## 🚀 Sistemi Kullanma Talimatları

Bu pipeline "benim bilgisayarımda çalışıyor" bahanesini yok etmek için tasarlandı. Bilgisayarınızda (veya bulut sunucunuzda) hiçbir Python, kütüphane veya QC aracı yüklü olmasına gerek yoktur; **sadece Docker yüklü olması yeterlidir**.

### 1. Hazırlık ve Dummy Data (İsteğe Bağlı)
Kendi FASTQ dosyanızı `data/sample_reads.fastq` olacak şekilde kopyalayabilirsiniz.
Test etmek için örnek veri yoksa projede dummy veri oluşturucu script bulunur. Eğer python'unuz varsa kök dizinde şu komutu çalıştırarak bir örnek veri üretebilirsiniz:
```bash
python scripts/generate_dummy.py
```

### 2. Docker İmajını İnşa Etme
Test ortamını kurmak için terminalden (Powershell/CMD/Bash) aşağıdaki komutu çalıştırın. (Bu işlem bağımlılıkları indirip izole ettiği için birkaç dakika sürebilir):
```bash
docker build -t bio-pipeline .
```

### 3. Pipeline'ı Tetikleme
Güçlü Snakemake orkestrasyonunu başlatmak için tek satırlık şu komutu çalıştırın:
```bash
docker run --rm -v ${PWD}:/app bio-pipeline
```
*(Not: Windows Powershell ortamında hata alırsanız `${PWD}` kısmını `${PWD}.Path` ile veya doğrudan statik mutlak yol ile değiştirin: `docker run --rm -v C:\Mutlak\Yol:/app bio-pipeline`)*

Snakemake pipeline'ı kendi kendine şunları yapacaktır:
1. `NanoPlot` engine ile kapsamlı QC süreçlerini işletir.
2. `scripts/calculate_metrics.py` ile `FastqGeneralIterator` üzerinden RAM dostu şekilde okuma uzunluklarını, GC içeriklerini hızla hesaplar ve `.csv`'ye yazar.
3. `scripts/plot_metrics.py` ile elde edilen bu CSV'yi okuyup Seaborn tabanlı istatistiksel grafikler ve bir rapor çıkarır.

### 4. Sonuçlar
Tetikleme sonrası oluşan `results/` klasörüne gidin:
- `metrics.csv`: Ham istatistik dataframe yapısı.
- `nanoplot/`: İçinde `NanoPlot-report.html` barındıran zengin arayüz.
- `plots_and_summary/`: GC dağılımı, Okuma uzunluğu grafiği, Kalite grafiği ve tüm istatistiklerin bulunduğu net bir `summary_statistics.txt` raporu.
