import pandas as pd
import requests
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

print("Step 1: Reading EDS Sheet.csv...", flush=True)
csv_path = r"C:\Users\Peepul\OneDrive - Absolute Return For Kids\Documents\EDS Sheet.csv"
df = pd.read_csv(csv_path)

obs_cols = [c for c in df.columns if "Key observation" in c]
OLLAMA_API_URL = "http://localhost:11434/api/generate"

full_report = "# Comprehensive Qualitative Research & Synthesis Report\n"
full_report += "## Based on `EDS Sheet.csv` (60 Teachers × 15 Variables)\n"
full_report += "### Analyzed using `Qwen2.5:14B` (Local LLM)\n\n"

full_report += "### Dataset Overview\n"
full_report += f"- **Total Teachers Observed:** {len(df)}\n"
full_report += f"- **Districts:** {', '.join(df['District of respondent teacher'].dropna().unique().astype(str))}\n"
full_report += f"- **Gender Split:** {df['Gender of respondent'].value_counts().to_dict()}\n"
full_report += f"- **Subjects:** {', '.join(df['Subject taught by teacher'].dropna().unique().astype(str))}\n\n"
full_report += "---\n\n"

for i, col in enumerate(obs_cols, 1):
    domain_clean = col.replace("Key observation note on ", "").replace("Key observation notes ", "")
    valid_notes = df[col].dropna().astype(str).tolist()
    valid_notes = [n.strip() for n in valid_notes if len(n.strip()) > 5 and n.strip() != col.strip()]
    
    if not valid_notes:
        continue

    # Take a representational sample of up to 15 key qualitative notes per domain to stay well within CPU compute limits
    sample_notes = valid_notes[:15]

    print(f"[{i}/{len(obs_cols)}] Analyzing domain via Qwen2.5:14B: '{domain_clean}' ({len(sample_notes)} sampled entries)...", flush=True)
    
    prompt = f"""You are a Principal Qualitative Researcher analyzing field observations of government school teachers in Madhya Pradesh.

Domain: {domain_clean}
Field Notes ({len(sample_notes)} observations):
""" + "\n".join([f"- {n}" for n in sample_notes]) + """

Please provide a detailed qualitative synthesis for this domain:
1. Core Findings & Emerging Patterns
2. Direct Evidence / Quotes
3. Operational Bottlenecks
4. Recommendations

Keep it concise, structured, and insightful."""

    payload = {
        "model": "qwen2.5:14B",
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_ctx": 2048,
            "temperature": 0.3
        }
    }
    
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=300)
        response.raise_for_status()
        res_text = response.json().get("response", "")
        
        full_report += f"## Domain {i}: {domain_clean.title()}\n\n"
        full_report += res_text + "\n\n---\n\n"
        print(f"[{i}/{len(obs_cols)}] Successfully synthesized domain '{domain_clean}'!", flush=True)
    except Exception as e:
        print(f"[{i}/{len(obs_cols)}] Error on domain '{domain_clean}': {e}", flush=True)

out_md_path = r"C:\Users\Peepul\.gemini\antigravity\brain\f3d36a05-31c4-4ca8-978f-d6e3730b02aa\EDS_CSV_Qwen14B_Domain_Report.md"
with open(out_md_path, "w", encoding="utf-8") as f:
    f.write(full_report)

print(f"\nSaved complete Domain Report to: {out_md_path}", flush=True)
