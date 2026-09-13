import pandas as pd
import glob

files = glob.glob(r"C:\Users\Peepul\OneDrive - Absolute Return For Kids\**\*EDS*.xlsx", recursive=True)

print(f"Found {len(files)} matching Excel files. Checking key files...")

for f in files:
    if "EDS_Cleaned_Master_2July" in f or "EDS_Master_Analysis" in f or "EDS Questionnaire" in f:
        try:
            xls = pd.ExcelFile(f)
            print(f"\nFile: {f}")
            print(f"  Sheets: {xls.sheet_names}")
            for sheet in xls.sheet_names:
                if "Quant" in sheet or "Structured" in sheet or "Master" in sheet:
                    df = pd.read_excel(f, sheet_name=sheet)
                    act_cols = [c for c in df.columns if "Activities participated" in c or "Digital" in c or "CLSS" in c or "Subject Training" in c]
                    print(f"  Sheet: {sheet} (Shape: {df.shape})")
                    for c in act_cols[:5]:
                        s = pd.to_numeric(df[c], errors="coerce").sum()
                        print(f"    - {c}: sum={s}, non-null={df[c].notna().sum()}")
        except Exception as e:
            print(f"  Error reading {f}: {e}")
