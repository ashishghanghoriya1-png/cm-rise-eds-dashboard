import os
import sys
import io
import json
import glob
import pandas as pd
import requests
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ---------------------------------------------------------
# Ollama Configuration
# ---------------------------------------------------------
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:14b"  # Local model verified in workspace

# ---------------------------------------------------------
# Qualitative Codebook & Prompts
# ---------------------------------------------------------
QUALITATIVE_PROMPT_TEMPLATE = """
You are an expert Qualitative Research Assistant specializing in Grounded Theory and CAQDAS thematic analysis.

Analyze the following qualitative field note / interview transcript snippet:

--- TRANSCRIPT SNIPPET ---
{transcript_text}
--- END SNIPPET ---

Metadata: Teacher ID: {teacher_id} | District: {district} | Experience: {experience}

Extract the following structured qualitative insights:
1. Primary Qualitative Theme (Choose from: 'Classroom Translation Barrier', 'Digital Compliance vs Engagement', 'CLSS Cascade Dynamics', 'Administrative Workload Strain', 'Resource Non-Receipt', 'Peer Mentoring Opportunity')
2. Underlying Operational Root Cause
3. Direct Verbatim Quote (in original Hindi/English language) supporting the theme
4. Actionable Policy Recommendation

Return ONLY a valid JSON object with the following exact keys:
{{
  "theme": "...",
  "root_cause": "...",
  "verbatim_quote": "...",
  "recommendation": "..."
}}
"""

def analyze_snippet_with_ollama(transcript_text, teacher_id="N/A", district="N/A", experience="N/A"):
    prompt = QUALITATIVE_PROMPT_TEMPLATE.format(
        transcript_text=transcript_text,
        teacher_id=teacher_id,
        district=district,
        experience=experience
    )
    
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "format": "json",
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_ctx": 4096
        }
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        if response.status_code == 200:
            res_json = json.loads(response.json().get("response", "{}"))
            return res_json
        else:
            print(f"Ollama HTTP {response.status_code} error.")
            return None
    except Exception as e:
        print(f"Ollama Request Error: {e}")
        return None

def process_qualitative_dataset(input_file):
    print(f"\n🚀 Starting Ollama Automated Qualitative Coding on: '{input_file}'...")
    
    if input_file.endswith(".csv"):
        df = pd.read_csv(input_file)
    elif input_file.endswith(".xlsx"):
        df = pd.read_excel(input_file)
    else:
        print("Unsupported file format. Please use CSV or Excel.")
        return

    text_cols = [c for c in df.columns if any(k in c.lower() for k in ["text", "obs", "note", "comment", "qual", "feedback", "response"])]
    if not text_cols:
        text_cols = [df.columns[-1]] # Fallback to last column
        
    print(f"Detected qualitative text column(s): {text_cols}")
    
    results = []
    for idx, row in df.iterrows():
        t_id = row.get("Teacher_ID", row.get("Teacher ID", f"T_{idx+1}"))
        dist = row.get("District of respondent teacher", row.get("District", "N/A"))
        exp = row.get("Years of teaching experience", row.get("Experience", "N/A"))
        
        combined_text = " | ".join([str(row[c]) for c in text_cols if pd.notna(row[c]) and str(row[c]).strip() != ""])
        if len(combined_text) < 10:
            continue
            
        print(f"[{idx+1}/{len(df)}] Coding Teacher {t_id} via Ollama ({MODEL_NAME})...")
        coded_res = analyze_snippet_with_ollama(combined_text, teacher_id=t_id, district=dist, experience=exp)
        
        if coded_res:
            coded_res["Teacher_ID"] = t_id
            coded_res["District"] = dist
            coded_res["Experience"] = exp
            coded_res["Raw_Text"] = combined_text
            results.append(coded_res)
            
        time.sleep(0.1)

    coded_df = pd.DataFrame(results)
    out_excel = "qualitative_coded_database.xlsx"
    coded_df.to_excel(out_excel, index=False)
    print(f"\n✅ Qualitative Coding Complete! Saved Coded Database to: '{out_excel}'")

if __name__ == "__main__":
    # Default to Master Excel sheet or CSV if available
    sample_csv = r"C:\Users\Peepul\OneDrive - Absolute Return For Kids\Documents\EDS Sheet.csv"
    if os.path.exists(sample_csv):
        process_qualitative_dataset(sample_csv)
    else:
        print("Specify your dataset path in the script!")
