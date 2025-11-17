import pandas as pd
import numpy as np


def convert_wals_to_wide_format(values_file, languages_file, parameters_file=None):
    """
    Convert WALS from long format to wide format.
    
    Input files:
    - values.csv: Language_ID, Parameter_ID, Value
    - languages.csv: ID, Name, Macroarea, Family, etc.
    - parameters.csv (optional): ID, Name, Description
    """
    
    print("Loading WALS data...")
    
    # Load files
    values = pd.read_csv(values_file)
    languages = pd.read_csv(languages_file)
    
    print(f"Loaded {len(values)} feature values for {len(languages)} languages")
    
    # Pivot to wide format: rows = languages, columns = parameters
    print("Converting to wide format...")
    wide = values.pivot(index='Language_ID', columns='Parameter_ID', values='Value')
    
    # Reset index to make Language_ID a column
    wide = wide.reset_index()
    
    # Merge with language metadata
    print("Adding language metadata...")
    result = languages.merge(wide, left_on='ID', right_on='Language_ID', how='left')
    
    # Drop duplicate Language_ID column
    if 'Language_ID' in result.columns:
        result = result.drop('Language_ID', axis=1)
    
    # Reorder columns: metadata first, then features
    metadata_cols = [col for col in result.columns if not col.endswith('A') and col in languages.columns]
    feature_cols = sorted([col for col in result.columns if col not in metadata_cols])
    result = result[metadata_cols + feature_cols]
    
    print(f"\nOutput shape: {result.shape[0]} languages × {result.shape[1]} columns")
    print(f"Feature columns: {len(feature_cols)}")
    
    return result


def convert_wals_values_to_numeric(df, feature_cols=None):
    """
    Convert WALS values to numeric codes.
    
    Common WALS values:
    - '1', '2', '3', etc. → Keep as is
    - '?' → NaN
    """
    
    if feature_cols is None:
        # Auto-detect feature columns (ones that end with 'A' like '81A', '82A')
        feature_cols = [col for col in df.columns if col[-1].isalpha() and col[:-1].isdigit()]
    
    print(f"\nConverting {len(feature_cols)} feature columns to numeric...")
    
    df_converted = df.copy()
    
    for col in feature_cols:
        # Replace '?' with NaN, then convert to numeric
        df_converted[col] = pd.to_numeric(df_converted[col].replace('?', np.nan), errors='coerce')
    
    return df_converted


def main():
    # File paths - adjust as needed
    values_file = 'values.csv'
    languages_file = 'languages.csv'
    output_file = 'wals_wide_format.csv'
    
    # Convert to wide format
    wals_wide = convert_wals_to_wide_format(values_file, languages_file)
    
    # Optional: Convert to numeric
    # wals_wide = convert_wals_values_to_numeric(wals_wide)
    
    # Save
    print(f"\nSaving to {output_file}...")
    wals_wide.to_csv(output_file, index=False)
    print("✓ Done!")
    
    # Show sample
    print("\nSample (first 5 rows, first 10 columns):")
    print(wals_wide.iloc[:5, :10])


if __name__ == "__main__":
    main()
