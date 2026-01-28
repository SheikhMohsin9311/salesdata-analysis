import pandas as pd

def get_revenue_by_category(df):
    """Calculates total revenue per product category."""
    return df.groupby('Product_Category')['Revenue'].sum().sort_values(ascending=False)

def get_monthly_sales_pivot(df):
    """Pivots data for monthly sales comparison by year."""
    pivot = df.pivot_table(values='Revenue', index='Month_Name', columns='Year', aggfunc='sum')
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    return pivot.reindex(month_order)

def get_top_profitable_subcategories(df, n=10):
    """Returns top N most profitable sub-categories."""
    return df.groupby('Sub_Category')['Profit'].sum().sort_values(ascending=True).tail(n)

def get_revenue_by_country(df):
    """Calculates revenue distribution by country."""
    return df.groupby('Country')['Revenue'].sum().sort_values(ascending=False)

def get_filtered_data(df, year=None, country=None, category=None):
    """
    Filters dataframe based on optional parameters.
    """
    filtered_df = df.copy()
    if year:
        filtered_df = filtered_df[filtered_df['Year'] == year]
    if country:
        filtered_df = filtered_df[filtered_df['Country'] == country]
    if category:
        filtered_df = filtered_df[filtered_df['Product_Category'] == category]
    return filtered_df
