import pandas as pd
import sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

file_path = r"C:\Users\Peepul\OneDrive - Absolute Return For Kids\CMRise TPD Team's files - TPD - Knowledge Management System\Academic Year 2026-27\9. CPD EDS\3. Report\2. EDS Internal Report\EDS_ Report Annexure_30 July\EDS_Master_Analysis.xlsx"

print(f"Reading Master Qualitative Transcript Log: '{file_path}'...")
xls = pd.ExcelFile(file_path)
print("Sheets:", xls.sheet_names)

df_coding = pd.read_excel(xls, sheet_name="Master Coding Table")
df_inductive = pd.read_excel(xls, sheet_name="Master Inductive Log")

print(f"\n1. Master Coding Table Shape: {df_coding.shape}")
print("Columns:", df_coding.columns.tolist())
print("\nSample Coded Transcripts:")
print(df_coding.head(8).to_string())

print(f"\n2. Master Inductive Log Shape: {df_inductive.shape}")
print("Columns:", df_inductive.columns.tolist())
print("\nSample Inductive Log Entries:")
print(df_inductive.head(8).to_string())
