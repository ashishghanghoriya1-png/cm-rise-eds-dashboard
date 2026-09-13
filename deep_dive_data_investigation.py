import pandas as pd
import json

excel_path = "c:/My Files Work/Gravity/EDS_Cleaned_Master_2July.xlsx"
xl = pd.ExcelFile(excel_path)

df_quant = pd.read_excel(excel_path, sheet_name="Quant_Structured")
df_qual = pd.read_excel(excel_path, sheet_name="Qual_FreeText")
df_obs = pd.read_excel(excel_path, sheet_name="Obs_Observations")
df_audit = pd.read_excel(excel_path, sheet_name="Kobo_Audit")
df_casc = pd.read_excel(excel_path, sheet_name="Sheet2")

print("=== DEEP DATA FACTS & ANALYSIS DUMP ===")
print("1. QUANTITATIVE FACTS:")
print("Districts:", df_quant["District of respondent teacher"].value_counts().to_dict())
print("Gender:", df_quant["Gender of respondent"].value_counts().to_dict())
print("Teaching Experience Summary:")
print(df_quant["Years of teaching experience"].describe().to_dict())
print("Daily Period Load Summary:")
print(df_quant["Avg no. of classroom periods taken in a day"].describe().to_dict())

print("\n2. TRAINING PARTICIPATION FACTS (%):")
for col in df_quant.columns:
    if "Activities participated" in str(col):
        val_c = df_quant[col].value_counts().to_dict()
        print(f"  {col.replace('Activities participated over 2025-26 academic year__', '')}: {val_c}")

print("\n3. QUALITATIVE FACTS & VERBATIMS (SAMPLE REAL TEACHER RESPONSES):")
print("\n--- Non-Academic Responsibilities (Real Verbatims) ---")
for i, txt in enumerate(df_qual["Teachers non-academic responsibilities in a Day"].dropna().head(10)):
    print(f"Teacher {i+1}: {txt}")

print("\n--- Training Improvements & Feedback (Real Verbatims) ---")
for i, txt in enumerate(df_qual["Key feedback to improve training session design or in-person training in general"].dropna().head(10)):
    print(f"Teacher {i+1}: {txt}")

print("\n--- Digital Course Effectiveness (Real Verbatims) ---")
for i, col in enumerate(df_qual.columns):
    if "digital" in col.lower() or "online" in col.lower() or "diksha" in col.lower():
        print(f"\nCol '{col}':")
        for j, txt in enumerate(df_qual[col].dropna().head(5)):
            print(f"  T{j+1}: {txt}")

print("\n--- Field Observer Real Notes ---")
for col in df_obs.columns:
    if "key observation" in col.lower():
        print(f"\nObserver Field Note Col '{col}':")
        for j, txt in enumerate(df_obs[col].dropna().head(5)):
            print(f"  Obs {j+1}: {txt}")
