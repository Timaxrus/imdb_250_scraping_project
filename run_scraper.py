# run_scraper.py
from imdb_scraper import top_250_movies_list, get_all_movie_data
from config import URL, HEADERS
import concurrent.futures
import pandas as pd
import json
import os
import logging
from datetime import datetime

def main():
    print("Starting IMDb Top 250 Scraper")
    
    # Create data and logging directories if it doesn't exist
    os.makedirs('data', exist_ok=True)  
    os.makedirs('logs', exist_ok=True)  # <- ADD THIS LINE
    
    # Setup logging to use logs folder
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/scraper.log'),
            logging.StreamHandler()
        ]
    )  
    
    logging.info("Starting IMDb Top 250 Scraper")

    # Step 1: Get basic movie list
    movies_list = top_250_movies_list(URL, HEADERS)
    
    if movies_list:
        logging.info(f"Successfully extracted {len(movies_list)} movies")
    else:
        logging.error("Failed to extract movies data")
        return
    
    # Step 2: Get additional data for each movie
    movie_urls = [movie.get('imdb_url') for movie in movies_list]
    
    directors = []
    top_actors = []
    release_years = []
    certificates = []
    metascores = []
    budgets = []
    box_offices = [] 
    wins_nominations_list = []

    logging.info(f"Processing {len(movie_urls)} movies...")
    
    # Concurrent processing code
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        results = list(executor.map(get_all_movie_data, movie_urls))
        
    for director, actors, certs, meta, release, wins, budget, box_office in results:
        directors.append(director)
        top_actors.append(actors)
        certificates.append(certs)
        metascores.append(meta)
        release_years.append(release)
        wins_nominations_list.append(wins)
        budgets.append(budget)
        box_offices.append(box_office)
    
    # Step 3: Combine all data
    for i, movie in enumerate(movies_list):
        movie['director'] = directors[i] if i < len(directors) else None
        movie['top_actors'] = top_actors[i] if i < len(top_actors) else None
        movie['release_year'] = release_years[i] if i < len(release_years) else None
        movie['certificate'] = certificates[i] if i < len(certificates) else None
        movie['metascore'] = metascores[i] if i < len(metascores) else None
        movie['wins_nominations'] = wins_nominations_list[i] if i < len(wins_nominations_list) else None
        movie['budget'] = budgets[i] if i < len(budgets) else None
        movie['box_office'] = box_offices[i] if i < len(box_offices) else None
    
    # Step 4: Save results
    # Save as JSON
    with open(f'data/imdb_top_250_{datetime.now().strftime('%Y%m%d_%H%M')}.json', 'w', encoding='utf-8') as f:
        json.dump(movies_list, f, indent=4, ensure_ascii=False)
    
    # Save as CSV
    df = pd.DataFrame(movies_list)
    df.to_csv(f'data/imdb_top_250_{datetime.now().strftime('%Y%m%d_%H%M')}.csv', index=False, encoding='utf-8-sig')
    
    logging.info(f"Data saved to data/imdb_top_250_{datetime.now().strftime('%Y%m%d_%H%M')}.json and data/imdb_top_250_{datetime.now().strftime('%Y%m%d_%H%M')}.csv")
    logging.info("Scraping completed successfully!")

if __name__ == "__main__":
    main()