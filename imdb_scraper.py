# imdb_scraper.py
# Data Scraping & Interaction
import requests
from bs4 import BeautifulSoup
import json
import concurrent.futures
import time
import re
import random

# Data Wrangling & Analysis
import pandas as pd
import numpy as np

# Data Visualization
import matplotlib.pyplot as plt
import seaborn as sns

from config import URL, HEADERS

# --- YOUR ORIGINAL FUNCTIONS (NO CHANGES) ---

def top_250_movies_list(url, headers):
    # Send request to the main page
    response = requests.get(url, headers=headers, timeout=10)

    # Check if request was successful
    if response.status_code != 200:
        print(f"Failed to fetch page. Status code: {response.status_code}")
        return None  # Return None instead of exit()

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the script tag containing JSON-LD data
    script_tag = soup.find('script', type='application/ld+json')

    # Check if we found the script tag
    if not script_tag:
        print("No JSON-LD data found")
        return None  # Return None instead of exit()

    # Parse the JSON data
    try:
        data = json.loads(script_tag.string)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON data: {e}")
        return None

    # Extract the movie list
    movies = data['itemListElement']
    basic_data = []

    for movie in movies:
        item = movie['item']
        
        # Fix the genre logic
        genre_value = item.get('genre', None)
        if isinstance(genre_value, list):
            formatted_genre = ', '.join(genre_value)
        else:
            formatted_genre = genre_value
        
        basic_data.append({
            'title': item.get('name', None),
            'id': item.get('url', '').removeprefix('https://www.imdb.com') if item.get('url') else None,
            'imdb_rating': item.get('aggregateRating', {}).get('ratingValue', None),
            'number_of_votes': item.get('aggregateRating', {}).get('ratingCount', None),
            'genre': formatted_genre,  # Fixed this line
            'run_time': item.get('duration', None),
            'imdb_url': item.get('url', None),
            'description': item.get('description', None)
        })
    
    return basic_data

# Helper function for our get_all_movie_data function
def get_movie_data_soup(movie_url):
    try:
        time.sleep(random.uniform(1, 3))
        response = requests.get(movie_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for specific data-testid attributes (more reliable)
        financial_data = {}
        
        # Find all financial items
        financial_items = soup.find_all('li', class_='ipc-metadata-list__item')
        
        for item in financial_items:
            label = item.find('span', class_='ipc-metadata-list-item__label')
            value = item.find('span', class_='ipc-metadata-list-item__list-content-item')
            
            if label and value:
                label_text = label.get_text(strip=True).lower()
                value_text = value.get_text(strip=True)
                
                if 'budget' in label_text:
                    financial_data['budget'] = value_text
                elif 'box office' in label_text or 'gross' in label_text:
                    financial_data['box_office'] = value_text
            
            if value and 'wins' in value.get_text():
                financial_data['awards'] = value.get_text()
        
        # Extract other data
        certs = soup.find('a', href=re.compile(r'parentalguide'))
        certs = certs.get_text(strip=True) if certs else None

        releaseinfo = soup.find('a', href=re.compile(r'releaseinfo'))
        release = releaseinfo.get_text(strip=True) if releaseinfo else None
        
        metascore = soup.find('span', class_=re.compile(r'metacritic'))
        metascore = metascore.get_text(strip=True) if metascore else None
        
        return (
            certs,
            metascore,
            release,
            financial_data.get('awards'),
            financial_data.get('budget'),
            financial_data.get('box_office')
        )
        
    except Exception as e:
        print(f"Error processing {movie_url}: {e}")
        return None, None, None, None, None, None

def get_all_movie_data(movie_url):
    """
    Get both JSON-LD and HTML data in one function call
    """
    try:
        time.sleep(random.uniform(1, 3))
        response = requests.get(movie_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get JSON-LD data
        json_data = None
        script_tag = soup.find('script', type='application/ld+json')
        if script_tag:
            json_data = json.loads(script_tag.string)
        
        # Get HTML data
        html_data = get_movie_data_soup(movie_url)  # Modified version that takes soup
        
        # Combine results
        if json_data:
            director = json_data.get('director', [{}])[0].get('name', None)
            top_actors = [actor['name'] for actor in json_data.get('actor', [])][:3]
        else:
            director, top_actors= None, []
        
        certs, meta, release, wins, budget, box_office = html_data
        
        return director, top_actors, certs, meta, release, wins, budget, box_office
        
    except Exception as e:
        print(f"Error with {movie_url}: {e}")
        return None, [], None, None, None, None, None, None