import pandas as pd

import pandas as pd

def get_top_grossing_directors(df, n=10):
    """Returns top N directors by total gross revenue."""
    return df.groupby('director_name')['gross'].sum().sort_values(ascending=False).head(n)

def get_avg_imdb_by_genre(df):
    """Calculates average IMDB score per primary genre."""
    return df.groupby('primary_genre')['imdb_score'].mean().sort_values(ascending=False)

def get_movies_per_year(df):
    """Counts number of movies released per year."""
    return df.groupby('title_year').size().sort_index()

def get_top_grossing_movies(df, n=10):
    """Returns top N movies by gross revenue."""
    return df[['movie_title', 'gross']].sort_values(by='gross', ascending=False).head(n)

def get_filtered_data(df, year=None, director=None, genre=None):
    """
    Filters dataframe based on optional parameters.
    """
    filtered_df = df.copy()
    if year:
        filtered_df = filtered_df[filtered_df['title_year'] == year]
    if director:
        filtered_df = filtered_df[filtered_df['director_name'] == director]
    if genre:
        filtered_df = filtered_df[filtered_df['primary_genre'] == genre]
    return filtered_df
