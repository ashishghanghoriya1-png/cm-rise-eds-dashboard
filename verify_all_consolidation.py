import pandas as pd
import numpy as np
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

aug_path = 'EDS_Full Data Table Consolidation_30 Aug.xlsx'
july_path = 'EDS_Cleaned_Master_2July.xlsx'

xls_aug = pd.ExcelFile(aug_path)
xls_july = pd.ExcelFile(july_path)

df_quant = pd.read_excel(xls_july, 'Quant_Structured').iloc[1:61].reset_index(drop=True)
df_qual = pd.read_excel(xls_july, 'Qual_FreeText').iloc[1:61].reset_index(drop=True)
df_obs = pd.read_excel(xls_july, 'Obs_Observations').iloc[1:61].reset_index(drop=True)

print("--- RAW CLEANED DATASET BASE STATS ---")
print(f"Quant rows: {len(df_quant)}")
print(f"Qual rows: {len(df_qual)}")
print(f"Obs rows: {len(df_obs)}")

# Let's inspect column names in df_quant
print("\n--- QUANT COLUMNS OF INTEREST ---")
digital_cols = [c for c in df_quant.columns if 'digital' in c.lower() or 'diksha' in c.lower() or 'igot' in c.lower() or 'online' in c.lower()]
print("Digital columns:", digital_cols)

ipt_cols = [c for c in df_quant.columns if 'subject' in c.lower() or 'training' in c.lower() or 'in-person' in c.lower() or 'skg' in c.lower() or 'webex' in c.lower() or 'ytl' in c.lower()]
print("IPT/Training columns:", ipt_cols)

clss_cols = [c for c in df_quant.columns if 'clss' in c.lower() or 'samwad' in c.lower() or 'attendance' in c.lower()]
print("CLSS columns:", clss_cols)

print("\n=======================================================")
print("AUDITING DIGITAL COURSE DATA SHEET")
print("=======================================================")
# Let's check digital course metrics in df_quant
# Column 37: 'Are there any online courses teacher has done in last 1 year'
# Column 62: 'Does teacher know about DIKSHA Courses and platform'
# Column 38: 'Does teacher think digital or online courses are an effective way for teachers to learn'
# Column 39: 'How many hours teacher can allocate to engage with digital courses__ digital learning'
# Column 96: 'Name of the online platforms used by the teacher'
# Column 97: 'Diksha Course', 98: 'DIKSHA', 99: 'iGOT', 102: 'Did Online Course'

col_did_online = 'Are there any online courses teacher has done in last 1 year'
if col_did_online in df_quant.columns:
    print(f"\nValue counts for '{col_did_online}':")
    print(df_quant[col_did_online].value_counts(dropna=False))

col_effective = 'Does teacher think digital or online courses are an effective way for teachers to learn'
if col_effective in df_quant.columns:
    print(f"\nValue counts for '{col_effective}':")
    print(df_quant[col_effective].value_counts(dropna=False))

col_hours = 'How many hours teacher can allocate to engage with digital courses__ digital learning'
if col_hours in df_quant.columns:
    print(f"\nValue counts for '{col_hours}':")
    print(df_quant[col_hours].value_counts(dropna=False))

col_know_diksha = 'Does teacher know about DIKSHA Courses and platform'
if col_know_diksha in df_quant.columns:
    print(f"\nValue counts for '{col_know_diksha}':")
    print(df_quant[col_know_diksha].value_counts(dropna=False))

# Most engaging features of DIKSHA (cols 43 to 49)
engaging_cols = [c for c in df_quant.columns if 'Most engaging features of DIKSHA' in c]
print("\nEngaging features of DIKSHA:")
for c in engaging_cols:
    cnt = df_quant[c].notna().sum()
    val_cnts = df_quant[c].value_counts().to_dict()
    print(f"  {c}: non-null={cnt}, details={val_cnts}")

# Reasons for not doing DIKSHA course (cols 63 to 67)
not_doing_cols = [c for c in df_quant.columns if 'Reason for not doing DIKSHA course' in c]
print("\nReasons for not doing DIKSHA:")
for c in not_doing_cols:
    cnt = df_quant[c].notna().sum()
    val_cnts = df_quant[c].value_counts().to_dict()
    print(f"  {c}: non-null={cnt}, details={val_cnts}")

# Timing to do online (cols 40 to 42)
timing_cols = [c for c in df_quant.columns if 'Timing to do online' in c]
print("\nTiming to do online:")
for c in timing_cols:
    cnt = df_quant[c].notna().sum()
    val_cnts = df_quant[c].value_counts().to_dict()
    print(f"  {c}: non-null={cnt}, details={val_cnts}")
