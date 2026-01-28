import pandas as pd
from src import loader, analysis, forecasting
import sys

def test_modules():
    print("Testing loader...")
    df = loader.load_data()
    if df is None:
        print("FAIL: DataFrame is None")
        sys.exit(1)
    print(f"PASS: Loaded {len(df)} records")

    print("\nTesting analysis...")
    rev_cat = analysis.get_revenue_by_category(df)
    if rev_cat.empty:
        print("FAIL: Revenue by category is empty")
        sys.exit(1)
    print("PASS: Revenue by category calculated")
    
    print("\nTesting forecasting...")
    forecast, history = forecasting.forecast_sales(df, periods=3)
    if forecast is None:
        print("FAIL: Forecast failed")
        sys.exit(1)
    print(f"PASS: Forecast generated for {len(forecast)} periods")
    
    print("\nAll modules passed basic checks.")

if __name__ == "__main__":
    test_modules()
