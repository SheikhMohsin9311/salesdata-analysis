import pandas as pd

def load_data(filepath='sales_data.csv'):
    """
    Loads and preprocesses sales data.
    
    Args:
        filepath (str): Path to the CSV file.
        
    Returns:
        pd.DataFrame: Processed dataframe with datetime conversion.
    """
    try:
        df = pd.read_csv(filepath)
        # Ensure Date is datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Extract useful time features for easier analysis
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.month
        df['Month_Name'] = df['Date'].dt.month_name()
        
        return df
    except FileNotFoundError:
        return None
