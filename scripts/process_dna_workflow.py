# making sure that everything is imported so that there are no errors
import os
import subprocess
import re
import glob
from Bio import SeqIO  # Import Biopython for handling FASTA files

# Defining the  directories
folder_path = r"C:\Users\Rushe\Desktop\Bioinformatics_cap_2025\Renamed_DNA_Sequences"
filtered_dir = os.path.join(folder_path, "Filtered_DNA_Sequences")
aligned_dir = os.path.join(folder_path, "Aligned_Sequences")

# Ensure directories exist. I had issues a new times this is why it was important for me to check that they do exist.
os.makedirs(filtered_dir, exist_ok=True)
os.makedirs(aligned_dir, exist_ok=True)

def filter_and_clean(input_fasta, output_fasta, max_n_percentage=20, invalid_keywords=None):
    """Filters sequences based on missing data and invalid species names."""
 # Default unwanted species names

    if invalid_keywords is None:
        invalid_keywords = ['sp.voucher', 'sp.sth'] 

    retained_sequences = 0

    with open(output_fasta, "w") as output_handle:
        for record in SeqIO.parse(input_fasta, "fasta"):
            species_name = " ".join(record.description.split()[:2])  # Extract Genus + Species

            # Skips any of the unwanted species names
            if any(keyword in species_name for keyword in invalid_keywords):
                continue

            # Remove sequences with excessive missing data
            n_percentage = (record.seq.count('N') / len(record)) * 100
            if n_percentage > max_n_percentage:
                continue

            record.id = species_name
            record.description = ""

            SeqIO.write(record, output_handle, "fasta")
            retained_sequences += 1

    print(f" Processed {retained_sequences} sequences. Saved to: {output_fasta}")

def run_mafft(input_file, output_file):
    """Runs MAFFT alignment."""
    mafft_cmd = rf'"C:\Users\Rushe\Downloads\mafft-7.526-win64-signed\mafft-win\mafft.bat" --auto --anysymbol {input_file} > {output_file}'
    result = subprocess.run(mafft_cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f" MAFFT failed: {result.stderr}")

def run_bmge(input_file, output_file):
    """Runs BMGE to refine alignments."""
    bmge_cmd = rf'docker run -v C:\Users\Rushe\Desktop\Bioinformatics_cap_2025:/data quay.io/biocontainers/bmge:1.12--hdfd78af_1 /usr/local/bin/bmge -i /data/Renamed_DNA_Sequences/{os.path.basename(input_file)} -t DNA -of /data/{os.path.basename(output_file)}'
    
    try:
        result = subprocess.run(bmge_cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f" BMGE failed: {result.stderr}")
    except Exception as e:
        print(f"BMGE execution error: {e}")

# Process all FASTA files
file_paths = glob.glob(os.path.join(folder_path, "*.fasta"))
for input_file in file_paths:
    filtered_file = os.path.join(filtered_dir, os.path.basename(input_file).replace(".fasta", "_filtered.fasta"))
    aligned_file = os.path.join(aligned_dir, os.path.basename(filtered_file).replace("_filtered.fasta", "_aligned.fasta"))
    cleaned_aligned_file = os.path.join(aligned_dir, os.path.basename(filtered_file).replace("_filtered.fasta", "_aligned_cleaned.fasta"))

    filter_and_clean(input_file, filtered_file)
    run_mafft(filtered_file, aligned_file)
    run_bmge(aligned_file, cleaned_aligned_file)

print("\n All sequences filtered, aligned, and cleaned successfully! ")


