import pandas as pd
import sys
import io
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

excel_path = r"C:\Users\Peepul\OneDrive - Absolute Return For Kids\Documents\EDS_Cleaned_Master_2July.xlsx"
df = pd.read_excel(excel_path, sheet_name="Obs_Observations")

text_cols = [c for c in df.columns if "Key observation" in c]

print(f"Total rows: {len(df)}")
print("Qualitative Observations Sample:\n")

for col in text_cols:
    print(f"=== {col.upper()} ===")
    # Drop NAs and the header row if it duplicated
    notes = df[col].dropna().astype(str).tolist()
    # Skip the first item if it matches the column name
    if notes and notes[0] == col:
        notes = notes[1:]
    
    # Print a sample of 5 distinct notes
    sample = list(set(notes))[:5]
    for i, note in enumerate(sample):
        print(f"  {i+1}. {note}")
    print("\n")
