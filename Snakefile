"""
Bioinformatics Pipeline for Minimal QC and Reporting
Targets: Long-read FASTQ sequence evaluation.
"""

rule all:
    input:
        "results/nanoplot/NanoPlot-report.html",
        "results/metrics.csv",
        "results/plots_and_summary/summary_statistics.txt"

rule run_nanoplot:
    input:
        fastq = "data/barcode77.fastq.gz"
    output:
        report = "results/nanoplot/NanoPlot-report.html"
    log:
        "results/nanoplot/nanoplot.log"
    shell:
        """
        NanoPlot --fastq {input.fastq} -o results/nanoplot > {log} 2>&1
        """

rule calculate_metrics:
    input:
        fastq = "data/barcode77.fastq.gz"
    output:
        csv = "results/metrics.csv"
    shell:
        """
        python scripts/calculate_metrics.py -i {input.fastq} -o {output.csv}
        """

rule plot_metrics:
    input:
        csv = "results/metrics.csv"
    output:
        summary = "results/plots_and_summary/summary_statistics.txt",
        plot_gc = "results/plots_and_summary/gc_distribution.png",
        plot_len = "results/plots_and_summary/length_distribution.png",
        plot_qual = "results/plots_and_summary/quality_distribution.png"
    params:
        outdir = "results/plots_and_summary"
    shell:
        """
        python scripts/plot_metrics.py -i {input.csv} -o {params.outdir}
        """
