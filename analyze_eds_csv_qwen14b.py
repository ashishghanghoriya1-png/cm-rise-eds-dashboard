import pandas as pd
import requests
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

print("Step 1: Reading EDS Sheet.csv...", flush=True)
csv_path = r"C:\Users\Peepul\OneDrive - Absolute Return For Kids\Documents\EDS Sheet.csv"
df = pd.read_csv(csv_path)

print(f"Loaded CSV: {len(df)} teachers x {len(df.columns)} columns", flush=True)

# Build a comprehensive structured textual context from the CSV
obs_cols = [c for c in df.columns if "Key observation" in c]

context_text = f"DATASET OVERVIEW:\n- Total Teachers Observed: {len(df)}\n"
context_text += f"- Districts Represented: {', '.join(df['District of respondent teacher'].dropna().unique().astype(str))}\n"
context_text += f"- Gender Breakdown: {df['Gender of respondent'].value_counts().to_dict()}\n"
context_text += f"- Subjects Represented: {', '.join(df['Subject taught by teacher'].dropna().unique().astype(str))}\n\n"

context_text += "QUALITATIVE FIELD OBSERVATIONS (BY DOMAIN):\n\n"

for col in obs_cols:
    domain_name = col.replace("Key observation note on ", "").replace("Key observation notes ", "")
    valid_notes = df[col].dropna().astype(str).tolist()
    # filter out header repeats if any
    valid_notes = [n for n in valid_notes if n.strip() != col.strip() and len(n.strip()) > 5]
    
    context_text += f"=== DOMAIN: {domain_name.upper()} (Total Entries: {len(valid_notes)}) ===\n"
    for idx, note in enumerate(valid_notes, 1):
        context_text += f"{idx}. {note}\n"
    context_text += "\n"

print("Step 2: Sending prompt to local model 'qwen2.5:14B' via Ollama...", flush=True)

OLLAMA_API_URL = "http://localhost:11434/api/generate"

system_prompt = """You are a Principal Qualitative Researcher and Education Policy Analyst. 
Analyze the provided teacher observation field notes from Madhya Pradesh government schools.

Please structure your report into the following sections:
1. Executive Summary & Synthesis
2. Domain 1: Daily & Annual Engagement Realities (Admin workload vs. teaching)
3. Domain 2: In-Person Training & Material Adoption Gaps
4. Domain 3: Perceived Value & Barriers in Digital / Online Learning
5. Domain 4: Non-Participation & Disengagement Root Causes
6. Domain 5: CLSS (Cluster Level Sharing Sessions) Learning Cascade Breakdown
7. Core Qualitative Insights (Themes & Quotes)
8. Strategic & Policy Recommendations for Education Department

Provide deep, evidence-based qualitative insights with direct references to the field observations."""

full_prompt = f"{system_prompt}\n\n{context_text}"

payload = {
    "model": "qwen2.5:14B",
    "prompt": full_prompt,
    "stream": False,
    "options": {
        "num_ctx": 8192,
        "temperature": 0.3
    }
}

try:
    response = requests.post(OLLAMA_API_URL, json=payload, timeout=600)
    response.raise_for_status()
    
    result = response.json()
    report_md = result.get("response", "")
    
    print("\nSuccessfully generated analysis from Qwen2.5:14B!", flush=True)
    
    # Save markdown output
    out_md_path = r"C:\Users\Peepul\.gemini\antigravity\brain\f3d36a05-31c4-4ca8-978f-d6e3730b02aa\EDS_CSV_Qwen14B_Insights.md"
    with open(out_md_path, "w", encoding="utf-8") as f:
        f.write(report_md)
    print(f"Saved Markdown report to: {out_md_path}", flush=True)

except Exception as e:
    print(f"Error communicating with Ollama API: {e}", flush=True)
