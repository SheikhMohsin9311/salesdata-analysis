import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def forecast_sales(df, periods=6):
    """
    Forecasts total sales for the next N periods using Exponential Smoothing.
    
    Args:
        df (pd.DataFrame): The main dataframe.
        periods (int): Number of months to forecast.
        
    Returns:
        pd.DataFrame: A dataframe containing 'Date' and 'Forecast' columns.
    """
    # Resample to monthly sales
    monthly_sales = df.resample('ME', on='Date')['Revenue'].sum()
    
    # Fit the model (Additive trend and seasonality)
    # Using 'add' because sales usually grow linearly, and seasonality is roughly constant amplitude or proportional. 
    # For robust dummy data simple 'add' is safer.
    try:
        model = ExponentialSmoothing(
            monthly_sales, 
            trend='add', 
            seasonal='add', 
            seasonal_periods=12
        ).fit()
        
        # Forecast
        forecast = model.forecast(periods)
        
        # Create forecast dataframe
        forecast_df = pd.DataFrame({
            'Date': forecast.index,
            'Forecast': forecast.values
        })
        
        return forecast_df, monthly_sales
    except Exception as e:
        print(f"Forecasting error: {e}")
        return None, None
