# main.py
import subprocess
import sys
import os
from datetime import datetime

def run_scraper():
    """Run the IMDb scraper"""
    print("Starting IMDb Scraper...")
    try:
        subprocess.run([sys.executable, "run_scraper.py"], check=True)
        print("Scraping completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Scraping failed: {e}")
        return False

def run_data_cleaning():
    """Run the data cleaning process"""
    print("Starting Data Cleaning...")
    try:
        # Run the data cleaning script
        subprocess.run([sys.executable, "data_cleaning.py"], check=True)
        print("Data cleaning completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Data cleaning failed: {e}")
        return False

def run_analysis():
    """Run the data analysis"""
    print("Starting Data Analysis...")
    try:
        # Run the analysis script
        subprocess.run([sys.executable, "imdb_analysis.py"], check=True)
        print("Analysis completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Analysis failed: {e}")
        return False

def find_latest_clean_data():
    """Find the latest cleaned CSV file for analysis"""
    import glob
    clean_files = glob.glob(os.path.join('data', 'clean_top_250_*.csv'))
    if not clean_files:
        return None
    return max(clean_files, key=os.path.getctime)

def main():
    """Main function to run the entire pipeline"""
    print("=" * 50)
    print("IMDb Top 250 Automation Pipeline")
    print("=" * 50)
    
    # Create necessary directories
    os.makedirs('data', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    os.makedirs('results', exist_ok=True)  # For analysis outputs
    os.makedirs('images', exist_ok=True)   # NEW: For visualization images
    
    # Run scraping
    scraping_success = run_scraper()
    
    if scraping_success:
        # Run data cleaning
        cleaning_success = run_data_cleaning()
        
        if cleaning_success:
            # Run analysis
            run_analysis()
    
    print("=" * 50)
    print("Pipeline completed!")
    print("=" * 50)

if __name__ == "__main__":
    main()