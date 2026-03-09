import argparse
import os
import pandas as pd
from Bio.SeqIO.QualityIO import FastqGeneralIterator

def calculate_gc_content(sequence: str) -> float:
    """Calculate GC content of a DNA sequence."""
    if not sequence:
        return 0.0
    sequence = sequence.upper()
    g_count = sequence.count('G')
    c_count = sequence.count('C')
    return ((g_count + c_count) / len(sequence)) * 100.0

def calculate_mean_quality(quality_string: str) -> float:
    """
    Calculate the arithmetic mean of Phred quality scores.
    
    Note: Mathematically, Phred scores are logarithmic (-10 * log10(P)).
    Strictly speaking, one should convert them to error probabilities, 
    average the probabilities, and convert back. However, for quick QC
    summaries and to match standard simple visualizer behaviors, 
    an arithmetic mean is commonly used and requested here.
    """
    if not quality_string:
        return 0.0
    # Phred+33 decoding
    scores = [ord(char) - 33 for char in quality_string]
    return sum(scores) / len(scores)

def process_fastq(input_fastq: str, output_csv: str):
    """
    Process a fastq file and output read metrics to a CSV file.
    Using FastqGeneralIterator for high performance on long-read data,
    as it avoids creating complex SeqRecord objects in memory.
    """
    print(f"Processing FASTQ file: {input_fastq}")
    
    if not os.path.exists(input_fastq):
        raise FileNotFoundError(f"Input file not found: {input_fastq}")
    
    metrics = []
    
    # Handle both gzipped and plain fastq files
    open_func = open
    if input_fastq.endswith('.gz'):
        import gzip
        open_func = gzip.open
        mode = 'rt'
    else:
        mode = 'r'
        
    with open_func(input_fastq, mode) as f:
        # FastqGeneralIterator returns (title, sequence, quality)
        for title, seq, qual in FastqGeneralIterator(f):
            read_id = title.split()[0] # get just the ID part, drop description
            
            length = len(seq)
            gc_content = calculate_gc_content(seq)
            mean_q = calculate_mean_quality(qual)
            
            metrics.append({
                "ReadID": read_id,
                "Length": length,
                "GC_Percent": gc_content,
                "Mean_Quality": mean_q
            })
            
    if not metrics:
        raise ValueError("No sequences found in the FASTQ file.")
        
    df = pd.DataFrame(metrics)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(os.path.abspath(output_csv)), exist_ok=True)
    
    df.to_csv(output_csv, index=False)
    print(f"Successfully processed {len(df)} reads. Metrics saved to {output_csv}")

def main():
    parser = argparse.ArgumentParser(description="Calculate metrics for long-read FASTQ data.")
    parser.add_argument("-i", "--input", required=True, help="Input FASTQ file path")
    parser.add_argument("-o", "--output", required=True, help="Output CSV file path")
    
    args = parser.parse_args()
    
    process_fastq(args.input, args.output)

if __name__ == "__main__":
    main()
