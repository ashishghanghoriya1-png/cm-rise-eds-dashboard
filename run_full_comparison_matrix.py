import pandas as pd
import numpy as np
import sys

sys.stdout.reconfigure(encoding='utf-8')

july_path = 'EDS_Cleaned_Master_2July.xlsx'
aug_path = 'EDS_Full Data Table Consolidation_30 Aug.xlsx'

xls_july = pd.ExcelFile(july_path)
xls_aug = pd.ExcelFile(aug_path)

df_quant = pd.read_excel(xls_july, 'Quant_Structured').iloc[1:61].reset_index(drop=True)
df_qual = pd.read_excel(xls_july, 'Qual_FreeText').iloc[1:61].reset_index(drop=True)
df_obs = pd.read_excel(xls_july, 'Obs_Observations').iloc[1:61].reset_index(drop=True)

print("=" * 120)
print("DEEP 100% COLUMN-BY-COLUMN COVERAGE VERIFICATION")
print("=" * 120)

all_quant_cols = df_quant.columns.tolist()
print(f"Total columns in Quant_Structured: {len(all_quant_cols)}")

summary_stats = []
for i, col in enumerate(all_quant_cols):
    non_nulls = df_quant[col].notna().sum()
    nulls = df_quant[col].isna().sum()
    unique_vals = df_quant[col].unique()
    val_counts = df_quant[col].value_counts(dropna=False).to_dict()
    
    summary_stats.append({
        'Col Index': i,
        'Column Name': col,
        'Non-Null Count': non_nulls,
        'Null Count': nulls,
        'Null %': f"{(nulls/60)*100:.1f}%",
        'Unique Values': len(unique_vals),
        'Top Value Counts': str(val_counts)[:100]
    })

df_summary = pd.DataFrame(summary_stats)
print(df_summary.to_string())

