## Imports
import pandas as pd


## Functions
def load_crime_data(filepath: str) -> pd.DataFrame:
    """
    Load csv and filter by year: 2020–2022
    """
    df = pd.read_csv(filepath, parse_dates=['Date'])
    df = df[(df['Date'].dt.year >= 2020) & (df['Date'].dt.year <= 2022)]
    return df
