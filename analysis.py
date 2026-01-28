import pandas as pd
import matplotlib.pyplot as plt

def load_data(filepath='sales_data.csv'):
    """Loads and preprocesses real sales data"""
    print(f"Loading data from {filepath}...")
    df = pd.read_csv(filepath)
    
    # Ensure Date is datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    return df

def analyze_and_plot(df):
    """Analyzes data and creates a dashboard of plots"""
    
    # 1. Revenue by Category
    revenue_per_category = df.groupby('Product_Category')['Revenue'].sum().sort_values(ascending=False)
    
    # 2. Sales Trend over Time (Monthly per Year)
    # Extract Year and Month for pivoting
    df['Year'] = df['Date'].dt.year
    df['Month_Name'] = df['Date'].dt.month_name()
    
    # Pivot to get Months as rows and Years as columns
    monthly_sales_pivot = df.pivot_table(values='Revenue', index='Month_Name', columns='Year', aggfunc='sum')
    
    # Reindex to ensure months are in calendar order
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    monthly_sales_pivot = monthly_sales_pivot.reindex(month_order)
    
    # 3. Top 10 Profitable Sub-Categories
    profit_by_subcategory = df.groupby('Sub_Category')['Profit'].sum().sort_values(ascending=True).tail(10)
    
    # 4. Revenue by Country
    revenue_by_country = df.groupby('Country')['Revenue'].sum().sort_values(ascending=False)

    print("Generating dashboard...")
    
    # Visualization Setup
    plt.figure(figsize=(18, 12))
    plt.suptitle('Sales Performance Dashboard', fontsize=20)
    
    # Plot 1: Revenue by Category (Bar)
    plt.subplot(2, 2, 1)
    revenue_per_category.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Total Revenue by Product Category')
    plt.ylabel('Revenue ($)')
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Plot 2: Monthly Sales Trend (Multi-Line)
    plt.subplot(2, 2, 2)
    monthly_sales_pivot.plot(kind='line', marker='o', linewidth=2, ax=plt.gca())
    plt.title('Monthly Sales Trend (Yearly Comparison)')
    plt.ylabel('Revenue ($)')
    plt.xlabel('Month')
    plt.legend(title='Year')
    plt.grid(True, linestyle='--', alpha=0.7)

    # Plot 3: Top 10 Profitable Sub-Categories (Horizontal Bar)
    plt.subplot(2, 2, 3)
    profit_by_subcategory.plot(kind='barh', color='coral', edgecolor='black')
    plt.title('Top 10 Most Profitable Sub-Categories')
    plt.xlabel('Profit ($)')
    
    # Plot 4: Revenue by Country (Pie)
    plt.subplot(2, 2, 4)
    # Using a donut chart style for better aesthetics
    plt.pie(revenue_by_country, labels=revenue_by_country.index, autopct='%1.1f%%', 
            startangle=140, colors=plt.cm.Paired.colors, wedgeprops=dict(width=0.4))
    plt.title('Revenue Distribution by Country')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust for suptitle
    plt.savefig('sales_dashboard.png')
    print("\nDashboard saved as 'sales_dashboard.png'")

if __name__ == "__main__":
    try:
        df = load_data()
        print(f"Loaded {len(df)} records.")
        analyze_and_plot(df)
    except FileNotFoundError:
        print("Error: 'sales_data.csv' not found. Please download it first.")
