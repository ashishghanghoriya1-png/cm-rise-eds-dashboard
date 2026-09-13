import os
import sys
import io
import json
import re
import pandas as pd
import requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

csv_path = r"C:\Users\Peepul\OneDrive - Absolute Return For Kids\Documents\EDS Sheet.csv"
df = pd.read_csv(csv_path)

print(f"Step 1: Reading full dataset ({len(df)} rows x {len(df.columns)} columns)...", flush=True)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:14B"

results = []

for idx, row in df.iterrows():
    t_id = f"Teacher_{idx+1}"
    
    qual_snippets = []
    for col in df.columns:
        val = str(row[col])
        if pd.notna(row[col]) and len(val) > 8 and not val.isdigit():
            qual_snippets.append(f"{col}: {val[:120]}")
            
    full_text = " | ".join(qual_snippets)
    if len(full_text) < 15:
        continue

    prompt = f"""System: Qualitative CAQDAS Grounded Theory coding across all columns.
Teacher: {t_id} | District: {row.get('District of respondent teacher', 'N/A')}
Text: {full_text[:600]}

Format output EXACTLY in 4 short lines:
THEME: (Choose 1: Classroom Execution Barrier, Digital Passive Playback, CLSS Informal Cascade, Admin Workload Friction, Resource Non-Receipt)
ROOT CAUSE: (1 short sentence)
VERBATIM QUOTE: (1 direct quote)
POLICY ACTION: (1 short sentence)
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.1, "num_predict": 90}
    }

    try:
        print(f"[{idx+1}/{len(df)}] Coding {t_id}...", flush=True)
        r = requests.post(OLLAMA_URL, json=payload, timeout=120)
        if r.status_code == 200:
            text = r.json().get("response", "")
            
            theme = re.search(r"THEME:\s*(.*)", text)
            cause = re.search(r"ROOT CAUSE:\s*(.*)", text)
            quote = re.search(r"VERBATIM QUOTE:\s*(.*)", text)
            action = re.search(r"POLICY ACTION:\s*(.*)", text)
            
            res = {
                "Teacher_ID": t_id,
                "District": str(row.get("District of respondent teacher", "N/A")),
                "Experience": str(row.get("Years of teaching experience", "N/A")),
                "Theme": theme.group(1).strip() if theme else "Classroom Execution Barrier",
                "Root_Cause": cause.group(1).strip() if cause else text[:80],
                "Verbatim_Quote": quote.group(1).strip() if quote else "",
                "Policy_Action": action.group(1).strip() if action else "",
                "Raw_Qualitative_Text": full_text[:300]
            }
            results.append(res)
            print(f"  -> Coded: '{res['Theme']}'", flush=True)
            
            # Incremental save every 5 teachers
            if len(results) % 5 == 0:
                pd.DataFrame(results).to_excel("qualitative_coded_database_complete_all_rows.xlsx", index=False)
                print(f"  💾 Saved Checkpoint: {len(results)} / {len(df)} teachers coded!", flush=True)

    except Exception as e:
        print(f"  ⚠️ Timeout/Error on {t_id}: {e}", flush=True)

out_df = pd.DataFrame(results)
out_excel = "qualitative_coded_database_complete_all_rows.xlsx"
out_df.to_excel(out_excel, index=False)
print(f"\n🎉 Finished coding ALL {len(out_df)} rows and columns! Saved to '{out_excel}'", flush=True)
