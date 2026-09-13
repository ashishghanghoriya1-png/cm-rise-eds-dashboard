import urllib.request
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

prompt = """
You are a Lead Qualitative & Quantitative Education Policy Researcher at Peepul.
Synthesize ALL key findings from the MP Teacher CPD Ecosystem Diagnostic Study (CPD EDS) across Kobo Surveys, PowerBI Analytics, TabFM Machine Learning Predictions, and Field Observer Notes into a SINGLE-PAGE MASTER FINDINGS SUMMARY.

Synthesize the findings into TWO main sections suitable for fitting on ONE single page/slide:
1. AN EMPIRICAL FINDINGS TABLE (5 Columns: Dimension, Metric/Data Fact, Empirical Finding, Qualitative Evidence/Quote, Strategic Impact)
2. CORE EXECUTIVE POINTERS & TABFM SIMULATION HIGHLIGHTS (Bullet points covering non-academic workload, digital proxy completion, Margdarshika storage gap, CAC co-teaching demand, and TabFM counterfactual predictions).

Make the synthesis extremely sharp, high-density, professional, evidence-backed, and concise so it fits perfectly on ONE page.
"""

url = "http://localhost:11434/api/generate"
payload = {
    "model": "qwen2.5:14B",
    "prompt": prompt,
    "stream": False
}

print("Sending request to local Ollama Qwen 2.5 14B for Single-Page Synthesis...")
data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req) as response:
        res_body = response.read().decode('utf-8')
        res_json = json.loads(res_body)
        synthesis = res_json.get("response", "")
        
        with open("qwen_one_page_synthesis.txt", "w", encoding="utf-8") as out_f:
            out_f.write(synthesis)
            
        print("Qwen single-page synthesis successfully saved!")
        print("Preview:\n", synthesis[:400])
except Exception as e:
    print("Error invoking Ollama Qwen:", e)
