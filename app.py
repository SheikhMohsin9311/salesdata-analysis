import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src import loader, analysis

# Page Config
st.set_page_config(page_title="Movie Analytics Dashboard", layout="wide", page_icon="🎬")

# Load Custom CSS
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Title
st.title("🎬 Movie Analytics Dashboard")
st.markdown("Explore trends in the IMDB 5000 movie dataset.")

# Load Data
@st.cache_data
def load_data():
    return loader.load_data()

df = load_data()

if df is not None:
    # Sidebar
    st.sidebar.header("Filters")
    
    # Filter by Year
    years = sorted(df['title_year'].unique(), reverse=True)
    selected_year = st.sidebar.selectbox("Select Release Year", ["All"] + list(years))
    
    # Filter by Genre
    genres = sorted(df['primary_genre'].unique())
    selected_genre = st.sidebar.multiselect("Select Genre", genres)
    
    # Filter by Director
    directors = sorted(df['director_name'].dropna().unique())
    selected_director = st.sidebar.multiselect("Select Director", directors)
    
    # Apply Filters
    filtered_df = df.copy()
    if selected_year != "All":
        filtered_df = filtered_df[filtered_df['title_year'] == selected_year]
    
    if selected_genre:
        filtered_df = filtered_df[filtered_df['primary_genre'].isin(selected_genre)]
        
    if selected_director:
        filtered_df = filtered_df[filtered_df['director_name'].isin(selected_director)]
        
    # KPIs
    st.markdown("### Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Movies", f"{filtered_df.shape[0]:,}")
    col2.metric("Total Box Office", f"${filtered_df['gross'].sum():,.0f}")
    col3.metric("Avg. IMDB Score", f"{filtered_df['imdb_score'].mean():.1f}")
    col4.metric("Avg. Budget", f"${filtered_df['budget'].mean():,.0f}")
    
    st.divider()

    # Tabs for Layout
    tab1, tab2, tab3 = st.tabs(["Overview", "Director Insights", "Genre Trends"])

    with tab1:
        st.subheader("Global Trends")
        
        # Movies Released per Year
        trend_df = analysis.get_movies_per_year(df if selected_year == "All" else filtered_df)
        fig_trend = px.line(
            x=trend_df.index, 
            y=trend_df.values,
            labels={'x': 'Year', 'y': 'Number of Movies'},
            markers=True,
            template='plotly_dark'
        )
        fig_trend.update_layout(title_text='Movies Released per Year', title_x=0.5)
        st.plotly_chart(fig_trend, use_container_width=True)

        st.subheader("Top Grossing Movies Data")
        top_movies = analysis.get_top_grossing_movies(filtered_df, n=20)
        st.dataframe(top_movies.set_index('movie_title'), use_container_width=True)

    with tab2:
        st.subheader("Top 10 Highest Grossing Directors")
        top_directors = analysis.get_top_grossing_directors(filtered_df)
        if not top_directors.empty:
            fig_dir = px.bar(
                x=top_directors.values, 
                y=top_directors.index, 
                orientation='h',
                labels={'x': 'Total Gross', 'y': 'Director'},
                color=top_directors.values,
                color_continuous_scale='Magma',
                template='plotly_dark'
            )
            fig_dir.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_dir, use_container_width=True)
        else:
            st.info("No data for directors.")

    with tab3:
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("Average IMDB Score by Genre")
            avg_score = analysis.get_avg_imdb_by_genre(filtered_df)
            if not avg_score.empty:
                fig_genre = px.bar(
                    x=avg_score.index, 
                    y=avg_score.values,
                    labels={'x': 'Genre', 'y': 'Avg IMDB Score'},
                    color=avg_score.values,
                    color_continuous_scale='Viridis',
                    template='plotly_dark'
                )
                fig_genre.update_yaxes(range=[0, 10])
                st.plotly_chart(fig_genre, use_container_width=True)
            else:
                st.info("No data for genres.")

        with col_right:
            st.subheader("Budget vs. Gross Revenue")
            fig_scatter = px.scatter(
                filtered_df,
                x='budget',
                y='gross',
                color='primary_genre',
                hover_data=['movie_title', 'director_name', 'title_year'],
                log_x=True, log_y=True,
                labels={'budget': 'Budget (Log)', 'gross': 'Gross Revenue (Log)'},
                template='plotly_dark'
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

else:
    st.error("Data could not be loaded. Please ensure 'movie_metadata.csv' is in the project directory.")
