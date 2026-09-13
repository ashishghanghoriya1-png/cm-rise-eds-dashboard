import pandas as pd
import requests
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# 1. Read the observations sheet
print("Loading 'Obs_Observations' sheet...")
excel_path = r"C:\Users\Peepul\OneDrive - Absolute Return For Kids\Documents\EDS_Cleaned_Master_2July.xlsx"
try:
    df_obs = pd.read_excel(excel_path, sheet_name="Obs_Observations")
except Exception as e:
    print(f"Error reading Excel file: {e}")
    sys.exit(1)

# 2. Extract key statistics to feed to the LLM
print(f"Dataset loaded: {df_obs.shape[0]} rows, {df_obs.shape[1]} columns.")

# We will dynamically summarize the first 15 columns (or all if fewer) to avoid blowing up the context window
summary_text = "Here is a statistical summary of the 'Obs_Observations' sheet from the field research:\n\n"
summary_text += f"Total Observations Recorded: {len(df_obs)}\n\n"

for col in df_obs.columns[:25]:  # Look at the first 25 columns
    valid_count = df_obs[col].notna().sum()
    if valid_count > 0:
        summary_text += f"Column: '{col}' (Valid Responses: {valid_count})\n"
        # If it looks like categorical data, get value counts
        if df_obs[col].dtype == 'object' or df_obs[col].nunique() < 10:
            counts = df_obs[col].value_counts().head(5).to_dict()
            summary_text += f"  Top answers: {counts}\n"
        else:
            # If numeric, get mean
            try:
                mean_val = pd.to_numeric(df_obs[col], errors='coerce').mean()
                summary_text += f"  Average value: {mean_val:.2f}\n"
            except:
                pass
        summary_text += "\n"

print("Summary built. Sending to Qwen3:4b...")

# 3. Construct the prompt for Ollama
OLLAMA_API_URL = "http://localhost:11434/api/generate"
prompt = f"""
You are an expert qualitative researcher and data analyst. I have provided you with a statistical summary of an 'Observation Sheet' used during school visits.

{summary_text}

Based ONLY on the data summary provided above, please provide:
1. The 3 most significant insights or trends you can identify from these field observations.
2. One major area of concern or a barrier that stands out.
3. A brief recommendation on what the field team should focus on during their next round of observations.

Keep your response analytical, structured, and easy to read.
"""

payload = {
    "model": "qwen3:4b",
    "prompt": prompt,
    "stream": False
}

try:
    # 5 minute timeout since local models can take a moment to process large prompts
    response = requests.post(OLLAMA_API_URL, json=payload, timeout=300)
    response.raise_for_status()
    
    result = response.json()
    print("\n" + "="*70)
    print("QWEN 3 (4B) ANALYSIS OF OBSERVATION SHEET:")
    print("="*70)
    print(result.get("response", "No response text found."))
    print("="*70)
    
except requests.exceptions.RequestException as e:
    print(f"\nError communicating with Ollama API: {e}")
