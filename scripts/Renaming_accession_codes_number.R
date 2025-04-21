# Define the base directory where the folder should be created
base_directory <- "C:/Users/Rushe/Desktop/Bioinformatics_cap_2025"
folder_name <- "number_accession_codes"
folder_path <- file.path(base_directory, folder_name)

# step 1: Create the folder if it doesn't exist
if (!dir.exists(folder_path)) {
  dir.create(folder_path)
}

# Define the file path for the cleaned dataset
file_path <- "cleaned_pnas_dataset.csv"
data <- read.csv(file_path, stringsAsFactors = FALSE)

# Define the mapping of old FASTA names to new .txt file names
new_names <- c(
  "AHR" = "958268.txt",
  "AIING" = "963935.txt",
  "BDNF" = "959071.txt",
  "BMP2" = "959337.txt",
  "HMGB2" = "965141.txt",
  "HNFL" = "959879.txt",
  "NB22519" = "960290.txt",
  "PAX1P1" = "961111.txt",
  "PSMCI" = "964649.txt",
  "R35" = "961185.txt",
  "RAG.1" = "961681.txt",
  "TB01" = "962105.txt",
  "TB29" = "962592.txt",
  "TB73" = "963043.txt",
  "ZFHX1B" = "963399.txt"
)

# Extract gene columns (all columns except 'Individual' and 'collection')
gene_columns <- colnames(data)[3:length(colnames(data))]

# Create and save renamed .txt files inside the folder
for (gene in gene_columns) {
  gene_data <- data[, gene]
  
  # Prepare the content for the file
  txt_content <- paste0("> ", gene, "\n")
  for (i in 1:nrow(data)) {
    txt_content <- paste0(txt_content, gene_data[i], "\n")
  }
  
  # Get the new filename from mapping (fallback to original name if missing)
  file_name <- ifelse(gene %in% names(new_names), new_names[gene], paste0(gene, ".txt"))
  
  # save the file inside the `number_accession_codes` folder
  file_path <- file.path(folder_path, file_name)
  write(txt_content, file = file_path)
  
  # Print a message to indicate completion
  cat("Data saved to", file_path, "\n")
}

print("all files successfully renamed and saved in 'number_accession_codes' folder!")
