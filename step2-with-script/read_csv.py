import pandas as pd
import sys
import os

def main():
    # Check if CSV file exists
    csv_file = 'sample_data.csv'
    
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found!")
        return
    
    # Read CSV file
    print(f"Reading {csv_file}...")
    df = pd.read_csv(csv_file)
    
    # Display basic info
    print(f"\nDataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print("\nFirst 5 rows:")
    print(df.head())
    
    print("\nBasic statistics:")
    print(df.describe())

if __name__ == "__main__":
    main()
