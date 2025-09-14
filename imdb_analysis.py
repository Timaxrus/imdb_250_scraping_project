# imdb_analysis.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import glob
import os

# Set style for better looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Create images directory if it doesn't exist
os.makedirs('images', exist_ok=True)

def find_latest_clean_data():
    """Find the latest cleaned CSV file"""
    clean_files = glob.glob(os.path.join('data', 'clean_top_250_*.csv'))
    if not clean_files:
        raise FileNotFoundError("No cleaned CSV files found in data directory")
    return max(clean_files, key=os.path.getctime)

def generate_analysis_results(df):
    """Generate and save analytical results to results/ folder"""
    print("Generating analytical results...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    
    # Create results directory
    os.makedirs('results', exist_ok=True)
    
    # 1. Basic Statistics Summary
    numeric_cols = ['imdb_rating', 'number_of_votes', 'run_time_minutes', 
                   'budget_million', 'box_office_million', 'award_wins', 'award_nominations']
    
    stats_summary = df[numeric_cols].describe().round(2)
    stats_summary.to_csv(f'results/statistical_summary_{timestamp}.csv')
    
    # 2. Correlation Matrix
    correlation_matrix = df[numeric_cols].corr().round(3)
    correlation_matrix.to_csv(f'results/correlation_matrix_{timestamp}.csv')
    
    # 3. Top 10 Lists
    # Top 10 highest rated movies
    top10_rated = df.nlargest(10, 'imdb_rating')[['title', 'imdb_rating', 'director', 'release_year']]
    top10_rated.to_csv(f'results/top10_highest_rated_{timestamp}.csv', index=False)
    
    # Top 10 most awarded movies
    top10_awards = df.nlargest(10, 'award_wins')[['title', 'award_wins', 'award_nominations', 'director']]
    top10_awards.to_csv(f'results/top10_most_awarded_{timestamp}.csv', index=False)
    
    # 4. Genre Analysis
    all_genres = []
    for genres in df['genre']:
        for genre in genres.split(', '):
            all_genres.append(genre)
    
    genre_stats = pd.Series(all_genres).value_counts().reset_index()
    genre_stats.columns = ['Genre', 'Count']
    genre_stats['Percentage'] = (genre_stats['Count'] / genre_stats['Count'].sum() * 100).round(1)
    genre_stats.to_csv(f'results/genre_analysis_{timestamp}.csv', index=False)
    
    # 5. Director Analysis
    director_stats = df['director'].value_counts().reset_index()
    director_stats.columns = ['Director', 'Movie_Count']
    director_stats.to_csv(f'results/director_analysis_{timestamp}.csv', index=False)
    
    # 6. Decade Analysis
    df['decade'] = (df['release_year'] // 10) * 10
    decade_stats = df.groupby('decade').agg({
        'imdb_rating': 'mean',
        'box_office_million': 'mean',
        'title': 'count'
    }).round(2)
    decade_stats.columns = ['Avg_Rating', 'Avg_Box_Office_Million', 'Movie_Count']
    decade_stats.to_csv(f'results/decade_analysis_{timestamp}.csv')
    
    # 7. Key Insights Report
    with open(f'results/key_insights_{timestamp}.txt', 'w') as f:
        f.write("IMDb Top 250 - Key Insights Report\n")
        f.write("=" * 50 + "\n\n")
        
        f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        
        f.write("Overall Statistics:\n")
        f.write(f"- Total Movies: {len(df)}\n")
        f.write(f"- Average Rating: {df['imdb_rating'].mean():.2f}/10\n")
        f.write(f"- Average Runtime: {df['run_time_minutes'].mean():.1f} minutes\n")
        f.write(f"- Average Box Office: ${df['box_office_million'].mean():.1f} million\n\n")
        
        f.write("Top Genres:\n")
        top_genres = genre_stats.head(5)
        for _, row in top_genres.iterrows():
            f.write(f"- {row['Genre']}: {row['Count']} movies ({row['Percentage']}%)\n")
        
        f.write(f"\nMost Prolific Director: {director_stats.iloc[0]['Director']} ({director_stats.iloc[0]['Movie_Count']} movies)\n")
        
        f.write(f"\nHighest Rated Movie: {top10_rated.iloc[0]['title']} ({top10_rated.iloc[0]['imdb_rating']}/10)\n")
        f.write(f"Most Awarded Movie: {top10_awards.iloc[0]['title']} ({top10_awards.iloc[0]['award_wins']} wins)\n")
        
        # Find interesting correlations
        rating_budget_corr = df['imdb_rating'].corr(df['budget_million'])
        rating_boxoffice_corr = df['imdb_rating'].corr(df['box_office_million'])
        
        f.write(f"\nInteresting Correlations:\n")
        f.write(f"- Rating vs Budget: {rating_budget_corr:.3f}\n")
        f.write(f"- Rating vs Box Office: {rating_boxoffice_corr:.3f}\n")
    
    print(f"Analytical results saved to /results folder with timestamp: {timestamp}")

def generate_all_visualizations(df):
    """Generate and save all visualizations"""
    print("Generating visualizations...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    
    # Question 1: Average runtime
    average_runtime = df['run_time_minutes'].mean()
    plt.figure(figsize=(10, 5))
    plt.hist(df['run_time_minutes'], bins=20, color='lightblue', edgecolor='black')
    plt.axvline(average_runtime, color='red', linestyle='--', 
               label=f'Average: {average_runtime:.1f} min')
    plt.xlabel('Runtime (minutes)')
    plt.ylabel('Number of Movies')
    plt.title('How Long Are the Best Movies?')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(f'images/runtime_distribution_{timestamp}.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Question 2: Most popular genres
    all_genres = []
    for genres in df['genre']:
        for genre in genres.split(', '):
            all_genres.append(genre)
    
    genre_counts = pd.Series(all_genres).value_counts()
    plt.figure(figsize=(12, 6))
    genre_counts.plot(kind='bar', color='orange')
    plt.xlabel('Genre')
    plt.ylabel('Number of Movies')
    plt.title('Most Common Genres in Top 250 Movies')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'images/genre_distribution_{timestamp}.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Question 3: Most frequent actors
    all_actors = []
    for actors in df['top_actors']:
        for actor in actors.split(', '):
            all_actors.append(actor)
    
    actor_counts = pd.Series(all_actors).value_counts().head(10)
    plt.figure(figsize=(10, 6))
    actor_counts.plot(kind='barh', color='green')
    plt.xlabel('Number of Appearances')
    plt.ylabel('Actor')
    plt.title('Top 10 Most Frequent Actors in Best Movies')
    plt.gca().invert_yaxis()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'images/top_actors_{timestamp}.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Question 4: Rating vs Box Office
    plt.figure(figsize=(10, 6))
    plt.scatter(df['imdb_rating'], df['box_office_million'], alpha=0.6, s=50)
    plt.xlabel('IMDb Rating (out of 10)')
    plt.ylabel('Box Office Revenue (Millions $)')
    plt.title('Do Higher Ratings Mean More Money?')
    plt.grid(True, alpha=0.3)
    
    # Add trend line
    z = np.polyfit(df['imdb_rating'], df['box_office_million'], 1)
    p = np.poly1d(z)
    plt.plot(df['imdb_rating'], p(df['imdb_rating']), "r--", alpha=0.8)
    plt.tight_layout()
    plt.savefig(f'images/rating_vs_boxoffice_{timestamp}.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Question 5: Ratings over time
    df['decade'] = (df['release_year'] // 10) * 10
    avg_rating_by_decade = df.groupby('decade')['imdb_rating'].mean()
    plt.figure(figsize=(10, 5))
    avg_rating_by_decade.plot(kind='line', marker='o', linewidth=2, markersize=8)
    plt.xlabel('Decade')
    plt.ylabel('Average IMDb Rating')
    plt.title('Average Movie Ratings Over Time')
    plt.grid(True, alpha=0.3)
    plt.xticks(avg_rating_by_decade.index)
    plt.tight_layout()
    plt.savefig(f'images/ratings_over_time_{timestamp}.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Question 6: Votes vs Box Office
    votes_corr = df['number_of_votes'].corr(df['box_office_million'])
    plt.figure(figsize=(8, 5))
    plt.scatter(df['number_of_votes']/1000000, df['box_office_million'], alpha=0.5)
    plt.xlabel('Votes (Millions)')
    plt.ylabel('Box Office ($ Millions)')
    plt.title(f'More Votes = More Money? (Correlation: {votes_corr:.2f})')
    plt.grid(True, alpha=0.3)
    plt.savefig(f'images/votes_vs_boxoffice_{timestamp}.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Question 7: Top 10 box office movies
    top10_box_office = df.nlargest(10, 'box_office_million')[['title', 'box_office_million']]
    plt.figure(figsize=(12, 8))
    bars = plt.barh(top10_box_office['title'], top10_box_office['box_office_million'], 
                    color='lightgreen', edgecolor='darkgreen', alpha=0.8)
    plt.xlabel('Box Office Revenue (Millions $)')
    plt.ylabel('Movie Title')
    plt.title('Top 10 Highest-Grossing Movies in IMDB Top 250')
    plt.gca().invert_yaxis()
    
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 50, bar.get_y() + bar.get_height()/2, 
                 f'${width:,.0f}M', 
                 va='center', ha='left', fontsize=10, fontweight='bold')
    
    plt.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    plt.savefig(f'images/top10_boxoffice_{timestamp}.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Question 8: Top 10 box office movies with directors
    top10_box_office = df.nlargest(10, 'box_office_million')[['title', 'box_office_million', 'director']]
    plt.figure(figsize=(14, 8))
    bars = plt.barh(top10_box_office['title'], top10_box_office['box_office_million'], 
                    color='lightcoral', edgecolor='darkred', alpha=0.8)
    plt.xlabel('Box Office Revenue (Millions $)')
    plt.ylabel('Movie Title')
    plt.title('Top 10 Highest-Grossing Movies and Their Directors')
    plt.gca().invert_yaxis()
    
    for i, (bar, director) in enumerate(zip(bars, top10_box_office['director'])):
        width = bar.get_width()
        plt.text(width + 50, bar.get_y() + bar.get_height()/2, 
                 f'Director: {director}', 
                 va='center', ha='left', fontsize=10, style='italic')
    
    for bar in bars:
        width = bar.get_width()
        plt.text(width - 100, bar.get_y() + bar.get_height()/2, 
                 f'${width:,.0f}M', 
                 va='center', ha='right', fontsize=10, fontweight='bold', color='white')
    
    plt.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    plt.savefig(f'images/top10_boxoffice_directors_{timestamp}.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Question 9: Top 10 award wins
    top10_wins = df.nlargest(10, 'award_wins')[['title', 'award_wins', 'imdb_rating']]
    plt.figure(figsize=(14, 8))
    bars = plt.barh(top10_wins['title'], top10_wins['award_wins'], 
                    color='gold', edgecolor='darkorange', alpha=0.8)
    plt.xlabel('Number of Award Wins')
    plt.ylabel('Movie Title')
    plt.title('Top 10 Movies with Most Award Wins and Their IMDb Ratings')
    plt.gca().invert_yaxis()
    
    for i, (bar, rating) in enumerate(zip(bars, top10_wins['imdb_rating'])):
        width = bar.get_width()
        plt.text(width + 2, bar.get_y() + bar.get_height()/2, 
                 f'IMDb: {rating}', 
                 va='center', ha='left', fontsize=10, fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    
    for bar in bars:
        width = bar.get_width()
        plt.text(width - 1, bar.get_y() + bar.get_height()/2, 
                 f'{width:.0f} wins', 
                 va='center', ha='right', fontsize=10, fontweight='bold', color='black')
    
    plt.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    plt.savefig(f'images/top10_award_wins_{timestamp}.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"All visualizations saved to /images folder with timestamp: {timestamp}")

def main():
    """Main analysis function"""
    try:
        # Load data
        latest_clean_file = find_latest_clean_data()
        df = pd.read_csv(latest_clean_file)
        print(f"Analyzing data from: {latest_clean_file}")
        
        # Generate all visualizations
        generate_all_visualizations(df)
        
        # Generate analytical results
        generate_analysis_results(df)
        
        print("Analysis completed successfully!")
        
    except Exception as e:
        print(f"Analysis failed: {e}")
        raise

if __name__ == "__main__":
    main()