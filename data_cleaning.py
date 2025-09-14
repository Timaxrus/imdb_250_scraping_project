# data_cleaning.py
import pandas as pd
import numpy as np
from datetime import datetime
import glob
import os

def find_latest_csv(directory="data"):
    """Find the latest scraped CSV file"""
    csv_files = glob.glob(os.path.join(directory, "imdb_top_250_*.csv"))
    if not csv_files:
        raise FileNotFoundError("No CSV files found in data directory")
    return max(csv_files, key=os.path.getctime)

# Function to convert PT1H30M format to total minutes
def convert_runtime(runtime_str):
    try:
        # Removing the 'PT' prefix
        runtime_str = runtime_str.replace('PT', '')
        # Checking if 'H' and 'M' are present
        if 'H' in runtime_str and 'M' in runtime_str:
            hours = int(runtime_str.split('H')[0])
            minutes = int(runtime_str.split('H')[1].replace('M', ''))
            return hours * 60 + minutes
        elif 'H' in runtime_str:
            hours = int(runtime_str.replace('H', ''))
            return hours * 60
        elif 'M' in runtime_str:
            minutes = int(runtime_str.replace('M', ''))
            return minutes
        else:
            return np.nan # Return NaN if format is unexpected
    except:
        return np.nan # Return NaN if conversion fails
    
# Function to clean currency strings and convert to float (in millions)
def clean_currency(currency_str):
    if pd.isna(currency_str): # Check if value is NaN
        return np.nan
    try:
        # Remove any text in parentheses like '(estimated)'
        clean_str = currency_str.split(' (')[0]
        # Remove common currency symbols and commas
        clean_str = clean_str.replace('$', '').replace('€', '').replace('¥', '').replace('₹', '').replace('£', '').replace('₩', '').replace('DEM', '').replace('ITL', '').replace('DKK', '').replace(',', '').replace(' ', '')
        # Convert to float. If empty after cleaning, return NaN.
        return round(float(clean_str) / 1_000_000, 2) if clean_str != '' else np.nan # Convert to millions
    except:
        return np.nan
    
# Function to extract wins and nominations from the string
def extract_awards(award_str):
    try:
        # Split the string by 'wins' and 'nominations'
        parts = award_str.split(' wins & ')
        wins = int(parts[0])
        nominations = int(parts[1].split(' nominations')[0])
        return wins, nominations
    except:
        # Return NaN if the format is unexpected or value is missing
        return np.nan, np.nan

def clean_data():
    """Main data cleaning function"""
    # Load the latest CSV
    latest_csv = find_latest_csv()
    print(f"Cleaning data from: {latest_csv}")
    df = pd.read_csv(latest_csv)
    
    # [COPY ALL YOUR CLEANING LOGIC FROM THE NOTEBOOK HERE]

    # Apply the conversion function to the 'run_time' column
    df['run_time_minutes'] = df['run_time'].apply(convert_runtime)

    # Drop the original 'run_time' column as we have the new clean one
    df.drop('run_time', axis=1, inplace=True)

    # Apply the cleaning function to 'budget' and 'box_office'
    df['budget_million'] = df['budget'].apply(clean_currency)
    df['box_office_million'] = df['box_office'].apply(clean_currency)

    # Drop the original 'box_office' column only. We keep 'budget' original column for now as it contains different currency symbols.
    df.drop(['box_office'], axis=1, inplace=True)

    # Apply the function and create new columns
    df[['award_wins', 'award_nominations']] = df['wins_nominations'].apply(
        lambda x: pd.Series(extract_awards(x))
    )

    # Drop the original 'wins_nominations' column
    df.drop('wins_nominations', axis=1, inplace=True)

    # Remove the square brackets and quotes, then strip extra spaces
    df['top_actors'] = (df['top_actors']
                        .str.strip('[]')  # Remove the outer brackets
                        .str.replace("'", "")  # Remove the single quotes
                        .str.replace('"', '')  # Remove double quotes (if any)
                        .str.strip())  # Remove any leading/trailing spaces
    
    
    
    # Save cleaned data
    output_path = f'data/clean_top_250_{datetime.now().strftime("%Y%m%d_%H%M")}.csv'
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to: {output_path}")
    return output_path

if __name__ == "__main__":
    clean_data()