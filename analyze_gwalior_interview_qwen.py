import urllib.request
import json
import os

# Load transcript from output.md
with open("output.md", "r", encoding="utf-8") as f:
    transcript_text = f.read()

prompt = f"""
You are a Lead Qualitative Researcher and Teacher Professional Development (TPD) Policy Expert.
Analyze the following interview transcript of a Gwalior school teacher conducted under the Continuous Professional Development Ecosystem Diagnostic Study (CPD EDS).

TRANSCRIPT CONTENT:
{transcript_text}

PROVIDE A COMPREHENSIVE QUALITATIVE RESEARCH REPORT structured with the following sections:

1. EXECUTIVE SUMMARY & KEY HIGHLIGHTS
2. RESPONDENT PROFILE & CONTEXTUAL CONSTRAINTS
   - Staffing context (Single/two-teacher school realities)
   - Non-academic burden (BLO duties, administrative work, APAR ID, elections)
3. TRAINING ENGAGEMENT & FORMAT PREFERENCES
   - In-person training experience & value drivers (group work, peer discussion)
   - Digital training perception (DIKSHA, iGOT) vs. In-person preference
   - Barriers to digital engagement (connectivity, lack of two-way interaction, real-time doubt clarification)
4. RETENTION & CLASSROOM TRANSFER GAPS
   - Recall analysis of Margdarshika and training modules
   - Application of learning (e.g. group discussion) vs recall struggle
5. PEER LEARNING COMMUNITIES (CLSS / SHAIKSHIK SAMWAAD)
   - Valued aspects (peer experience sharing)
   - Facilitation challenges (clarity of messaging)
   - Single-teacher limitation in school-level cascading
6. CLASSROOM OBSERVATION & MENTORING EXPECTATIONS
   - Teacher's mental model of observation (syllabus tracking vs pedagogical support)
   - Expectations from CACs/Academic Mentors (Demand for live classroom demonstrations)
7. ACTIONABLE POLICY & SYSTEMIC RECOMMENDATIONS

Make the analysis highly detailed, structured, insightful, and grounded strictly in the transcript evidence.
"""

url = "http://localhost:11434/api/generate"
payload = {
    "model": "qwen2.5:14B",
    "prompt": prompt,
    "stream": False
}

print("Sending request to Ollama qwen2.5:14B...")
data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req) as response:
        res_body = response.read().decode('utf-8')
        res_json = json.loads(res_body)
        analysis = res_json.get("response", "")
        
        with open("Gwalior_Teacher_CPD_Analysis_Qwen.md", "w", encoding="utf-8") as out_f:
            out_f.write(analysis)
            
        print("Analysis successfully saved to Gwalior_Teacher_CPD_Analysis_Qwen.md")
except Exception as e:
    print("Error invoking Ollama:", e)
