import pandas as pd

def load_data(filepath='movie_metadata.csv'):
    """
    Loads and preprocesses IMDB movie data.
    
    Args:
        filepath (str): Path to the CSV file.
        
    Returns:
        pd.DataFrame: Processed dataframe with cleaned columns.
    """
    try:
        df = pd.read_csv(filepath)
        
        # Drop duplicates if any
        df = df.drop_duplicates()
        
        # Fill missing values for critical columns or drop
        # For simplicity in this demo, we'll drop rows with missing Title or Year
        df = df.dropna(subset=['movie_title', 'title_year'])
        
        # Convert year to integer
        df['title_year'] = df['title_year'].astype(int)
        
        # Clean titles (remove trailing whitespace often found in this dataset)
        df['movie_title'] = df['movie_title'].str.strip()
        
        # Handle genres (pipe separated) -> taking the primary genre for simplicity in some charts
        df['primary_genre'] = df['genres'].apply(lambda x: x.split('|')[0] if isinstance(x, str) else 'Unknown')
        
        return df
    except FileNotFoundError:
        return None
