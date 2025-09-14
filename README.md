**1. Project summary**

# IMDb Top 250 Movies Scraper 🎬

A Python project that automatically collects and analyzes data from IMDb's Top 250 movies.

## What It Does

- **Scrapes** movie data from IMDb Top 250 list
- **Cleans** and processes the data
- **Creates** charts and visualizations
- **Runs automatically** on a schedule

## Quick Start

### 1. Install Requirements
```bash
pip install -r requirements.txt```


**2. Run the Project**

``` bash
# Run everything at once (or you can run each file one by one if needed)
python main.py```


# Run the scheduler (stays running in background)
python scheduler.py

# Press Ctrl+C to stop when done

**3. Automatic scheduling**

# Run the scheduler (stays running in background)
python scheduler.py

# Press Ctrl+C to stop when done

**Project structure**

imdb_scraping_project/
├── main.py                 # Main controller
├── run_scraper.py        # Scraping script
├── data_cleaning.py        # Data cleaning
├── imdb_analysis.py        # Analysis & charts
├── scheduler.py            # Auto-scheduler
├── requirements.txt        # Python packages
│
├── data/                   # CSV/JSON files (auto-created)
├── images/                 # Charts (auto-created)
├── results/                # Analysis results (auto-created)
└── logs/                   # Log files (auto-created)

Data Collected

- For each movie, we get:

- Title, rating, and votes

- Director and main actors

- Release year and runtime

- Budget and box office

- Awards and genres

Charts Created

- Movie runtime distribution

- Most common genres

- Top actors appearances

- Rating vs box office

- Highest-grossing movies

- Award-winning films


Automation

The scheduler runs:

Daily at 4 PM GMT

Weekly on Sundays at 2 AM

To change times, edit scheduler.py.

Requirements

- Python 3.8+

- Packages in requirements.txt

Notes

- First run creates needed folders automatically

- Check logs/ folder if anything goes wrong

- Press Ctrl+C to stop the scheduler
