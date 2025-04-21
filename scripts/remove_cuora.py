# this is when had to realign the dna sequences the species Cuora was causing issues for the alignment. 
from Bio import SeqIO
#these lines defines the input and output files
input_file = "FcC_supermatrix.fas"
output_file = "cleaned_supermatrix.fas"
exclude_genus = "Cuora"  # Genus to exclude

# Reads the supermatrix FASTA file
records = list(SeqIO.parse(input_file, "fasta"))

# Filter sequences to exclude the specified genus
#this is important since we don't want cuora
filtered_records = [
    record for record in records if exclude_genus not in record.id
]
# Keep only sequences that do not belong to the genus Cuora
# Write the filtered sequences to a new FASTA file
with open(output_file, "w") as f:
    SeqIO.write(filtered_records, f, "fasta")
# print statements for the outputs
print(f"Sequences with genus '{exclude_genus}' excluded.")
print(f"Cleaned supermatrix saved to '{output_file}'")



