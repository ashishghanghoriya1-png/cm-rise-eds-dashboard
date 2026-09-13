import pandas as pd
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

csv_path = r"C:\Users\Peepul\OneDrive - Absolute Return For Kids\Documents\EDS Sheet.csv"
df = pd.read_csv(csv_path)

print(f"=== EDS SHEET OVERVIEW ===")
print(f"Teachers: {len(df)}")
print(f"Districts: {df['District of respondent teacher'].value_counts().to_dict()}")
print(f"Gender: {df['Gender of respondent'].value_counts().to_dict()}")
print(f"Subjects: {df['Subject taught by teacher'].value_counts().to_dict()}")

obs_cols = [c for c in df.columns if "Key observation" in c]

for i, col in enumerate(obs_cols, 1):
    print(f"\n==========================================")
    print(f"DOMAIN {i}: {col}")
    print(f"==========================================")
    valid_notes = df[col].dropna().astype(str).tolist()
    valid_notes = [n.strip() for n in valid_notes if len(n.strip()) > 5 and n.strip() != col.strip()]
    print(f"Total non-empty observations: {len(valid_notes)}")
    for j, note in enumerate(valid_notes[:10], 1):
        print(f"  {j}. {note}")
