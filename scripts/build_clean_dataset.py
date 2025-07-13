## Imports
import os
from src.data_loader import load_crime_data
from src.cleaner import clean_crime_data


## Loads
# Paths
input_path = 'data/crime_raw.csv'
output_path = 'data/crime_filtered.csv'

# Load and filter
print("Loading raw data...")
df_raw = load_crime_data(input_path)


## Main
# Clean and structure
print("Cleaning data...")
df_cleaned = clean_crime_data(df_raw)

# Ensure output folder exists
os.makedirs("data", exist_ok=True)

# Save cleaned dataset
df_cleaned.to_csv(output_path, index=False)
print(f"Cleaned dataset saved to {output_path}")
