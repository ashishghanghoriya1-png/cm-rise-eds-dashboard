import sys
import io
import pandas as pd
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

excel_path = "c:/My Files Work/Gravity/EDS_Cleaned_Master_2July.xlsx"
xl = pd.ExcelFile(excel_path)

df_quant = pd.read_excel(excel_path, sheet_name="Quant_Structured")
df_qual = pd.read_excel(excel_path, sheet_name="Qual_FreeText")
df_obs = pd.read_excel(excel_path, sheet_name="Obs_Observations")

print("=================================================================")
print("  ACTUAL STUDY DATA EXPLORATION (60 TEACHERS ACROSS MP)")
print("=================================================================")

print(f"\n1. DISTRICT BREAKDOWN ({df_quant['District of respondent teacher'].nunique()} Districts):")
print(df_quant['District of respondent teacher'].value_counts())

print("\n2. TEACHING EXPERIENCE & PERIOD LOAD:")
print(df_quant[['Years of teaching experience', 'Avg no. of classroom periods taken in a day']].describe())

print("\n3. PARTICIPATION RATES ACROSS TRAINING MODALITIES:")
activity_cols = [c for c in df_quant.columns if "Activities participated" in str(c)]
for col in activity_cols:
    clean_name = str(col).split("/")[-1].split("__")[-1]
    count_1 = (df_quant[col].astype(str) == "1").sum()
    pct = (count_1 / 60) * 100
    print(f"  - {clean_name}: {count_1}/60 teachers ({pct:.1f}%)")

print("\n4. ACTUAL QUALITATIVE RESPONSES (SAMPLE VERBATIMS):")
print("\n--- Non-Academic Responsibilities ---")
for i, txt in enumerate(df_qual["Teachers non-academic responsibilities in a Day"].dropna()):
    if i < 15:
        print(f"T{i+1}: {str(txt)[:150]}")

print("\n--- Training Feedback & Suggestions ---")
for i, txt in enumerate(df_qual["Key feedback to improve training session design or in-person training in general"].dropna()):
    if i < 15:
        print(f"T{i+1}: {str(txt)[:150]}")

print("\n--- Digital Course Perceptions ---")
for col in df_qual.columns:
    if "digital" in str(col).lower() or "online" in str(col).lower():
        print(f"\nCol '{col}':")
        for j, txt in enumerate(df_qual[col].dropna()):
            if j < 8:
                print(f"  T{j+1}: {str(txt)[:150]}")

print("\n--- Field Observer Real Notes ---")
for col in df_obs.columns:
    if "key observation" in str(col).lower():
        print(f"\nObserver Note Col '{col}':")
        for j, txt in enumerate(df_obs[col].dropna()):
            if j < 8:
                print(f"  Obs {j+1}: {str(txt)[:150]}")
