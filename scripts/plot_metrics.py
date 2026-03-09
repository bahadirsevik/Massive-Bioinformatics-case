import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set premium seaborn aesthetic
sns.set_theme(style="whitegrid", context="paper")

def calculate_n50(lengths: iter) -> int:
    """
    Calculate the N50 metric for sequence lengths.
    N50 is defined as the sequence length such that 50% of the entire 
    assembly/readset is contained in sequences equal to or larger than this length.
    """
    sorted_lengths = sorted(lengths, reverse=True)
    total_length = sum(sorted_lengths)
    half_length = total_length / 2.0
    
    running_sum = 0
    for length in sorted_lengths:
        running_sum += length
        if running_sum >= half_length:
            return length
    return 0

def create_plots(df: pd.DataFrame, out_dir: str):
    """
    Create static visualizations for the quality metrics.
    """
    print("Generating plots...")
    
    # 1. GC Content Plot
    plt.figure(figsize=(10, 6))
    sns.histplot(df['GC_Percent'], bins=50, kde=True, color="mediumseagreen")
    plt.title('GC Content Distribution', fontsize=16, fontweight='bold')
    plt.xlabel('GC Content (%)')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'gc_distribution.png'), dpi=300)
    plt.close()
    
    # 2. Read Length Plot
    plt.figure(figsize=(10, 6))
    # Long read lengths are often skewed, so we use log_scale on x-axis
    ax = sns.histplot(df['Length'], bins=50, kde=True, color="dodgerblue", log_scale=True)
    plt.title('Read Length Distribution (Log Scale)', fontsize=16, fontweight='bold')
    plt.xlabel('Length (bp)')
    plt.ylabel('Frequency')
    # Formatting x-axis to show regular numbers instead of 10^x
    ax.xaxis.set_major_formatter(plt.ScalarFormatter())
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'length_distribution.png'), dpi=300)
    plt.close()
    
    # 3. Mean Quality Plot
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Mean_Quality'], bins=30, kde=True, color="coral")
    plt.title('Mean Read Quality Score Distribution', fontsize=16, fontweight='bold')
    plt.xlabel('Mean Phred Score')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'quality_distribution.png'), dpi=300)
    plt.close()


def create_summary_report(df: pd.DataFrame, out_file: str):
    """
    Calculate and save summary statistics to a text file.
    """
    print("Generating summary report...")
    
    # Basic Stats
    total_reads = len(df)
    total_bases = df['Length'].sum()
    
    mean_length = df['Length'].mean()
    median_length = df['Length'].median()
    max_length = df['Length'].max()
    min_length = df['Length'].min()
    n50_length = calculate_n50(df['Length'])
    
    mean_gc = df['GC_Percent'].mean()
    mean_q = df['Mean_Quality'].mean()
    
    report_content = f"""==================================================
LONG-READ SEQUENCING QC REPORT
==================================================

OVERALL STATISTICS
--------------------------------------------------
Total Reads:           {total_reads:,}
Total Yield (bases):   {total_bases:,} bp

READ LENGTH METRICS
--------------------------------------------------
Min Length:            {min_length:,} bp
Max Length:            {max_length:,} bp
Mean Length:           {mean_length:,.2f} bp
Median Length:         {median_length:,} bp
N50:                   {n50_length:,} bp

QUALITY METRICS
--------------------------------------------------
Mean GC Content:       {mean_gc:.2f}%
Overall Mean Q-Score:  {mean_q:.2f}
==================================================
"""
    
    with open(out_file, 'w') as f:
        f.write(report_content)
        
    print(f"Summary saved to {out_file}")

def main():
    parser = argparse.ArgumentParser(description="Plot metrics and generate summary report.")
    parser.add_argument("-i", "--input", required=True, help="Input CSV file from calculate_metrics.py")
    parser.add_argument("-o", "--outdir", required=True, help="Output directory for plots and summary")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        raise FileNotFoundError(f"Input file not found: {args.input}")
        
    os.makedirs(args.outdir, exist_ok=True)
    
    df = pd.read_csv(args.input)
    
    create_plots(df, args.outdir)
    
    summary_file = os.path.join(args.outdir, 'summary_statistics.txt')
    create_summary_report(df, summary_file)
    
    print("Visualization and reporting complete.")


if __name__ == "__main__":
    main()
