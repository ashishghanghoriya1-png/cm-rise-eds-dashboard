import pandas as pd
import json

excel_path = "c:/My Files Work/Gravity/EDS_Cleaned_Master_2July.xlsx"
xl = pd.ExcelFile(excel_path)

summary_data = {}

for sheet in xl.sheet_names:
    df = pd.read_excel(excel_path, sheet_name=sheet)
    sheet_info = {"shape": [df.shape[0], df.shape[1]], "columns": {}}
    for col in df.columns:
        col_s = df[col].dropna()
        n_count = len(col_s)
        n_unique = int(col_s.nunique())
        
        val_counts_raw = col_s.value_counts().head(5).to_dict()
        top_vals = {}
        for k, v in val_counts_raw.items():
            top_vals[str(k)[:100]] = int(v)
            
        sheet_info["columns"][str(col)] = {
            "non_null": n_count,
            "unique": n_unique,
            "top_values": top_vals
        }
    summary_data[sheet] = sheet_info

print("EXHAUSTIVE COLUMN AUDIT SUMMARY:")
for sheet_name, info in summary_data.items():
    print(f"Sheet '{sheet_name}': {info['shape'][0]} rows x {info['shape'][1]} cols | {len(info['columns'])} columns audited")

with open("column_by_column_summary.json", "w", encoding="utf-8") as f:
    json.dump(summary_data, f, indent=2, ensure_ascii=False)

print("Saved complete column audit to column_by_column_summary.json")
