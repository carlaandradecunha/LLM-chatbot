## Imports
import pandas as pd

## Functions
def clean_crime_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and prepare crime data, preserving relevant columns and enabling analysis.
    """
    # Select only relevant columns
    columns_to_keep = [
        'Date',
        'Primary Type',
        'District',
        'Ward',
        'Community Area',
        'Arrest',
        'Domestic',
        'Year'
    ]
    df = df[columns_to_keep].copy()

    # Rename columns to snake_case
    df = df.rename(columns={
        'Date': 'date',
        'Primary Type': 'primary_type',
        'District': 'district',
        'Ward': 'ward',
        'Community Area': 'community_area',
        'Arrest': 'arrest',
        'Domestic': 'domestic',
        'Year': 'year'
    })

    # Normalize text columns
    df['primary_type'] = df['primary_type'].astype(str).str.strip().str.lower()

    # Convert booleans
    df['arrest'] = df['arrest'].astype(bool)
    df['domestic'] = df['domestic'].astype(bool)

    # Remove rows with missing key data
    df = df.dropna(subset=['date', 'primary_type', 'community_area', 'ward', 'district'])

    return df
