import pandas as pd
from src import loader, analysis
import sys

def test_modules():
    print("Testing loader...")
    df = loader.load_data()
    if df is None:
        print("FAIL: DataFrame is None")
        sys.exit(1)
    print(f"PASS: Loaded {len(df)} movie records")

    print("\nTesting analysis...")
    # Test Director Analysis
    top_dirs = analysis.get_top_grossing_directors(df)
    if top_dirs.empty:
        print("FAIL: Top directors is empty")
        sys.exit(1)
    print("PASS: Top directors calculated")
    
    # Test Genre Analysis
    avg_genre = analysis.get_avg_imdb_by_genre(df)
    if avg_genre.empty:
        print("FAIL: Avg genre score is empty")
        sys.exit(1)
    print("PASS: Avg genre score calculated")
    
    print("\nAll modules passed basic checks.")

if __name__ == "__main__":
    test_modules()
