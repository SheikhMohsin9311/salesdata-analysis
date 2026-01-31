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

# Load Data
@st.cache_data
def load_data():
    return loader.load_data()

df = load_data()

if df is not None:
    # Sidebar
    st.sidebar.title("🎬 Filters")
    st.sidebar.markdown("Customize your view")
    
    # Filter by Year
    years = sorted(df['title_year'].unique(), reverse=True)
    selected_year = st.sidebar.select_slider("Release Year", options=["All"] + list(years), value="All")
    
    # Filter by Genre
    genres = sorted(df['primary_genre'].unique())
    selected_genre = st.sidebar.multiselect("Genre", genres)
    
    # Filter by Director
    directors = sorted(df['director_name'].dropna().unique())
    selected_director = st.sidebar.multiselect("Director", directors)
    
    st.sidebar.markdown("---")
    st.sidebar.info("Data source: IMDB 5000 Movie Dataset")

    # Apply Filters
    filtered_df = df.copy()
    if selected_year != "All":
        filtered_df = filtered_df[filtered_df['title_year'] == selected_year]
    
    if selected_genre:
        filtered_df = filtered_df[filtered_df['primary_genre'].isin(selected_genre)]
        
    if selected_director:
        filtered_df = filtered_df[filtered_df['director_name'].isin(selected_director)]

    # Main Content Area
    # Header
    col_header, col_kpi = st.columns([1, 2])
    
    with col_header:
        st.title("Movie Analytics")
        st.markdown(f"**{filtered_df.shape[0]}** movies filtered")

    # KPIs
    st.markdown("### Key Metrics")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Total Movies", f"{filtered_df.shape[0]:,}")
    kpi2.metric("Total Box Office", f"${filtered_df['gross'].sum():,.0f}")
    kpi3.metric("Avg. IMDB Score", f"{filtered_df['imdb_score'].mean():.1f}")
    kpi4.metric("Avg. Budget", f"${filtered_df['budget'].mean():,.0f}")
    
    st.markdown("---")

    # Tabs for Layout
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "🎬 Directors", "🎭 Genres"])

    with tab1:
        st.subheader("Global Trends")
        
        col_trend_1, col_trend_2 = st.columns([2, 1])
        
        with col_trend_1:
            # Movies Released per Year
            trend_df = analysis.get_movies_per_year(df if selected_year == "All" else filtered_df)
            fig_trend = px.area( # Changed to area for better visual
                x=trend_df.index, 
                y=trend_df.values,
                labels={'x': 'Year', 'y': 'Number of Movies'},
                template='plotly_dark'
            )
            fig_trend.update_traces(line_color='#00ADB5', fillcolor='rgba(0, 173, 181, 0.3)')
            fig_trend.update_layout(
                title_text='Movies Released per Year', 
                title_x=0,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
            )
            st.plotly_chart(fig_trend, use_container_width=True)

        with col_trend_2:
             # Budget vs Gross Scatter - moved here for a dense view
            st.markdown("#### Financial Performance")
            fig_scatter = px.scatter(
                filtered_df,
                x='budget',
                y='gross',
                color='primary_genre',
                hover_data=['movie_title', 'director_name', 'title_year'],
                log_x=True, log_y=True,
                labels={'budget': 'Budget', 'gross': 'Gross'},
                template='plotly_dark',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_scatter.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=30, l=0, r=0, b=0),
                legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

        st.subheader("Top Grossing Movies")
        top_movies = analysis.get_top_grossing_movies(filtered_df, n=10)
        st.dataframe(
            top_movies[['movie_title', 'director_name', 'gross', 'imdb_score', 'title_year']].set_index('movie_title'),
            use_container_width=True,
            column_config={
                "movie_title": "Movie Title",
                "director_name": "Director",
                "gross": st.column_config.NumberColumn("Gross Revenue", format="$%d"),
                "imdb_score": st.column_config.ProgressColumn("IMDB Score", min_value=0, max_value=10, format="%.1f"),
                "title_year": "Year"
            }
        )

    with tab2:
        st.subheader("Result-Oriented Directors")
        top_directors = analysis.get_top_grossing_directors(filtered_df)
        if not top_directors.empty:
            fig_dir = px.bar(
                x=top_directors.values, 
                y=top_directors.index, 
                orientation='h',
                labels={'x': 'Total Gross', 'y': 'Director'},
                color=top_directors.values,
                color_continuous_scale='Teal', # Matching theme
                template='plotly_dark'
            )
            fig_dir.update_layout(
                yaxis=dict(categoryorder='total ascending', showgrid=False),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
            )
            st.plotly_chart(fig_dir, use_container_width=True)
        else:
            st.info("No data for directors.")

    with tab3:
        st.subheader("Genre Landscape")
        
        avg_score = analysis.get_avg_imdb_by_genre(filtered_df)
        if not avg_score.empty:
            fig_genre = px.bar(
                x=avg_score.index, 
                y=avg_score.values,
                labels={'x': 'Genre', 'y': 'Avg IMDB Score'},
                color=avg_score.values,
                color_continuous_scale='Tropic',
                template='plotly_dark'
            )
            fig_genre.update_yaxes(range=[0, 10])
            fig_genre.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_genre, use_container_width=True)
        else:
            st.info("No data for genres.")

else:
    st.error("Data could not be loaded. Please ensure 'movie_metadata.csv' is in the project directory.")

