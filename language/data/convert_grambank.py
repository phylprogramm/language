import pandas as pd
import numpy as np


def convert_grambank_to_wide_format(values_file, languages_file, parameters_file=None):
    """
    Convert Grambank from long format to wide format.
    
    Input files:
    - grambank.csv or values.csv: Language_ID, Parameter_ID (GB020, etc.), Value
    - languages.csv: ID, Name, Macroarea, Family_name, etc.
    - parameters.csv (optional): ID, Name, Description
    """
    
    print("Loading Grambank data...")
    
    # Load files
    values = pd.read_csv(values_file)
    languages = pd.read_csv(languages_file)
    
    # Handle different column naming conventions
    lang_id_col = 'Language_ID' if 'Language_ID' in values.columns else 'language_id'
    param_id_col = 'Parameter_ID' if 'Parameter_ID' in values.columns else 'parameter_id'
    value_col = 'Value' if 'Value' in values.columns else 'value'
    
    print(f"Loaded {len(values)} feature values for {len(languages)} languages")
    
    # Pivot to wide format: rows = languages, columns = parameters (GB020, GB021, etc.)
    print("Converting to wide format...")
    wide = values.pivot(index=lang_id_col, columns=param_id_col, values=value_col)
    
    # Reset index
    wide = wide.reset_index()
    
    # Merge with language metadata
    print("Adding language metadata...")
    
    # Handle different ID column names
    lang_id_in_langs = 'ID' if 'ID' in languages.columns else 'id'
    result = languages.merge(wide, left_on=lang_id_in_langs, right_on=lang_id_col, how='left')
    
    # Drop duplicate ID column
    if lang_id_col in result.columns and lang_id_col != lang_id_in_langs:
        result = result.drop(lang_id_col, axis=1)
    
    # Reorder: metadata first, then GB features
    metadata_cols = [col for col in result.columns if not col.startswith('GB')]
    feature_cols = sorted([col for col in result.columns if col.startswith('GB')])
    result = result[metadata_cols + feature_cols]
    
    print(f"\nOutput shape: {result.shape[0]} languages × {result.shape[1]} columns")
    print(f"GB feature columns: {len(feature_cols)}")
    
    return result


def convert_grambank_values_to_sane_format(df, feature_cols=None):
    """
    Convert Grambank values to standardized format.
    
    Grambank codes:
    - 0 → '0' (feature absent)
    - 1 → '1' (feature present)
    - ? → NaN (unknown)
    
    This version keeps them as strings for consistency with analysis scripts.
    """
    
    if feature_cols is None:
        feature_cols = [col for col in df.columns if col.startswith('GB')]
    
    print(f"\nConverting {len(feature_cols)} GB feature columns...")
    
    df_converted = df.copy()
    
    for col in feature_cols:
        # Convert to string, replace '?' with NaN
        df_converted[col] = df_converted[col].astype(str)
        df_converted[col] = df_converted[col].replace('?', np.nan)
        df_converted[col] = df_converted[col].replace('nan', np.nan)
    
    return df_converted


def add_feature_descriptions(df, parameters_file):
    """
    Add feature descriptions as comments or separate mapping file.
    """
    
    try:
        params = pd.read_csv(parameters_file)
        
        # Create mapping dictionary
        param_dict = {}
        for _, row in params.iterrows():
            param_id = row.get('ID', row.get('id', row.get('Parameter_ID', '')))
            param_name = row.get('Name', row.get('name', ''))
            if param_id and param_name:
                param_dict[param_id] = param_name
        
        # Save mapping to separate file
        mapping_df = pd.DataFrame(list(param_dict.items()), 
                                  columns=['Parameter_ID', 'Description'])
        mapping_df.to_csv('grambank_feature_descriptions.csv', index=False)
        print("✓ Feature descriptions saved to: grambank_feature_descriptions.csv")
        
        return param_dict
    except:
        print("⚠ Could not load parameter descriptions")
        return {}


def main():
    # File paths - adjust as needed
    values_file = 'grambank.csv'  # or 'values.csv'
    languages_file = 'languages.csv'
    parameters_file = 'parameters.csv'  # optional
    output_file = 'grambank_sane_format.csv'
    
    # Convert to wide format
    grambank_wide = convert_grambank_to_wide_format(values_file, languages_file)
    
    # Convert to sane format (strings, handle NaN)
    grambank_wide = convert_grambank_values_to_sane_format(grambank_wide)
    
    # Add feature descriptions (optional)
    try:
        add_feature_descriptions(grambank_wide, parameters_file)
    except:
        print("⚠ Skipping feature descriptions")
    
    # Save
    print(f"\nSaving to {output_file}...")
    grambank_wide.to_csv(output_file, index=False)
    print("✓ Done!")
    
    # Show sample
    print("\nSample (first 5 rows, first 10 columns):")
    print(grambank_wide.iloc[:5, :10])
    
    # Show some statistics
    print("\nDataset statistics:")
    print(f"Total languages: {len(grambank_wide)}")
    gb_cols = [col for col in grambank_wide.columns if col.startswith('GB')]
    print(f"Total GB features: {len(gb_cols)}")
    
    # Count coverage
    if gb_cols:
        coverage = grambank_wide[gb_cols].notna().sum(axis=1)
        print(f"Average features per language: {coverage.mean():.1f}")
        print(f"Min features: {coverage.min()}")
        print(f"Max features: {coverage.max()}")


if __name__ == "__main__":
    main()
