# Linguistic Typology Correlation Analysis

Scripts for analyzing correlations between typological features in WALS and Grambank.

## Files

### Conversion Scripts
- `convert_wals.py` - WALS long→wide format converter
- `convert_grambank.py` - Grambank long→wide format converter

### Analysis Notebooks
- `VO_OV_CORRELATION_dryer.ipynb` - VO/OV correlations (Dryer method)
- `sv_vs_correlation_anti_dryer_wals.ipynb` - SV/VS correlations (WALS)
- `sv_vs_correlation_anti-dryer_grambank.ipynb` - SV/VS correlations (Grambank)
- `independence_sv_pssr_adj.ipynb` - Independence tests (SV/possessor/adjective)

## Data Format

Converts long format (Language_ID, Parameter_ID, Value) to wide format:
- Rows: languages
- Columns: metadata + features
- Values: feature codes (WALS: numeric; Grambank: 0/1/NaN)

### Input Files

**WALS:**
- `values.csv` - feature values
- `languages.csv` - language metadata

**Grambank:**
- `grambank.csv` or `values.csv` - feature values
- `languages.csv` - language metadata
- `parameters.csv` - feature descriptions (optional)

### Output Files

**WALS:**
- `wals_wide_format.csv` - wide format with feature columns (81A, 82A, etc.)

**Grambank:**
- `grambank_sane_format.csv` - wide format with GB features (GB020, GB021, etc.)
- `grambank_feature_descriptions.csv` - feature name mapping

## Usage
```bash
python convert_wals.py
python convert_grambank.py
```

Edit file paths in `main()` as needed.

## Methods

Notebooks compare Dryer's genealogical sampling method with alternative approaches for testing typological feature correlations.

## Requirements

- pandas
- numpy
