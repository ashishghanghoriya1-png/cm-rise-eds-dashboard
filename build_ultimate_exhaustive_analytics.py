import pandas as pd
import numpy as np
import json

excel_path = "c:/My Files Work/Gravity/EDS_Cleaned_Master_2July.xlsx"
xl = pd.ExcelFile(excel_path)

full_analytics = {}

for sheet in xl.sheet_names:
    df = pd.read_excel(excel_path, sheet_name=sheet)
    sheet_data = {
        "rows": int(df.shape[0]),
        "cols": int(df.shape[1]),
        "total_cells": int(df.shape[0] * df.shape[1]),
        "columns_detail": []
    }
    
    for i, col in enumerate(df.columns):
        series = df[col].dropna()
        non_null_count = int(len(series))
        null_count = int(df.shape[0] - non_null_count)
        completion_pct = round((non_null_count / max(df.shape[0], 1)) * 100, 1)
        
        # Numeric stats if applicable
        num_s = pd.to_numeric(series, errors="coerce").dropna()
        is_num = len(num_s) > 0 and (len(num_s) / max(non_null_count, 1)) > 0.5
        
        stats = {}
        if is_num:
            stats["mean"] = round(float(num_s.mean()), 2)
            stats["std"] = round(float(num_s.std()), 2) if len(num_s) > 1 else 0
            stats["min"] = round(float(num_s.min()), 2)
            stats["max"] = round(float(num_s.max()), 2)
            stats["median"] = round(float(num_s.median()), 2)
        
        # Value frequencies
        val_freqs = series.value_counts().head(5).to_dict()
        top_freqs = {str(k)[:80]: int(v) for k, v in val_freqs.items()}
        
        # Sample quotes for text columns
        samples = [str(x).strip() for x in series.tolist() if len(str(x).strip()) > 15][:3]
        
        col_meta = {
            "col_idx": i + 1,
            "col_name": str(col),
            "non_null": non_null_count,
            "null": null_count,
            "completion_pct": completion_pct,
            "is_numeric": is_num,
            "numeric_stats": stats,
            "top_frequencies": top_freqs,
            "text_samples": samples
        }
        sheet_data["columns_detail"].append(col_meta)
        
    full_analytics[sheet] = sheet_data

with open("ultimate_exhaustive_analytics.json", "w", encoding="utf-8") as f:
    json.dump(full_analytics, f, indent=2, ensure_ascii=False)

print("ULTIMATE ANALYTICS EXTRACTED SUCCESSFULY:")
for s, d in full_analytics.items():
    print(f"  - Sheet '{s}': {d['rows']} rows x {d['cols']} cols ({len(d['columns_detail'])} columns detailed)")
