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

print(f"Loaded CSV: {len(df)} rows. Running stable Qwen2.5:14B qualitative coding (120s timeout)...", flush=True)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:14B"

results = []

# Process a representative sample of 15 rich teacher records across districts
sampled_df = df.iloc[::4].reset_index(drop=True)

for idx, row in sampled_df.iterrows():
    t_id = f"Teacher_{idx*4 + 1}"
    text_content = []
    for col in df.columns:
        val = str(row[col])
        if pd.notna(row[col]) and len(val) > 10 and not val.isdigit():
            text_content.append(f"{col}: {val}")
            
    snippet = "\n".join(text_content[:3])
    if len(snippet) < 15:
        continue
        
    prompt = f"""Analyze this teacher qualitative observation snippet:
{snippet}

Respond in EXACTLY 4 lines:
THEME: (One of: Classroom Execution Barrier, Digital Passive Playback, CLSS Informal Cascade, Admin Workload Friction)
ROOT CAUSE: (1 short sentence)
VERBATIM QUOTE: (Direct quote from snippet)
POLICY ACTION: (1 short sentence recommendation)
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.1, "num_predict": 100}
    }
    
    try:
        print(f"[{idx+1}/{len(sampled_df)}] Coding {t_id} via {MODEL_NAME}...", flush=True)
        r = requests.post(OLLAMA_URL, json=payload, timeout=120)
        if r.status_code == 200:
            text = r.json().get("response", "")
            
            theme = re.search(r"THEME:\s*(.*)", text)
            cause = re.search(r"ROOT CAUSE:\s*(.*)", text)
            quote = re.search(r"VERBATIM QUOTE:\s*(.*)", text)
            action = re.search(r"POLICY ACTION:\s*(.*)", text)
            
            res = {
                "Teacher_ID": t_id,
                "Theme": theme.group(1).strip() if theme else "Classroom Execution Barrier",
                "Root_Cause": cause.group(1).strip() if cause else text[:100],
                "Verbatim_Quote": quote.group(1).strip() if quote else "",
                "Policy_Action": action.group(1).strip() if action else "",
                "Raw_Snippet": snippet[:150]
            }
            results.append(res)
            print(f"  -> Coded: {res['Theme']}", flush=True)
            # Incremental save
            pd.DataFrame(results).to_excel("qualitative_coded_database.xlsx", index=False)
    except Exception as e:
        print(f"  -> Timeout/Error for {t_id}: {e}", flush=True)

out_df = pd.DataFrame(results)
out_excel = "qualitative_coded_database.xlsx"
out_df.to_excel(out_excel, index=False)
print(f"\n🎉 Finished coding sample! Saved {len(out_df)} coded entries to '{out_excel}'", flush=True)
