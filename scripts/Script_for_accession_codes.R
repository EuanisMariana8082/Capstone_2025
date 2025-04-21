# 4/16/2025 updated code 
# accession code 
# this is the code that gets the accession codes and creates .fas files for each gene
# Define the file path - use the cleaned dataset
file_path <- "cleaned_pnas_dataset.csv"
# Read the CSV file
data <- read.csv(file_path, stringsAsFactors = FALSE)
# Check the column names to identify the correct columns
print(colnames(data))
# Extract gene columns (all columns except 'Individual' and 'collection')
gene_columns <- colnames(data)[3:length(colnames(data))]
# Create and save files for each gene
for (gene in gene_columns) {
  gene_data <- data[, gene]
  
  # Prepare the content for the .fas file
  fas_content <- paste0("> ", gene, "\n")
  for (i in 1:nrow(data)) {
    fas_content <- paste0(fas_content, gene_data[i], "\n")
  }
  
  # Create the file name based on the gene name
  file_name <- paste0(gene, ".fas")
  
  # Write the .fas file
  write(fas_content, file = file_name)
  
  # Print a message to indicate completion for each gene
  cat("Data saved to", file_name, "\n")
}
