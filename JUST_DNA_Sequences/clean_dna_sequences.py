from Bio import SeqIO
import os
import re
import glob
import shutil

# Define the base folder where everything will be handled
base_dir = os.path.dirname(os.path.abspath(__file__))  # The directory where the script is located
data_dir = os.path.join(base_dir, "DNA_Cleanup")
output_dir = os.path.join(data_dir, "cleaned_sequences")

# Create directories if they don't exist
os.makedirs(data_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

# Copy FASTA files from the original folder (adjust this path)
original_folder = "C:\\Users\\Rushe\\Desktop\\Bioinformatics_cap_2025\\JUST_DNA_Sequences"
file_paths = glob.glob(os.path.join(original_folder, "*.fasta"))

for file_path in file_paths:
    shutil.copy(file_path, data_dir)  # Copy each file into DNA_Cleanup

def process_file(file_path, output_dir):
    species_seen = set()
    cleaned_sequences = []
    gene_name = os.path.splitext(os.path.basename(file_path))[0]  # Extract gene name from filename

    for record in SeqIO.parse(file_path, "fasta"):
        description = record.description
        # Remove accession numbers and unnecessary identifiers
        description = re.sub(r'^[> ]*([A-Z]{2,}\d+|\d+[A-Z]{2,}\d*|\S+\.\d+)\s*', '', description)
        parts = description.split()
        genus_species = None

        # Identify valid binomial names (Genus + Species)
        for i in range(len(parts) - 1):
            candidate_genus = parts[i]
            candidate_species = parts[i+1]

            if "sp." in candidate_species:  # Skip "sp." entries
                continue

            # Skip if names look like IDs or numbers
            if candidate_genus.replace('.', '').isdigit() or candidate_species.replace('.', '').isdigit():
                continue

            if candidate_species == candidate_genus:  # Skip if species == genus (invalid binomial)
                continue

            # Found a valid binomial name
            genus_species = f"{candidate_genus} {candidate_species}"
            break

        if genus_species is None:
            print(f"Skipped: No valid binomial found in {record.id}")
            continue  

        # Ensure unique species per file
        if genus_species not in species_seen:
            species_seen.add(genus_species)
            record.id = genus_species
            record.description = ""  # Remove redundant description
            cleaned_sequences.append(record)

    # Save cleaned sequences
    output_file = os.path.join(output_dir, f"{gene_name}_cleaned.fasta")
    SeqIO.write(cleaned_sequences, output_file, "fasta")
    print(f"Processed {file_path} and saved to {output_file}")

# Process all copied FASTA files in "DNA_Cleanup"
copied_files = glob.glob(os.path.join(data_dir, "*.fasta"))
for file_path in copied_files:
    process_file(file_path, output_dir)

print("\n✅ Processing complete! All cleaned sequences are saved in:", output_dir)