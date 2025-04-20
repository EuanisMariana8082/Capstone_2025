from Bio import SeqIO

input_file = "FcC_supermatrix.fas"
output_file = "cleaned_supermatrix.fas"
exclude_genus = "Cuora"  # Genus to exclude

# Read the supermatrix FASTA file
records = list(SeqIO.parse(input_file, "fasta"))

# Filter sequences to exclude the specified genus
filtered_records = [
    record for record in records if exclude_genus not in record.id
]

# Write the filtered sequences to a new FASTA file
with open(output_file, "w") as f:
    SeqIO.write(filtered_records, f, "fasta")

print(f"Sequences with genus '{exclude_genus}' excluded.")
print(f"Cleaned supermatrix saved to '{output_file}'")



