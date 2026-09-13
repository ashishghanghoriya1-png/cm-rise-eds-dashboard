import pandas as pd
import numpy as np
import sys

sys.stdout.reconfigure(encoding='utf-8')

aug_path = 'EDS_Full Data Table Consolidation_30 Aug.xlsx'
july_path = 'EDS_Cleaned_Master_2July.xlsx'

xls_aug = pd.ExcelFile(aug_path)
xls_july = pd.ExcelFile(july_path)

df_quant = pd.read_excel(xls_july, 'Quant_Structured').iloc[1:61].reset_index(drop=True)
df_qual = pd.read_excel(xls_july, 'Qual_FreeText').iloc[1:61].reset_index(drop=True)
df_obs = pd.read_excel(xls_july, 'Obs_Observations').iloc[1:61].reset_index(drop=True)
df_sheet2 = pd.read_excel(xls_july, 'Sheet2').iloc[1:61].reset_index(drop=True)

print("=" * 100)
print("EXACT DISCREPANCY DETECTOR: ROW BY ROW AUDIT OF 30 AUG SHEETS VS 2 JULY DATA")
print("=" * 100)

for sheet in xls_aug.sheet_names:
    df_s = pd.read_excel(xls_aug, sheet)
    print(f"\n" + "#"*100)
    print(f"SHEET: {sheet}")
    print("#"*100)
    
    for idx, row in df_s.iterrows():
        col0 = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ""
        col1 = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else ""
        col2 = str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else ""
        col3 = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else ""
        
        print(f"R{idx:02d} | [{col0}] | [{col1}] | [{col2}] | [{col3}]")

