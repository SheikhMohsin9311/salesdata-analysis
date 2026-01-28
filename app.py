import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src import loader, analysis, forecasting

# Page Config
st.set_page_config(page_title="Sales Dashboard", layout="wide", page_icon="📊")

# Title
st.title("📊 Interactive Sales Performance Dashboard")

# Load Data
@st.cache_data
def load_data():
    return loader.load_data()

df = load_data()

if df is not None:
    # Sidebar
    st.sidebar.header("Filters")
    
    # Filter by Year
    years = sorted(df['Year'].unique())
    selected_year = st.sidebar.selectbox("Select Year", ["All"] + years)
    
    # Filter by Country
    countries = sorted(df['Country'].unique())
    selected_country = st.sidebar.multiselect("Select Country", countries, default=countries)
    
    # Filter by Category
    categories = sorted(df['Product_Category'].unique())
    selected_category = st.sidebar.multiselect("Select Category", categories, default=categories)
    
    # Apply Filters
    filtered_df = df.copy()
    if selected_year != "All":
        filtered_df = filtered_df[filtered_df['Year'] == selected_year]
    
    if selected_country:
        filtered_df = filtered_df[filtered_df['Country'].isin(selected_country)]
        
    if selected_category:
        filtered_df = filtered_df[filtered_df['Product_Category'].isin(selected_category)]
        
    # KPIs
    st.markdown("### Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"${filtered_df['Revenue'].sum():,.0f}")
    col2.metric("Total Profit", f"${filtered_df['Profit'].sum():,.0f}")
    col3.metric("Total Orders", f"{filtered_df.shape[0]:,}")
    col4.metric("Avg. Unit Price", f"${filtered_df['Unit_Price'].mean():,.2f}")
    
    st.divider()

    # Layout: 2 Columns for Charts
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Revenue by Category")
        rev_by_cat = analysis.get_revenue_by_category(filtered_df)
        fig_cat = px.bar(
            x=rev_by_cat.index, 
            y=rev_by_cat.values, 
            labels={'x': 'Category', 'y': 'Revenue'},
            color=rev_by_cat.values,
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_cat, use_container_width=True)
        
        st.subheader("Top 10 Profitable Sub-Categories")
        prof_sub = analysis.get_top_profitable_subcategories(filtered_df)
        fig_prof = px.bar(
            x=prof_sub.values,
            y=prof_sub.index,
            orientation='h',
            labels={'x': 'Profit', 'y': 'Sub-Category'},
            color=prof_sub.values,
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig_prof, use_container_width=True)

    with col_right:
        st.subheader("Sales Trend (Monthly)")
        # For trend, we want to see the filtered trend
        monthly_sales = filtered_df.groupby(['Year', 'Month', 'Month_Name'])['Revenue'].sum().reset_index()
        # Sort by year and month
        monthly_sales = monthly_sales.sort_values(['Year', 'Month'])
        # Create a 'Date' column for plotting
        monthly_sales['Date'] = pd.to_datetime(monthly_sales[['Year', 'Month']].assign(Day=1))
        
        fig_trend = px.line(
            monthly_sales, 
            x='Date', 
            y='Revenue',
            markers=True
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
        st.subheader("Revenue by Country")
        rev_country = analysis.get_revenue_by_country(filtered_df)
        fig_country = px.pie(
            values=rev_country.values,
            names=rev_country.index,
            hole=0.4
        )
        st.plotly_chart(fig_country, use_container_width=True)

    st.divider()
    
    # Forecasting Section
    st.subheader("🔮 Sales Forecast (Next 6 Months)")
    st.markdown("Forecast is based on the **entire dataset** history (filters ignored to ensure data continuity).")
    
    if st.button("Generate Forecast"):
        with st.spinner("Training model..."):
            forecast_df, history = forecasting.forecast_sales(df, periods=6)
            
            if forecast_df is not None:
                # Plotting History + Forecast
                fig_forecast = go.Figure()
                
                # History
                fig_forecast.add_trace(go.Scatter(
                    x=history.index, 
                    y=history.values, 
                    mode='lines', 
                    name='Historical Sales',
                    line=dict(color='blue')
                ))
                
                # Forecast
                fig_forecast.add_trace(go.Scatter(
                    x=forecast_df['Date'], 
                    y=forecast_df['Forecast'], 
                    mode='lines+markers', 
                    name='Forecast',
                    line=dict(color='orange', dash='dash')
                ))
                
                fig_forecast.update_layout(title="Sales Forecast", xaxis_title="Date", yaxis_title="Revenue")
                st.plotly_chart(fig_forecast, use_container_width=True)
                
                st.write("Predicted Values:", forecast_df.set_index('Date'))
            else:
                st.error("Not enough data to generate forecast or model failed.")

else:
    st.error("Data could not be loaded. Please ensure 'sales_data.csv' is in the project directory.")
