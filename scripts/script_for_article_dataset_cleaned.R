# start be creating a folder where you will keep everything for this so it is easy to keep track of.
#download the dataset. Make sure that is in your folder so this script will run.
# If you don't have the packages make sure to install them on R studio so this runs properly.
# Load necessary libraries
library(tidyverse)
library(readr)
library(dplyr)
library(ggplot2)
library(tidyr)
# I am usually bad at this. I noticed that I had the file path set to my computer.This should be fixed now.
# Use relative path for input
dataset <- read_csv("pnas.2012215118.sd01.csv")
#The reason why this data set needed to be cleaned up.
# Convert "-" to NA
dataset <- dataset %>%
  mutate(across(everything(), ~na_if(., "-")))
# we need to know what the missing values are.
# Now check for missing values
missing_values <- dataset %>% 
  filter_all(any_vars(is.na(.)))
print(missing_values)
print(paste("Number of rows with missing values:", nrow(missing_values)))
# we need to fill or just remove the values.
# Remove rows with any missing values
cleaned_dataset <- dataset %>% drop_na()
# we need to check that there are no empty values.
# Check for any remaining missing values after cleaning
missing_values_after_cleaning <- cleaned_dataset %>% 
  filter_all(any_vars(is.na(.)))
print(missing_values_after_cleaning)
#double check to see what is removed
# Print how many rows were removed
print(paste("Original dataset rows:", nrow(dataset)))
print(paste("Cleaned dataset rows:", nrow(cleaned_dataset)))
print(paste("Rows removed:", nrow(dataset) - nrow(cleaned_dataset)))

# Save the cleaned dataset (with all dash symbols converted to NA and then removed) to a new CSV file
write_csv(cleaned_dataset, "cleaned_pnas_dataset.csv")
