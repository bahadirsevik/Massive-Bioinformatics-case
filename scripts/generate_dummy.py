import random
import gzip
from pathlib import Path

def generate_random_sequence(length):
    return ''.join(random.choices(['A', 'C', 'G', 'T'], k=length))

def generate_random_quality(length, mean_quality):
    # Simulated Phred scores from expected mean quality
    # Character code = Quality + 33
    qualities = [chr(int(max(0, min(random.gauss(mean_quality, 2), 40))) + 33) for _ in range(length)]
    return ''.join(qualities)

def create_dumb_fastq(filepath, num_reads=1000):
    print(f"Generating dummy FASTQ at {filepath}...")
    
    with open(filepath, 'w') as f:
        for i in range(num_reads):
            # Simulate long-read lengths (e.g. 500bp to 30,000bp, right-skewed)
            # using a gamma distribution or just uniform
            length = int(random.gammavariate(alpha=2, beta=3000))
            if length < 500:
                length = 500
                
            # Simulate Nanopore typical read qualities (around 10)
            mean_q = random.uniform(8, 14)
            
            # GC Content (approx 40-60%)
            seq = generate_random_sequence(length)
            qual = generate_random_quality(length, mean_q)
            
            f.write(f"@dummy_read_{i+1}_len_{length}\n")
            f.write(f"{seq}\n")
            f.write("+\n")
            f.write(f"{qual}\n")
            
    print("Done!")

if __name__ == "__main__":
    out_dir = Path("data")
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / "sample_reads.fastq"
    create_dumb_fastq(out_file, num_reads=500)
